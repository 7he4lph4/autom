# Auto Map Base Map Functions

alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
c = combat()


def mapPresent():
    map_combatant = None
    for name in ("map", "dm", "lair"):
        map_combatant = c.get_combatant(name)
        if map_combatant:
            break
    return map_combatant


def parse_map_info(info):
    return {
        f[0].lower(): f[1]
        for f in [i.split(": ") for i in [r for r in info.split(" ~ ")]]
        if len(f) == 2
    }


def parse_mapsize(size_str):
    return (
        [20, 20]
        if ("x" not in size_str or any(not s.isdigit() for s in size_str.split("x")))
        else [max(1, int(s)) for s in size_str.split("x")][:2]
    )


def get_map_info():
    for combatant in c.combatants:
        for effect in combatant.effects:
            if effect.name == "map":
                map_info = parse_map_info(effect.attacks[0].attack.automation[0].text)
                return map_info, combatant
    return {}, None


def parse_note(note):
    if not note:
        return {}
    return {
        item.split(":")[0].lower().strip(): item.split(":")[1].strip()
        for item in note.split("|")
        if ":" in item
    }


def update_combatant_note(combatant, **kwargs):
    note = parse_note(combatant.note)
    note.update(kwargs)
    new_note = " | ".join(f"{k.title()}: {v.strip()}" for k, v in note.items())
    combatant.set_note(new_note)


def attach_map_to_combatant(map_state):
    map_info, map_combatant = get_map_info()
    if not map_combatant:
        missing_map_warning = f"Map init object missing!\n\nPlease add a map object to combat using:\n`{pref}i add 0 DM -p 20`"
        return False, missing_map_warning

    # Update map_info with new state
    map_info.update(map_state)

    # Format map information
    info_str = " ~ ".join(f"{k.capitalize()}: {v}" for k, v in map_info.items() if v)

    # Create or update the effect
    map_combatant.add_effect(
        "map",
        attacks=[
            {
                "attack": {
                    "name": "map",
                    "automation": [{"type": "text", "text": info_str}],
                    "_v": 2,
                }
            }
        ],
    )

    return True, f"Map information attached to {map_combatant.name}"


def generate_map_image(overlays=None):
    map_url = f"{get('otfbm_base_url', 'http://otfbm.io/')}"

    # Get the latest map info from the map combatant
    map_info, map_combatant = get_map_info()

    # Use the stored map options or defaults
    cell_size = map_info.get("options", get("mapOptions", ""))
    if cell_size:
        map_url += f"@{cell_size}/"

    # Use the stored map size or default
    mapsize = map_info.get("size", get("mapSize", "10x10"))
    map_url += f"{mapsize}"

    # Add combatants
    combatant_str = ""
    for combatant in c.combatants:
        if combatant.name.lower() not in ["map", "dm", "lair"]:
            note = parse_note(combatant.note)
            location = note.get("location")
            if location:
                size = note.get("size", "M")
                size_letter = size[0].upper()  # Ensure size letter is uppercase
                # Get grid size for token from size map
                size_map = {"T": 1, "S": 1, "M": 1, "L": 2, "H": 3, "G": 4}
                grid_size = size_map.get(size_letter, 1)

                color = note.get("color", "b" if "/" in combatant.hp_str() else "r")
                if len(color) in (3, 6) and color.isalnum():
                    color = f"~{color.upper()}"
                else:
                    color = color[0]
                name = combatant.name.replace(" ", "_")

                # Build the combatant string for the map URL
                combatant_str += f"/{location}{size_letter}{color}"
                combatant_str += f"-{name}"
    if combatant_str:
        map_url += combatant_str

    # Add overlays
    if overlays:
        # Ensure overlays are prefixed with '*'
        processed_overlays = [f"*{overlay.lstrip('*')}" for overlay in overlays]
        # Join overlays with '/'
        overlays_str = "/".join(processed_overlays)
        # Add overlays to the map URL
        map_url += f"/{overlays_str}"

    # Add walls
    walls = map_info.get("walls", "").split(", ") if map_info.get("walls") else []
    walls_str = "_".join(walls)
    if walls_str:
        map_url += f"_{walls_str}/"

    # Add objects
    objects = map_info.get("objects", "").split("/") if map_info.get("objects") else []
    if objects:
        map_url += "/".join(objects) + "/"

    # Add fog of war
    fow = map_info.get("fow", "").split(", ") if map_info.get("fow") else []
    if fow:
        map_url += "*f" + "/*f".join(fow).replace(":", "") + "/"

    # Add background
    bg_image = map_info.get("background", get("mapBg", ""))
    if bg_image:
        map_url += f"?bg={bg_image.split('?')[0]}"

    # Add JSON data
    loadedjson = map_info.get("json", "").split(", ") if map_info.get("json") else []
    if loadedjson:
        map_url += f"{'&' if '?' in map_url else '?'}load={'&load='.join(loadedjson)}"

    return map_url


# Placement Functions


def get_placed_combatants():
    placed, unplaced = {}, {}
    for co in c.combatants:
        if typeof(co) == "SimpleGroup":
            for gco in co.combatants:
                data, p = process_map_combatant(gco, placed)
                (placed if p else unplaced)[gco.name] = data
        elif co.name.lower() not in ["map", "dm", "lair"]:
            data, p = process_map_combatant(co, placed)
            (placed if p else unplaced)[co.name] = data
    return placed, unplaced


def update_adjacent(data, placed):
    if 0 < len(data.get("adjacent", [])):
        for name in data["adjacent"]:
            placed[name]["adjacent"].remove(data["combatant"].name)
    data["adjacent"] = []

    x, y = data["pos"]
    size_offset = (data["size_mod"] + 1, data["size_mod"] + 1)
    for pname, pc in placed.items():
        pcx, pcy = subtract_coords(pc["pos"], size_offset)
        pc_size = size_offset[0] + pc["size_mod"] + 1
        if (x in range(pcx, pcx + pc_size + 1)) and (
            y in range(pcy, pcy + pc_size + 1)
        ):
            data["adjacent"].append(pname)
            pc["adjacent"].append(data["combatant"].name)


def process_map_combatant(combatant, placed):
    data = parse_note(combatant.note)
    data["combatant"] = combatant
    if "location" in data:
        data["pos"] = loc_to_coords(data["location"])
        data["size_mod"] = get_size_mod(data.get("size", "M"))
        update_adjacent(data, placed)
        return data, True
    return data, False


def update_position(combatant, placed, position, out):
    co_name = combatant.name
    data = placed.get(co_name, {})
    data["location"] = coords_to_loc(position)
    data["pos"] = position
    update_adjacent(data, placed)
    placed[co_name] = data

    update_combatant_note(combatant, location=data["location"])
    out[co_name] = out.get(co_name, {})
    out[co_name]["location"] = data["location"]


def update_occupied(occupied_grid, space_mod, data, width, height):
    top = (data["pos"][0] - space_mod, data["pos"][1] - space_mod)
    xbound, ybound = width - space_mod, height - space_mod + 1
    size = data["size_mod"] + 1
    occupied_y = list(range(max(top[1], 1), min(top[1] + size + space_mod, ybound)))
    for x in range(max(top[0], 0), min(data["pos"][0] + size, xbound)):
        if x in occupied_grid:
            occupied_grid[x] = list(set(occupied_grid[x] + occupied_y))
            if height - space_mod <= len(occupied_grid[x]):
                occupied_grid.pop(x)


# Coordinate Functions


def loc_to_coords(loc):
    loc_x = "".join(x for x in loc if x.isalpha()).upper()
    loc_y = "".join(y for y in loc if y.isdigit())
    if not loc_x or not loc_y:
        return (0, 0)
    x = 0
    for s in loc_x:
        x = x * 26 + (alph.index(s) + 1)
    return (x - 1, int(loc_y))


def coords_to_loc(coords):
    loc_x = ""
    x = round(coords[0])  # - 1
    while 0 <= x:
        loc_x = alph[x % 26] + loc_x
        x = (x // 26) - 1
    return f"{loc_x}{round(coords[1])}"


def add_coords(a, b):
    return (a[0] + b[0], a[1] + b[1])


def subtract_coords(a, b):
    return (a[0] - b[0], a[1] - b[1])


def scale_coords(coords, scale):
    return ((coords[0] * scale), (coords[1] * scale))


def distance(coord1, coord2):
    return sqrt((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2)


def get_nearest_coords(coords1, coords2):
    dist, c1_nearest, c2_nearest = -1, (0, 1), (0, 1)
    for gc1 in coords1:
        for gc2 in coords2:
            d = distance(gc1, gc2)
            if d < dist or dist < 0:
                dist, c1_nearest, c2_nearest = d, gc1, gc2
    return dist, c1_nearest, c2_nearest


def get_nearest(pos1, size1, pos2, size2):
    nx1, ny1 = pos1
    nx2, ny2 = pos2
    x, s = 0, max(size1, size2)
    while x < s:
        x += 1
        if x <= size1:
            x1, y1 = pos1[0] + x, pos1[1] + x
            nx1 = x1 if (abs(nx2 - x1) < abs(nx2 - nx1)) else nx1
            ny1 = y1 if (abs(ny2 - y1) < abs(ny2 - ny1)) else ny1
        if x <= size2:
            x2, y2 = pos2[0] + x, pos2[1] + x
            nx2 = x2 if ((abs(nx1 - x2) < abs(nx1 - nx2))) else nx2
            ny2 = y2 if ((abs(ny1 - y2) < abs(ny1 - ny2))) else ny2
    distance = round(distance((nx1, ny1), (nx2, ny2))) * 5
    return distance, (nx1, ny1), (nx2, ny2)


def get_placed_distances(name, target_names, placed):
    pos, size = placed[name].pos, placed[name].size_mod
    distances = {}
    for pc, data in placed.items():
        if pc != name and pc in target_names and "pos" in data:
            nearest = get_nearest(pos, size, data.pos, data.size_mod)
            distances[nearest[0]] = distances.get(nearest[0], []) + [
                (pc, nearest[1], nearest[2])
            ]
    dkeys = list(distances.keys())
    dkeys.sort()
    return {k: distances[k] for k in dkeys}


def get_move_coords(name, placed, width, height):
    size = placed[name].size_mod
    rbound, bbound = width - size, height - size
    occupied = set()
    unoccupied = set()
    for pc_name, pc in placed.items():
        if pc_name == name:
            continue
        occupied.update(occupied_box(size, pc.pos, pc.size_mod))
        unoccupied.update(melee_box(size, pc.pos, pc.size_mod))
    unoccupied -= occupied
    unoccupied = [
        p for p in unoccupied if (0 <= p[0] < rbound) and (1 <= p[1] <= bbound)
    ]
    return unoccupied, occupied


def filter_occupied(name, placed, distances, move_coords, max_targets=1):
    targets = {}
    size = placed[name].size_mod
    for d, dist_targets in distances.items():
        for data in dist_targets:
            target = data[0]
            melee = {}
            mbox = melee_box(size, placed[target].pos, placed[target].size_mod)
            for p in move_coords:
                if p in mbox:
                    mdist = round(distance(placed[name].pos, p)) * 5
                    melee[mdist] = melee.get(mdist, []) + [p]
            if melee:
                mkeys = list(melee.keys())
                mkeys.sort()
                targets[target] = {"distance": d, "melee": {k: melee[k] for k in mkeys}}
                if max_targets <= len(targets):
                    return targets
    return targets


# Sizes: <=M: 0, L: 1, H: 2, G: 3
def get_size_mod(size):
    size_map = {"T": 0, "S": 0, "M": 0, "L": 1, "H": 2, "G": 3}
    return size_map.get(size[0].upper(), 0)


def gbox(top_left, size=0, include_inner=False):
    if size < 1:
        return [top_left]
    x0, y0 = int(top_left[0]), int(top_left[1])
    x1, y1 = x0 + size, y0 + size
    y_range = range(max(y0 + 1, 1), y1)
    box = {x0: y_range}
    if 1 < size:
        x_range = range(x0 + 1, x1)
        y = list(y_range) if include_inner else (y0, y1)
        box.update({x: y for x in x_range})
    box[x1] = y_range
    return


def gmelee(size1, c2, size2):
    top_left = (c2[0] - size1 + 1, c2[1] - size1 + 1)
    mbox = gbox(top_left, size1 + size2 + 1)


def box(top_left, size=0, include_inner=False):
    if size <= 0:
        return [top_left]
    x0, y0 = int(top_left[0]), int(top_left[1])
    x1, y1 = x0 + size, y0 + size
    x_range = range(max(x0, 0), x1 + 1)
    y_range = range(max(y0 + 1, 1), y1)
    box_coords = [(x, y) for x in x_range for y in (y0, y1) if 0 < y]
    x_range = x_range if include_inner else (max(x0, 0), x1)
    return box_coords + [(x, y) for x in x_range for y in y_range]


# Sorts by distance if C1 is not None
def melee_box(size1, c2, size2, c1=None):
    top_left = subtract_coords(c2, (size1 + 1, size1 + 1))
    melee_box = box(top_left, size1 + size2 + 2)
    if c1:
        melee_box.sort(key=lambda c: distance(c1, c))
    return melee_box


def occupied_box(size1, c2, size2):
    occ_top_left = subtract_coords(c2, (size1, size1))
    return box(occ_top_left, size1 + size2, True)


def center(top_left, size):
    return [top_left[0] + (size / 2), top_left[1] + (size / 2)]


# Bresenham Circle Algorithm
def circle(center, radius, offset=0, bounds=[0, 1, 20, 21]):
    if radius < 0:
        return [center]
    h, k = center[0], center[1]
    offset += 0 if ((h % 1 == 0) and (k % 1 == 0)) else 0.5
    x, y = offset, radius - offset

    points = []

    def oct_points(h, k, x, y):
        hnx, hny, hx, hy = (
            max(int(h - x), bounds[0]),
            max(int(h - y), bounds[0]),
            min(int(h + x), bounds[2]),
            min(int(h + y), bounds[2]),
        )
        knx, kny, kx, ky = (
            max(int(k - x), bounds[1]),
            max(int(k - y), bounds[1]),
            min(int(k + x), bounds[3]),
            min(int(k + y), bounds[3]),
        )
        return [
            (hnx, ky),
            (hnx, kny),
            (hny, kx),
            (hny, knx),
            (hx, ky),
            (hx, kny),
            (hy, kx),
            (hy, knx),
        ]

    points = oct_points(h, k, x, y + offset)
    d = 1 - radius  # - 0.5
    while x < y:
        x += 1
        if d < 0:
            d += 2 * x + 1
        else:
            y -= 1
            d += 2 * (x - y) + 1
        xoct_points = oct_points(h, k, x, y + offset)
        points += xoct_points
    points = list(set(points))
    points.sort(key=lambda x: (x[0], x[1]))
    return points


# Raycasting Algorithm
def points_in_shape(shape, points):
    return [
        p
        for p in points
        if (p in shape)
        or len([s for s in shape if (p[1] == s[1] and p[0] < s[0])]) % 2 != 0
    ]


def points_outside_shape(shape, points):
    return [
        p
        for p in points
        if not (
            (p in shape)
            or len([s for s in shape if (p[1] == s[1] and s[0] < p[0])]) % 2 != 0
        )
    ]


def diff_box(coords, top_left, box_size):
    diff_box = box(top_left, box_size)
    new_circle = points_outside_shape(diff_box, coords)
    intersection = points_in_shape(coords, diff_box)
    return new_circle + intersection


def get_line_area(start_pos, end_pos, width=0):
    # Generate the list of coordinates covered by a line from start_pos to end_pos
    # Implement Bresenham's Line Algorithm to get the points on the line
    x1, y1 = int(round(start_pos[0])), int(round(start_pos[1]))
    x2, y2 = int(round(end_pos[0])), int(round(end_pos[1]))
    coords = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x, y = x1, y1
    sx = -1 if x1 > x2 else 1
    sy = -1 if y1 > y2 else 1
    if dx == 0 and dy == 0:
        coords.extend(box([x, y], width))
    elif dx >= dy:
        err = dx / 2.0
        while x != x2:
            coords.extend(box([x, y], width))
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
        coords.extend(box([x, y], width))
    else:
        err = dy / 2.0
        while y != y2:
            coords.extend(box([x, y], width))
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
        coords.extend(box([x, y], width))
    # Remove duplicates
    coords = list(set(coords))
    return coords

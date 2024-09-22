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
        for attack in combatant.attacks:
            if attack.name == "map":
                map_info = parse_map_info(attack.raw.automation[-1].text)
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
        map_combatant = mapPresent()

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


def get_all_map_combatants():
    return {
        co.name: parse_note(co.note)
        for co in c.combatants
        if co.name.lower() not in ["map", "dm", "lair"]
    }


def generate_map_image(overlays=None):
    map_url = f"{get('otfbm_base_url', 'http://otfbm.io/')}"

    # Get the latest map info from the map combatant
    map_info, _ = get_map_info()

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


# Coordinate Functions


def loc_to_coords(loc):
    loc_x = "".join(x for x in loc if x.isalpha()).upper()
    loc_y = "".join(y for y in loc if y.isdigit())
    if not loc_x or not loc_y:
        return [0, 0]
    return [alph.index(loc_x), int(loc_y)]


def coords_to_loc(coords):
    x_index = max(0, min(round(coords[0]), len(alph) - 1))
    y = max(1, min(20, round(coords[1])))
    return f"{alph[x_index]}{y}"


def add_coords(a, b):
    return [a[0] + b[0], a[1] + b[1]]


def subtract_coords(a, b):
    return [a[0] - b[0], a[1] - b[1]]


def scale_coords(coords, scale):
    return [coords[0] * scale, coords[1] * scale]


def distance(coord1, coord2):
    return sqrt((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2)


def get_nearest_coords(coords1, coords2, max_dist=-1):
    dist, c1_nearest, c2_nearest = -1, (0, 0), (0, 0)
    for gc1 in coords1:
        for gc2 in coords2:
            d = distance(gc1, gc2)
            if (d < dist or dist < 0) and (d <= max_dist or max_dist < 0):
                dist, c1_nearest, c2_nearest = d, gc1, gc2
    return dist, c1_nearest, c2_nearest


# Sizes: <=M: 0, L: 1, H: 2, G: 3
def get_size_mod(size):
    size_map = {"T": 0, "S": 0, "M": 0, "L": 1, "H": 2, "G": 3}
    return size_map.get(size[0].upper(), 0)


def box(top_left, size=0, include_inner=False):
    bottom_right = add_coords(top_left, [size, size])
    return [
        (x, y)
        for x in range(top_left[0], bottom_right[0] + 1)
        for y in range(top_left[1], bottom_right[1] + 1)
        if (
            include_inner
            or x in [top_left[0], bottom_right[0]]
            or y in [top_left[1], bottom_right[1]]
        )
        and (0 <= x and 0 < y)
    ]


def out_box(top_left, size=0, include_inner=False):
    out_top_left = subtract_coords(top_left, [1, 1])
    return box(out_top_left, size + 2, include_inner)


def melee_box(size1, c2, size2):
    move_top_left = subtract_coords(c2, [size1 + 1, size1 + 1])
    return box(move_top_left, size1 + size2 + 2)


def occupied_box(size1, c2, size2):
    occ_top_left = subtract_coords(c2, [size1, size1])
    return box(occ_top_left, size1 + size2, True)


def get_occupied_coords(my_name="", my_size=0):
    occupied = set()
    for name, data in get_all_map_combatants().items():
        if name and (name == my_name):
            continue
        if "location" in data:
            pos = loc_to_coords(data["location"])
            size = get_size_mod(data.get("size", "M"))
            occupied.update(occupied_box(my_size, pos, size))
    return occupied


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
        return [
            (h + x, k + y),
            (h + x, k - y),
            (h - x, k + y),
            (h - x, k - y),
            (h + y, k + x),
            (h + y, k - x),
            (h - y, k + x),
            (h - y, k - x),
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
    points = [
        p
        for p in list(set(points))
        if (bounds[0] <= p[0] < bounds[2]) and (bounds[1] <= p[1] < bounds[3])
    ]
    points.sort(key=lambda x: (x[0], x[1]))
    return points

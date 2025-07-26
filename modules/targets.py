# Auto Targeting Module

using(
    autolib="ec14bc6e-81e4-4df7-86e9-5d64ed2fa9b7",
    Mob="f47ec495-d76b-4d71-8834-6e369dfabae5",
    Map="04794472-def2-46d2-b9ba-f765321e39d1",
)

party = []
monsters, dead_monsters = [], []

if c := combat():
    for co in c.combatants:
        if not co.hp or co.name.lower() in ["dm", "map", "lair"]:
            continue
        if 0 < co.hp:
            (monsters if autolib.isMonster(co) else party).append(co)
        elif autolib.isMonster(co):
            dead_monsters.append(co)

notes = {
    "no_combat": '-f "|__**Channel is not in combat!**__"',
    "not_in_combat": '-f "|__**<name> is not in combat!**__"',
    "no_map": '-f "|__**Map not found for auto targeting!**__"',
    "not_on_map": '-f "|__**<name> not found on map!**__"',
    "no_targets": '-f "|__**No valid targets found!**__"',
    "cq_ranged": '''-f "Ranged Attacks in Close Combat|All ranged attack rolls have Disadvantage if made within 5 feet of an enemy that isn't Incapacitated and can see the attacker."''',
    "no_range": '-f "|__**Auto targeting without parameters!**__"',
    "range_no_targets": '-f "|__**No targets within range!**__"',
}


# Process arguments for -at targeting snippet
def parse_target_args(args):
    processed_args = (
        argparse(args).last("at", default="", ephem=True).lower().replace("true", "")
    )
    valid_args = ["m", "r", "dash"]

    targ_args = {}
    for targ in processed_args.split("|"):
        tsubargs = [t for t in targ.split(":") if t]
        if not tsubargs:
            tsubargs = ["r", []]
        elif tsubargs[0].isdigit():
            tsubargs = ["m", [int(tsubargs[0])]]
        elif "/" in tsubargs[0]:
            tsubargs = ["r", tsubargs[0]]

        if len(tsubargs) == 1:
            if tsubargs[0].startswith("m"):
                tsubargs = ["m", [5]]
            else:
                tsubargs = ["r", []]

        elif not typeof(tsubargs[1]) == "SafeList":
            tsubargs[1] = [int(tsa) for tsa in tsubargs[1].split("/") if tsa.isdigit()]

        if tsubargs[0] in valid_args:
            targ_args[tsubargs[0]] = tsubargs[1]
    return targ_args


def get_co_movement(co):
    movement, move_mode = 0, "walk"
    if move_effect := co.get_effect("Remaining Movement"):
        movement = int("".join([c for c in move_effect.name if c.isdigit()]))
    elif co.monster_name:
        movement, move_mode = Mob.get_monster_speed(co.monster_name)
    else:
        movement = 30
    return movement, move_mode


def get_target_lists(targs={}):
    master_list = [
        co
        for co in c.combatants
        if co
        and co.name.lower() not in ["dm", "map", "lair"]
        and (targs.get("dead", False) or 0 < co.hp)
    ]
    if targs.get("order", "_") in "hl":
        sort_health(
            master_list,
            descending=(targs.order == "h"),
            true_hp=(not autolib.isMonster(master_list[0])),
        )

    monster_list, party_list = [], []
    for co in c.combatants:
        (monster_list if autolib.isMonster(co) else party_list).append(co)
    return master_list, party_list, monster_list


def sort_health(target_list, descending=False, true_hp=False):
    # fmt: off
    state_sort = lambda t: (
        5 if (t.max_hp <= t.hp) else
        4 if (0.5 <= t.hp / t.max_hp) else
        3 if (0.15 < t.hp / t.max_hp) else
        2 if (0 < t.hp / t.max_hp) else 1
    )
    # fmt: on
    target_list.sort(
        reverse=(descending),
        key=((lambda t: t.hp) if true_hp else state_sort),
    )


def get_teams():
    teams = {}
    for co in c.combatants:
        if not co.hp or co.name.lower() in ["dm", "map", "lair"]:
            continue
        if any(effect.name.startswith("Ghost (auto)") for effect in co.effects):
            continue

        for effect in co.effects:
            if effect.name.startswith("Ally (auto)"):
                teams[1] = teams.get(1, []) + [co.name]
                break
            if all(e in effect.name for e in ["Team", "(auto)"]):
                team = int("".join([c for c in effect.name if c.isdigit()]))
                teams[team] = teams.get(team, []) + [co.name]
                break
        else:
            team = 1 if not autolib.isMonster(co) else max(max(teams, default=2), 2)
            teams[team] = teams.get(team, []) + [co.name]
    return teams


def get_my_team(teams, name):
    my_team, enemies = 1, []
    for t in teams:
        if name in teams[t]:
            my_team = t
        else:
            enemies += teams[t]
    return my_team, enemies


# Map Functions
def bounded_box(top_left, bottom_right, map_size=[20, 20]):
    x0, y0 = max(1, top_left[0]), max(1, top_left[1])
    x1, y1 = min(map_size[0], bottom_right[0]), min(map_size[1], bottom_right[1])
    return {x: range(y0, y1 + 1) for x in range(x0, x1 + 1)}


def move_box(location, movement, size=1, map_size=[20, 20]):
    move_mod = max(0, movement // 5)
    size_mod = max(0, size - 1)
    move_tl = [location[0] - move_mod, location[1] - move_mod]
    move_br = [location[0] + size_mod + move_mod, location[1] + size_mod + move_mod]
    return bounded_box(move_tl, move_br, map_size)


def target_box(placed, target_pco, atk_range, map_size=[20, 20]):
    target_loc = [target_pco["loc"][0] + 1, target_pco["loc"][1]]
    tsize_mod = target_pco["size_mod"]
    range_mod = max(0, atk_range // 5)
    tsr = range_mod + tsize_mod
    target_tl = [target_loc[0] - range_mod, target_loc[1] - range_mod]
    target_br = [target_loc[0] + tsr, target_loc[1] + tsr]
    return bounded_box(target_tl, target_br, map_size)


def get_occupied_box(co, placed_co, map_size=[20, 20]):
    size_mod = co["size_mod"]
    pco_loc = [placed_co["loc"][0] + 1, placed_co["loc"][1]]
    pco_size_mod = placed_co["size_mod"]
    pco_tl = (pco_loc[0] - size_mod, pco_loc[1] - size_mod)
    pco_br = (pco_loc[0] + pco_size_mod, pco_loc[1] + pco_size_mod)
    return bounded_box(pco_tl, pco_br, map_size)


def box_difference(box1, box2):
    diff_box = box1.copy()
    for x in box2:
        if x not in diff_box:
            continue
        new_y_range = [y for y in diff_box[x] if y not in box2[x]]
        if new_y_range:
            diff_box[x] = new_y_range
        else:
            diff_box.pop(x, None)
    return diff_box


def box_intersection(box1, box2):
    inter_box = {}
    for x in box1:
        if x not in box2:
            continue
        inter_y_range = [y for y in box1[x] if y in box2[x]]
        if inter_y_range:
            inter_box[x] = inter_y_range
    return inter_box


def get_valid_movement(placed, co_name, co_data, movement=0, map_size=[20, 20]):
    location = [co_data["loc"][0] + 1, co_data["loc"][1]]
    size_mod = co_data["size_mod"]
    move_box = move_box(location, movement, size_mod + 1, map_size)
    for placed_name, placed_data in placed.items():
        if placed_name == co_name:
            continue
        occupied_box = get_occupied_box(co_data, placed_data, map_size)
        move_box = box_difference(move_box, occupied_box)
    return move_box


def distance(start, end):
    dx = abs(end[0] - start[0])
    dy = abs(end[1] - start[1])
    straight = abs(dx - dy)
    diag = min(dx, dy)
    diag_cost = (diag // 2) * 3 + (1 if diag % 2 else 0)
    return round(diag_cost + straight)


def get_nearest_spaces(spaces, location):
    nearest_spaces = []
    min_distance = float("inf")
    for x, y_range in spaces.items():
        for y in y_range:
            dist = distance(location, (x, y))
            if dist < min_distance:
                min_distance = dist
                nearest_spaces = [(x, y)]
            elif dist == min_distance:
                nearest_spaces.append((x, y))
    return nearest_spaces


def get_farthest_spaces(spaces, location):
    farthest_spaces = []
    max_distance = 0
    for x, y_range in spaces.items():
        for y in y_range:
            dist = distance(location, (x, y))
            if max_distance < dist:
                max_distance = dist
                farthest_spaces = [(x, y)]
            elif dist == max_distance:
                farthest_spaces.append((x, y))
    return farthest_spaces


def filter_true_distance(move_attack_box, location, movement):
    filtered_box = {}
    for x, y_range in move_attack_box.items():
        filtered_y = [
            y for y in y_range if distance(location, (x, y)) <= round(movement) // 5
        ]
        if filtered_y:
            filtered_box[x] = filtered_y
    return filtered_box


alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def loc_to_cell(location):
    loc_x = ""
    x = round(location[0]) - 1
    while 0 <= x:
        loc_x = alph[x % 26] + loc_x
        x = (x // 26) - 1
    return f"{loc_x}{round(location[1])}"


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


def create_arrow_overlay(distance, start_cell, end_cell, color="r"):
    return f"*a{distance}{color}{start_cell}{end_cell}"


def move_to_location(combatant, start_location, to_location):
    start_cell, to_cell = loc_to_cell(start_location), loc_to_cell(to_location)
    update_combatant_note(combatant, location=to_cell)
    move_distance = distance(start_location, to_location) * 5
    phrase = f"Moving from {start_cell} to {to_cell} (~{move_distance} ft.)"
    overlays = [create_arrow_overlay(move_distance, start_cell, to_cell)]
    map = Map.generate_map_image(overlays)
    return phrase, map

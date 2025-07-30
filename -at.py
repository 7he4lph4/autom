<drac2>
using(Targets="cb0a8fe6-0eb1-4cc1-a868-f0b4d19cda92")

notes = {k: n.replace("<name>", name) for k, n in Targets.notes.items()}
errpref = "miss -i"

c = combat()
if not c: return notes["no_combat"]

co = c.get_combatant(name)
if not co: return f'{errpref} {notes["not_in_combat"]}'

using(Map="04794472-def2-46d2-b9ba-f765321e39d1")

args = &ARGS&
targ_args = Targets.parse_target_args(args)
movement, move_mode = Targets.get_co_movement(co)

# Map Data
map_info, map_attach_co = Map.get_map_info()
if not map_attach_co: return notes["no_map"]
map_size = [int(s) for s in map_info.get("size", "20x20").split("x")][:2]
placed, unplaced = Map.get_placed_combatants()

# Combatant Map Data
co_map_data = placed.get(name, {})
if not co_map_data: return notes["not_on_map"]
location = co_map_data["loc"][0] + 1, co_map_data["loc"][1]
size_mod = co_map_data["size_mod"]

# Targets and Teams
targets, party, monsters = Targets.get_target_lists()
teams = Targets.get_teams()
my_team, raw_enemies = Targets.get_my_team(teams, name)
enemies = [e for e in raw_enemies if e in [t.name for t in targets]]

# Get Distances and Unoccupied Coordinates
target_distances = Map.get_placed_distances(name, enemies, placed)
if not target_distances: return f'{errpref} {notes["no_targets"]}'
closest = min(target_distances)

move_delta = 0
move_spaces = Targets.get_valid_movement(placed, name, co_map_data, movement, map_size)
true_distance = get_svar("trueDistance", True)

out = {}

# unoccupied, occupied = Map.get_move_coords(name, placed, map_width, map_height)
# if "dash" in pargs:
#     return Map.dash_towards(
#         co, name, movement, placed, enemies, closest, unoccupied, occupied, cell, location, out
#     )



target = randchoice(target_distances[closest])[0]
if closest <= 5:
    if "m" in targ_args: return f'-t "{target}"'
    if "r" in targ_args: return f'-t "{target}" dis {notes["cq_ranged"]}'

move_melee = list(targ_args.keys())[0] == "m"
flank = move_melee and get_svar("flank", True)
for ttype, trange in targ_args.items():
    if not trange: return f'-t "{target}" {notes["no_range"]}'

    if ttype == "e":
        target_distances = Map.get_placed_distances(name, [t.name for t in targets], placed)
        in_range_targets = []
        for d, t in target_distances.items():
            if d <= trange[0]:
                in_range_targets += [dt[0] for dt in t if dt[0] not in in_range_targets]
        return ' '.join(f'-t "{target}"' for target in in_range_targets)
                
    
    atk_range, max_range = trange[0], trange[-1]
    adv = ""
    
    if ttype == "m":
        atk_range = int(atk_range) if atk_range else 5
        max_range = atk_range
    elif ttype == "r" and (movement + atk_range < closest):
        adv = "dis"

    if movement + max_range < closest: continue
    if (closest <= atk_range) and not move_melee: return f'-t "{target}"'

    valid_dts = {d: t for d, t in target_distances.items() if d <= movement + max_range}
    for d, t in valid_dts.items():
        for dt_name, (mx, my), (tx, ty) in t:
            pdt_box = Targets.target_box(placed, placed[dt_name], atk_range, map_size)
            move_attack_box = Targets.box_intersection(move_spaces, pdt_box)
            if true_distance:
                move_attack_box = Targets.filter_true_distance(move_attack_box, location, movement)
            if not move_attack_box: continue

            if move_melee:
                move_attack_box = Targets.get_nearest_spaces(move_attack_box, (tx + 1, ty))
            else:
                move_attack_box = Targets.get_farthest_spaces(move_attack_box, (tx + 1, ty))

            move_location = randchoice(move_attack_box)
            phrase, map = Targets.move_to_location(co, location, move_location)

            # Update Movement Speed
            move_delta = Map.distance(location, move_location) * 5
            if 0 < move_delta:
                co.remove_effect("Remaining Movement")
                co.add_effect(f'Remaining Movement: {movement - move_delta} ft. {move_mode}', duration=0, end=True)
            return f'-t "{dt_name}" {adv} -phrase "{phrase}" -thumb "{map}"'

return f'{errpref} {notes["no_targets"]}'
</drac2>
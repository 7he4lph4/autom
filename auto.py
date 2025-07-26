<drac2>
#auto
pref, al = ctx.prefix, ctx.alias
cmd = pref+al
null, nl, comma = '', '\n', ','
args = argparse(&ARGS&)

cname_list, command_list, combatant_mismatch = [],[],[]
multiattack, spell_viable, counter = False, False, 0

team_colors = {1: "b", 2: "r", 3: "y", 4: "g", 5: "o", 6: "p"}

raw_inp = "&*&"
inp = "&*&".lower().replace('"', '')
inp1 = "&1&"
inp2 = "&2&"
inp3 = "&3&"

c = combat()

using(
    helpl = "2020ae6c-6c1f-4044-a1a7-45137357ff6d", # importing only this early since targl accesses combat variables and combat() is null in below if block and errors out
)

# Simple advanced help implementation without pagination
if inp == 'advanced':
    title = f"Advanced 🤖 Auto Monster AI Reference - Comprehensive Usage Guide"
    desc = helpl.advanced_help_text
    return f'embed -title "{title}" -desc "{desc}" -color {color}'

if not c or inp == 'help' or inp == '?':
    title = helpl.help_title
    desc = helpl.help_text
    return f'embed -title "{title}" -desc "{desc}"'

using(
    # autolib = "ec14bc6e-81e4-4df7-86e9-5d64ed2fa9b7",
    # autolib test
    autolib = "b02daf2d-7cfc-4b0c-8fd2-f7be253e8f13",

    core = "49f5f503-1c00-4f24-ba43-92e65c2c2fb6",
    presets = "c14e4526-4acb-4964-8ba9-f6861617ffdf",
    #presets test
    # presets = "9262c036-97ad-4c8b-a34c-ee0d351c06e4",

    
    # mapl = "faa1ca51-5c75-401c-be46-8650472e68f2",
    # mapl test
    mapl = "1d668d94-2807-47ca-b07c-e414b3342b5f",
    
    # mobl = "65c27eae-11c3-4b5c-90e5-472bc49f0037",
    # mobl test
    mobl = "56f70775-86f6-46c5-ae74-acb839bbee74",

    #targl = "f8369cc0-8ab0-42a5-8dfd-4ab7f34c0e61",
    # targl test
    targl = "0e93fa5a-ba10-4981-9efb-11f7e114101a"
)

command = f"""multiline{nl}"""
footer = f'{cmd} help | made by @alpha983'

if inp1.lower() in ['m', 'map'] and inp2.lower() == 'list':
    return command + nl.join(presets.generate_list_embeds(footer))


title = helpl.help_title
desc_text = helpl.help_text

if inp1.lower() == 'lair':
    command_list.append(f'{pref}i add 0 Lair -p 20')
    command_list.append(f'''{pref}embed -title "A Lair Object has been added!" -desc "A Lair object was added at Initiative 20 to run monsters' Lair Actions." -color <color>''')
    return command + nl.join(command_list)


# INITIALIZING COMBAT AND MAP

combatants = c.combatants
combatant_list, party_list, monster_list = targl.get_target_lists()

party_names = [p.name for p in party_list]
monster_names, monster_types = [], []
for mon in monster_list:
    monster_names.append(mon.name)
    monster_types.append(mon.monster_name)

# Map-related variables
alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
size_map = {'T': 1, 'S': 1, 'M': 1, 'L': 2, 'H': 3, 'G': 4}
map_base_url = get("otfbm_base_url", "http://otfbm.io/")
mapsize = get("mapSize", "20x20")

map_combatant = mapl.mapPresent()
map_info, map_attach = mapl.get_map_info()
if not map_attach:
    map_attach = (
        map_combatant if map_combatant
        else combat().me if combat().me else party_list[0] if 0 < len(party_list) else None
    )
    if not map_attach:
        desc = f"""No combatant found to attach the map to!
        \nIf you are fighting a monster with Lair Actions, add a Lair object with:
        `{cmd} lair`\n\nOtherwise, a player must join the combat initiative using `{pref}i join`
        """
        return f'embed -title "Map Setup Pending:" -desc "{desc}" -color <color>'
    
    map_attach.add_effect("map", attacks=[{"attack": {"name":"map", "automation": [{"type":"text", "text":""}], "_v":2,}}])
    
    desc = helpl.no_map
    command_list.append(f'{pref}embed -title "Map Settings attached to {map_attach.name}!" -desc "{desc}" -color <color>')
    # return f'embed -title "Map Settings attached to {map_attach.name}!" -desc "{desc}" -color <color>'
map_state = {
    "current_map": None, 
    "size": map_info.get("size", [20, 20]),
    "mapoptions": map_info.get("options", ""),
    "bg_image": map_info.get("background", "")
}
width, height = mapl.parse_mapsize(map_state.get("size"))

teams = {}
for co in c.combatants:
    if co.name.lower() in ["dm", "map", "lair"] or autolib.isGhost(c, co):
        continue
    for effect in co.effects:
        if effect.name.startswith("Ally (auto)"):
            teams[1] = teams.get(1, []) + [co.name]
            break
        if all(e in effect.name for e in ["Team", "(auto)"]):
            team = int("".join([e for e in effect.name if e.isdigit()]))
            teams[team] = teams.get(team, []) + [co.name]
            break
    else:
        team = 1 if not autolib.isMonster(co) else max(max(teams, default=2),2)
        teams[team] = teams.get(team, []) + [co.name]

placed, unplaced = mapl.get_placed_combatants(teams, team_colors)
map_state["combatants"] = placed

# Update colors for already placed combatants based on teams
for combatant_name, data in placed.items():
    combatant = data.get("combatant")
    if combatant:
        combatant_team = mapl.get_combatant_team(combatant_name, teams)
        new_color = team_colors.get(combatant_team, "r")
        data["color"] = new_color
        # Update the combatant's note to reflect new color
        mapl.update_combatant_note(combatant, {}, color=new_color)

out = {}

new_combat = False
if (inp1.lower() in ['m', 'map']) or not map_info:
    map_name = inp2 if inp1.lower() in ['m', 'map'] else ""
    message = presets.load_specific_map(map_state, map_attach, map_name)
    width, height = mapl.parse_mapsize(map_state.get("size"))
    map_info = {"size": f"{width}x{height}", "background": map_state.get("bg_image", ""), "options": map_state.get("mapoptions", "")}
    if unplaced:
        mapl.place_combatants(placed, unplaced, width, height, out, map_state, teams, team_colors)
    map_url = mapl.generate_map_image(map_info=map_info)
    command_list.append(f'{pref}embed {message} -image "{map_url}"')
    new_combat = True

# Place any unplaced combatants on the map
if unplaced:
    mapl.place_combatants(placed, unplaced, width, height, out, map_state, teams, team_colors)
    map_url = mapl.generate_map_image(map_state=map_state)
    command_list.append(f'{pref}embed -title "Map Setup Complete!" -desc "All combatants have been placed on the map." -image "{map_url}"')
    new_combat = True
    
if not party_names:
    err(helpl.no_players)

# Initialize overlays and descriptions
overlays = []
desc = []

# Remove dead monsters from combat
dead_monster_names = []
if targl.dead_monsters:
    for dead_monster in targl.dead_monsters:
        dead_monster_names.append(dead_monster.name)
        mapl.update_combatant_note(dead_monster, map_state, color="gy")
        dead_monster.set_group("Dead monsters")
    map_url = mapl.generate_map_image(overlays, map_state=map_state)
    command_list.append(
        pref + core.make_embed(
            title="Removing Dead Monsters", 
            desc="**The following dead monsters were found:**\n" + ", ".join(dead_monster_names)
        ) + f" -image {map_url}"
    )
    command_list.append(
        f"{pref}i n" if c.current and c.current.name in dead_monster_names else f'{pref}i remove "Dead monsters"'
    )
    if not targl.monsters:
        command_list.append(
            pref + core.make_embed(
                title="No monsters found in initiative!",
                desc=f'All monsters have been defeated!\n\nFeel free to add more at any time and run `{cmd}` to place them on the map.'
            )
        )
        return command + nl.join(command_list)
    new_combat = True

# Check if there are any monsters in initiative
if not targl.monsters:
    command_list.append(
        pref + core.make_embed(
            title="No monsters found in initiative!",
            desc=f'That\'s fine, feel free to add them any time and run `{cmd}` every time it\'s the monster\'s turn!'
        )
    )
    return command + nl.join(command_list)

# Check if it's the first round of combat
current_init = combatants[0].name if not c.current else c.current.name
if c.current is None:
    command_list.append(f'{pref}i n')

# Check if it's a lair action turn
if current_init.casefold() in ['map', 'dm', 'lair']:
    title = f'Waiting on Lair Action :dragon:'
    desc_text = f'Use `{pref}i n` if there are no actions to take this round!'
    command_list.append(f'{pref}embed -title "{title}" -desc "{desc_text}"')
    return command + nl.join(command_list)

current_combatant = c.get_combatant(current_init)

# It's a group's turn
if not current_combatant:
    current_combatant = c.get_group(current_init)
    if current_combatant:
        title = f'It\'s a group\'s turn! :dragon:'
        desc_text = f"Waiting on **{current_init}** to play their turn!"
        command_list.append(f'{pref}embed -title "{title}" -desc "{desc_text}"')
        return command + nl.join(command_list)

# It's a player's turn
if not current_combatant.monster_name:
    title = f'It\'s a player turn! :mage:'
    desc_text = f"Waiting on **{current_init}** to play their turn!"
    if not get_uvar('mapStates'):
        desc_text += helpl.move_help
    command_list.append(f'{pref}embed -title "{title}" -desc "{desc_text}"')
    return command + nl.join(command_list)

# Current combatant has the "Stop Automation" effect
if current_combatant.monster_name and current_combatant.get_effect("Stop Automation (auto)"):
    title = f'Stopping automation for {current_combatant.name}'
    desc_text = f"Automation has been stopped for **{current_combatant.name}**'s turn! Use `{pref}i n` to continue automation!"
    command_list.append(f'{pref}embed -title "{title}" -desc "{desc_text}"')
    return command + nl.join(command_list)

# New combat current combatant is a monster
if new_combat:
    title = f'Ready to automate monsters! :robot:'
    desc_text = f'''**Use `{cmd}` again to automate the following monsters:**\n{", ".join([m for m in monster_names if m not in dead_monster_names])}'''
    command_list.append(f'{pref}embed -title "{title}" -desc "{desc_text}"')
    return command + nl.join(command_list)
  
    
# MAP INITIALIZATION COMPLETE

def find_best_aoe_position(monster, aoe_attack, target_names):
    best_position = None
    max_targets = 0
    monster_map_data = mapl.parse_note(monster.note)
    monster_location = monster_map_data.get('location', None)
    if not monster_location:
        return None

    mapX, mapY = width, height

    # Generate positions in the monster's line of sight/direction
    # For simplicity, we'll consider positions in front of the monster
    # Assuming the monster is facing towards the majority of targets

    # Find the center position of all targets to determine general direction
    target_positions = []
    for target_name in target_names:
        target = c.get_combatant(target_name)
        if target:
            target_map_data = mapl.parse_note(target.note)
            target_location = target_map_data.get('location', None)
            if target_location:
                coords = mapl.loc_to_coords(target_location)
                target_positions.append(coords)

    if not target_positions:
        return None

    # Calculate average position of targets
    avg_x = sum(pos[0] for pos in target_positions) / len(target_positions)
    avg_y = sum(pos[1] for pos in target_positions) / len(target_positions)
    direction_vector = [avg_x - mapl.loc_to_coords(monster_location)[0], avg_y - mapl.loc_to_coords(monster_location)[1]]

    # Normalize direction vector
    length = sqrt(direction_vector[0] ** 2 + direction_vector[1] ** 2)
    if length == 0:
        direction_vector = [0, 1]  # Default direction
    else:
        direction_vector = [direction_vector[0] / length, direction_vector[1] / length]

    # Check positions in the direction the monster is facing
    for distance in range(1, max(mapX, mapY)):
        x = mapl.loc_to_coords(monster_location)[0] + int(direction_vector[0] * distance)
        y = mapl.loc_to_coords(monster_location)[1] + int(direction_vector[1] * distance)
        if x < 0 or y < 1 or x >= len(alph) or y > mapY:
            break
        position = f"{alph[x]}{y}"
        affected_targets = count_affected_targets(position, aoe_attack, target_names)
        if affected_targets > max_targets:
            max_targets = affected_targets
            best_position = position

    return best_position

def count_affected_targets(position, aoe_attack, targets):
    affected = 0

    for target in targets:
        target_map_data = mapl.parse_note(c.get_combatant(target).note)
        target_location = target_map_data.get('location', None)
        if target_location and is_in_aoe(position, target_location, aoe_attack):
            affected += 1
    return affected

def is_in_aoe(origin, target, aoe_attack):
    ox, oy = alph.index(origin[0]), int(origin[1:])
    tx, ty = alph.index(target[0]), int(target[1:])
    dx, dy = abs(tx - ox), abs(ty - oy)
    distance = max(dx, dy) * 5  # Assuming 5ft per square

    if aoe_attack['shape'] in ['cone', 'sphere', 'radius']:
        return distance <= aoe_attack['size']
    elif aoe_attack['shape'] == 'line':
        return (dx == 0 or dy == 0 or dx == dy) and distance <= aoe_attack['size']
    elif aoe_attack['shape'] in ['cube', 'cylinder']:
        return dx <= aoe_attack['size'] // 5 and dy <= aoe_attack['size'] // 5

    return False

def distance(pos1, pos2):
    x1, y1 = alph.index(pos1[0].upper()), int(pos1[1:])
    x2, y2 = alph.index(pos2[0].upper()), int(pos2[1:])
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    
    # D&D 5e uses a simplified diagonal movement rule
    # where every other diagonal counts as 10 feet instead of 5
    diagonals = min(dx, dy)
    straight = abs(dx - dy)
    
    return (diagonals * 5) + (straight * 5)

def draw_aoe_overlay(monster, aoe_attack, position, targets):
    shapeDict = [{"type": "circle",     "name":"c",  "num": [3], "args": ("size", "color", "loc")},
               {"type": "circletop",    "name":"ct", "num": [3], "args": ("size", "color", "loc")},
               {"type": "circlecorner", "name":"co", "num": [3], "args": ("size", "color", "loc")},
               {"type": "cone",         "name":"t",  "num": [4], "args": ("size", "color", "loc", "eloc")},
               {"type": "line",         "name":"l",  "num": [5], "args": ("size", "width", "color", "loc", "eloc")},
               {"type": "arrow",        "name":"a",  "num": [3], "args": ("color", "loc", "eloc")},
               {"type": "square",       "name":"s",  "num": [3,4], "args": ("size", "color", "loc", "eloc")},
               {"type": "squaretop",    "name":"st", "num": [3,4], "args": ("size", "color", "loc", "eloc")}]

    color = 'r'  # Default color for AoE
    shape = aoe_attack['shape']
    size = aoe_attack.get('size', 10)
    
    # Create a dictionary mapping shape names to their short codes
    shape_to_code = {item['type']: item['name'] for item in shapeDict}
    
    if shape in ['sphere', 'radius', 'cube', 'cylinder']:
        shape_code = shape_to_code['circle' if shape in ['sphere', 'radius'] else 'square']
        return f"{shape_code}{size}{color}{position}"
    
    if shape in ['cone', 'line']:
        nearest_target = min(targets, key=lambda t: distance(position, mapl.parse_note(c.get_combatant(t).note).get('location', 'A1')))
        nearest_pos = mapl.parse_note(c.get_combatant(nearest_target).note).get('location', 'A1')
        shape_code = shape_to_code[shape]
        return f"{shape_code}{size},{aoe_attack.get('width', size) if shape == 'line' else ''}{color}{position}{nearest_pos}".rstrip(',')
    
    return None

def find_adjacent_position(monster_location, target_position):
    mx, my = alph.index(monster_location[0]), int(monster_location[1:])
    tx, ty = alph.index(target_position[0]), int(target_position[1:])
    
    adjacent_positions = [
        (mx-1, my), (mx+1, my), (mx, my-1), (mx, my+1),
        (mx-1, my-1), (mx-1, my+1), (mx+1, my-1), (mx+1, my+1)
    ]
    
    closest_position = min(adjacent_positions, key=lambda p: ((p[0]-tx)**2 + (p[1]-ty)**2))
    return f"{alph[closest_position[0]]}{closest_position[1]}"

def get_targets_in_aoe(monster_location, aoe_attack, target_names):
    affected_targets = []
    for target_name in target_names:
        target = c.get_combatant(target_name)
        if target:
            target_map_data = mapl.parse_note(target.note)
            target_location = target_map_data.get('location', None)
            if target_location and is_in_aoe(monster_location, target_location, aoe_attack):
                affected_targets.append(target_name)
    return affected_targets

def get_attack_reach(attack_str):
    attack_str = attack_str.lower()
    if 'reach' in attack_str:
        words = attack_str.split()
        for i, word in enumerate(words):
            if word == 'reach' and i + 1 < len(words):
                reach = ''.join(core.filter(str.isdigit, words[i+1]))
                if reach:
                    return int(reach)
    return 8  # Default melee reach

def get_max_attack_reach(attacks):
    max_reach = 8
    for attack in attacks:
        reach = get_attack_reach(str(attack))
        if reach > max_reach:
            max_reach = reach
    return max_reach

def get_spell_range(spell_name):
    spell_data = load_json(get_gvar('00d6334d-af6c-46ac-b810-752465e0ad33'))
    spell_name = spell_name.strip('"')  # Remove quotes if present
    for spell in spell_data:
        if spell['name'].lower() == spell_name.lower():
            range_str = spell['range']
            # Extract the numeric value from the range string
            range_value = ''.join(core.filter(str.isdigit, range_str))
            return int(range_value) if range_value else 30  # Default to 30 if no numeric value found
    return 30  # Default range if spell not found

def move_towards(start_pos, end_pos, distance, unoccupied, occupied=[]):
    total_distance = mapl.distance(start_pos, end_pos) * 5
    dxy = mapl.subtract_coords(end_pos, start_pos)
    ratio = min(distance / total_distance, 1) if 0 < total_distance else 0
    
    move_pos = mapl.add_coords(start_pos, mapl.scale_coords(dxy, ratio))
    move_pos = (round(move_pos[0]), round(move_pos[1]))
    if move_pos not in occupied:
        return mapl.coords_to_loc(move_pos), None, move_pos
    
    if len(unoccupied) < 1:
        return mapl.coords_to_loc(start_pos), None, start_pos
    
    unocc = list(unoccupied)
    found = []
    move_dist = -1
    for p in unocc:
        if distance < round(mapl.distance(start_pos, p)) * 5:
            continue
        end_dist = mapl.distance(p, end_pos)
        if end_dist <= move_dist or move_dist < 0:
            found.append(p)
            move_pos, move_dist = p, end_dist
    
    # if move_pos in occupied:
    #     return mapl.coords_to_loc(start_pos), None, start_pos
    # command_list.append(f'{pref}echo {move_pos}')
    # goto = list(unoccupied)
    # goto.sort(key=lambda p: mapl.distance(move_pos, p))
    
    # Generate arrow overlay with correct syntax
    distanceT = round(mapl.distance(start_pos, move_pos)) * 5
    color = 'r' # Use red color for the arrow
    start_location = mapl.coords_to_loc(start_pos)
    new_location = mapl.coords_to_loc(move_pos)
    arrow = f"*a{distanceT}{color}{start_location}{new_location}"
    
    return new_location, arrow, move_pos

def create_arrow_overlay(distance, start_location, end_location):
    colr = 'r' # Use red color for the arrow
    return f"*a{distance}{colr}{start_location}{end_location}"

def find_best_target(monster, target_names, move_coords=[], distances={}, max_surrounding=2):
    if len(distances) < 1:
        return None, -1, None
    
    if min(distances) <= 5:
        dist = min(distances)
        return randchoice(distances[dist])[0], dist, None
    
    filtered_targets = mapl.filter_occupied(monster.name, placed, distances, move_coords)
    if not filtered_targets:
        dist = min(distances)
        data = randchoice(distances[dist])
        return data[0], dist, {dist: [data[2]]}
    
    for k, v in filtered_targets.items():
        return k, v["distance"], v["melee"]
    
    #if monster.stats.intelligence < 20:
    
    targets = [c.get_combatant(tname) for tname in target_names if c.get_combatant(tname)]
    target_hp = [(t, t.hp) for t in targets if t.hp is not None and 0 < t.hp]    
    if not target_hp:
        return randchoice(distances[min(distances)])
     
    def count_surrounding_monsters(target):
        tname = target.name
        if not tname in placed:
            return 0, False
        adjacent = placed[tname].get("adjacent", [])
        large_monster_present = any(0 < placed[aname]["size_mod"] for aname in adjacent)
        return len(adjacent), large_monster_present
    
    # Sort targets by HP and intelligence level
    if 17 <= monster.stats.intelligence:
        sorted_targets = core.sorted(target_hp, key=lambda x: x[1])
    else:
        # Weighted random selection favoring lower HP targets
        weights = [max(1, 100 - t[1]) for t in target_hp]
        sorted_targets = [t for t, _ in core.sorted(core.zip(target_hp, weights), key=lambda x: x[1], reverse=True)]
    
    for target, _ in sorted_targets:
        monster_count, large_monster_present = count_surrounding_monsters(target)
        if monster_count < max_surrounding and not large_monster_present:
            return target.name
    
    # If all preferred targets are surrounded or near large monsters, choose the least surrounded one without a large monster
    valid_targets = [t for t in sorted_targets if not count_surrounding_monsters(t[0])[1]]
    if valid_targets:
        return min(valid_targets, key=lambda x: count_surrounding_monsters(x[0])[0])[0].name
    
    # If all targets have large monsters nearby, choose a random target from the valid ones (those with HP > 0)
    return randchoice([t.name for t, _ in target_hp]) if target_hp else None

def getAttackText(attack):
    """Extract the text from the attack's automation entries."""
    for entry in attack.raw.get('automation', []):
        if entry.get('type') == 'text' and 'text' in entry:
            return entry['text']
    return ''

def extract_attack_range(attack):
    """Safely extract the range from a ranged attack."""
    text = getAttackText(attack)
    if 'range' in text.lower():
        try:
            # Look for pattern like "range 150/600 ft." or "range 80 ft."
            range_part = text.split('range')[1].split('/')[0].split('ft.')[0].strip()
            # Extract just the numbers
            range_value = ''.join(core.filter(str.isdigit, range_part))
            return int(range_value) if range_value else 30
        except ("IndexError", "ValueError"):
            return 30
    return 30

def parse_range(range_code, range_shape_map):
    if not range_code:
        return None, None, None, None
    n = len(range_code)
    # Handle just single-letter (e.g. 'S', 'T', 'V')
    if n == 1:
        shape_code = range_code
        return None, shape_code, None, range_shape_map.get(shape_code, shape_code)
    # Handle patterns like "60R5", "120L5", "15C"
    i = 0
    while i < n and range_code[i].isdigit():
        i += 1
    dist_ft = int(range_code[:i]) if i > 0 else None
    # Next letter is shape
    if i < n:
        shape_code = range_code[i]
        i += 1
    else:
        shape_code = None
    # Remaining is size
    size_ft = int(range_code[i:]) if i < n and range_code[i:].isdigit() else None
    shape_name = range_shape_map.get(shape_code, shape_code)
    return dist_ft, shape_code, size_ft, shape_name


# **HELPER FUNCTIONS FOR EFFICIENT AoE PROCESSING**
def get_team_positions(teams, placed, exclude_name=None):
    """Pre-compute all creature positions by team - O(n)"""
    team_positions = {}
    all_positions = {}
    
    for team_num, team_members in teams.items():
        team_positions[team_num] = []
        for member_name in team_members:
            if member_name in placed and member_name != exclude_name:
                creature_data = {
                    "name": member_name,
                    "pos": placed[member_name]["pos"],
                    "location": placed[member_name]["location"],
                    "size_mod": placed[member_name].get("size_mod", 0),
                    "team": team_num
                }
                team_positions[team_num].append(creature_data)
                all_positions[member_name] = creature_data
    
    return team_positions, all_positions

def creatures_in_circle(center_pos, radius_ft, all_positions):
    """Fast circle collision detection using distance squared - O(n)"""
    targets_hit = []
    radius_squared = radius_ft ** 2
    
    for creature_data in all_positions.values():
        creature_pos = creature_data["pos"]
        creature_size = creature_data["size_mod"]
        
        # Check if any part of creature is within circle
        hit = False
        for dx in range(creature_size + 1):
            for dy in range(creature_size + 1):
                check_x = creature_pos[0] + dx
                check_y = creature_pos[1] + dy
                
                # Distance squared (no sqrt needed = faster)
                distance_squared = ((center_pos[0] - check_x) * 5) ** 2 + ((center_pos[1] - check_y) * 5) ** 2
                
                if distance_squared <= radius_squared:
                    hit = True
                    break
            if hit:
                break
        
        if hit:
            targets_hit.append(creature_data)
    
    return targets_hit

def find_optimal_circle_center(aoe_origin, aoe_size, chosen_target, caster_pos, caster_team, all_positions, width, height, spell_range):
    """Ultra-efficient O(1) circle optimization using smart heuristics"""
    
    if aoe_origin == "Target":
        # Target-centered spells - use smart positioning with max 3 candidates
        
        enemies = [pos for pos in all_positions.values() if pos["team"] != caster_team]
        
        if not enemies:
            # No enemies - fallback to original target
            target_pos = all_positions.get(chosen_target, {"pos": caster_pos})["pos"]
            return mapl.coords_to_loc(target_pos), [all_positions[chosen_target]] if chosen_target in all_positions else []
        
        # **SMART CANDIDATE SELECTION - MAX 3 POSITIONS**
        candidates = []
        
        # Candidate 1: Enemy centroid (optimal for clustered enemies)
        enemy_center_x = sum(e["pos"][0] for e in enemies) / len(enemies)
        enemy_center_y = sum(e["pos"][1] for e in enemies) / len(enemies)
        centroid_pos = (round(enemy_center_x), round(enemy_center_y))
        
        # Validate centroid is within range and bounds
        centroid_distance = sqrt((centroid_pos[0] - caster_pos[0])**2 + (centroid_pos[1] - caster_pos[1])**2) * 5
        if (centroid_distance <= spell_range and 
            0 <= centroid_pos[0] < width and 1 <= centroid_pos[1] <= height):
            candidates.append(centroid_pos)
        
        # Candidate 2: Densest enemy position (best for spread enemies)
        if len(enemies) > 1:
            best_density_pos = None
            max_nearby = 0
            
            for enemy in enemies[:min(3, len(enemies))]:  # Check only first 3 for efficiency
                enemy_pos = enemy["pos"]
                nearby_count = sum(1 for e in enemies if sqrt((e["pos"][0] - enemy_pos[0])**2 + (e["pos"][1] - enemy_pos[1])**2) * 5 <= aoe_size)
                if nearby_count > max_nearby:
                    max_nearby = nearby_count
                    best_density_pos = enemy_pos
            
            if best_density_pos and best_density_pos not in candidates:
                density_distance = sqrt((best_density_pos[0] - caster_pos[0])**2 + (best_density_pos[1] - caster_pos[1])**2) * 5
                if density_distance <= spell_range:
                    candidates.append(best_density_pos)
        
        # Candidate 3: Original target position (fallback)
        if chosen_target in all_positions:
            target_pos = all_positions[chosen_target]["pos"]
            target_distance = sqrt((target_pos[0] - caster_pos[0])**2 + (target_pos[1] - caster_pos[1])**2) * 5
            if target_distance <= spell_range and target_pos not in candidates:
                candidates.append(target_pos)
        
        # If no valid candidates, use closest enemy within range
        if not candidates:
            valid_enemies = [e for e in enemies if sqrt((e["pos"][0] - caster_pos[0])**2 + (e["pos"][1] - caster_pos[1])**2) * 5 <= spell_range]
            if valid_enemies:
                closest_enemy = min(valid_enemies, key=lambda e: sqrt((e["pos"][0] - caster_pos[0])**2 + (e["pos"][1] - caster_pos[1])**2))
                candidates.append(closest_enemy["pos"])
    
    else:
        # Self-centered spells - true O(1)
        candidates = [caster_pos]
    
    # **EVALUATE CANDIDATES - MAX 3 EVALUATIONS**
    best_center = mapl.coords_to_loc(caster_pos)
    best_score = -999
    best_targets = []
    
    for candidate_pos in candidates:
        score, targets = score_circle_position(candidate_pos, aoe_size, all_positions, caster_team)
        if score > best_score:
            best_score = score
            best_center = mapl.coords_to_loc(candidate_pos)
            best_targets = targets
    
    return best_center, best_targets

def score_circle_position(center_pos, radius_ft, all_positions, caster_team):
    """Optimized scoring - early exit when possible"""
    targets_hit = []
    score = 0
    radius_squared = radius_ft ** 2
    
    for creature_data in all_positions.values():
        creature_pos = creature_data["pos"]
        creature_size = creature_data["size_mod"]
        
        # Quick distance check first (faster than full collision)
        dx = abs(center_pos[0] - creature_pos[0]) * 5
        dy = abs(center_pos[1] - creature_pos[1]) * 5
        
        # Skip if obviously too far (before expensive collision check)
        if dx > radius_ft + (creature_size * 5) or dy > radius_ft + (creature_size * 5):
            continue
        
        # Only do full collision check if potentially in range
        hit = False
        for sx in range(creature_size + 1):
            for sy in range(creature_size + 1):
                check_x = creature_pos[0] + sx
                check_y = creature_pos[1] + sy
                distance_squared = ((center_pos[0] - check_x) * 5) ** 2 + ((center_pos[1] - check_y) * 5) ** 2
                
                if distance_squared <= radius_squared:
                    hit = True
                    break
            if hit:
                break
        
        if hit:
            targets_hit.append(creature_data)
            score += 2 if creature_data["team"] != caster_team else -1
    
    return score, targets_hit
# **HELPER FUNCTIONS FOR EFFICIENT AoE PROCESSING**


# Spell Lookup Helper Functions
def preprocess_spell_data(spell_list, spell_data):
    """
    Pre-process spell data for O(1) lookups
    Returns: spell_levels, spell_ranges, spell_aoe_info dictionaries
    """
    spell_levels = {}
    spell_ranges = {}
    spell_aoe_info = {}
    
    # Range/AoE shape mapping for quick lookup
    shape_map = {
        "u": "Radius", "r": "Radius", "t": "Square", "q": "Square",
        "g": "Cone", "p": "Line", "w": "Wall", "a": "Feet",
        "s": "Self", "v": "Self", "y": "Sight", "z": "Willing", "x": "Unlimited"
    }
    
    for spell_name in spell_list:
        if spell_name in spell_data:
            spell_info = spell_data[spell_name]
            spell_levels[spell_name] = spell_info.get("l", 0)
            
            # Parse range/AoE from "r" key
            range_code = spell_info.get("r", "")
            range_value, aoe_size, shape_code = parse_spell_range_aoe(range_code)
            
            # Set spell range
            if range_value == 0 and aoe_size > 0:
                spell_ranges[spell_name] = aoe_size  # Self spells use AoE size as effective range
            else:
                spell_ranges[spell_name] = range_value if range_value > 0 else 30
            
            # Store AoE info if it has area effect
            if aoe_size > 0 and shape_code in shape_map:
                origin = "Self" if range_code.upper().startswith('S') else "Target"
                spell_aoe_info[spell_name] = {
                    "shape": shape_map[shape_code],
                    "size": aoe_size,
                    "origin": origin
                }
        else:
            spell_ranges[spell_name] = 30  # Default range for unknown spells
    
    return spell_levels, spell_ranges, spell_aoe_info

def parse_spell_range_aoe(range_code):
    """
    Parse a spell range code like 'SQ15', '60R5', '120L10'
    Returns: (range_value, aoe_size, shape_code)
    """
    if not range_code:
        return 30, 0, ""
    
    range_value = 0
    aoe_size = 0
    shape_code = ""
    
    # Handle "Self" cases like "SQ15" (thunderwave, etc.)
    if range_code.upper().startswith('S'):
        range_value = 0  # Self range
        remaining = range_code[1:]
        
        # Find the last sequence of digits (AoE size)
        aoe_nums = ""
        i = len(remaining) - 1
        while i >= 0 and remaining[i].isdigit():
            aoe_nums = remaining[i] + aoe_nums
            i -= 1
        
        if aoe_nums:
            aoe_size = int(aoe_nums)
        
        # Find shape letter just before the numbers
        if i >= 0 and aoe_nums:
            shape_code = remaining[i].lower()
    else:
        # Extract leading numbers (range)
        i = 0
        range_nums = ""
        while i < len(range_code) and range_code[i].isdigit():
            range_nums += range_code[i]
            i += 1
        
        if range_nums:
            range_value = int(range_nums)
        
        # Find the last sequence of digits (AoE size) working backwards
        aoe_nums = ""
        j = len(range_code) - 1
        while j >= i and range_code[j].isdigit():
            aoe_nums = range_code[j] + aoe_nums
            j -= 1
        
        if aoe_nums:
            aoe_size = int(aoe_nums)
            # Shape letter should be just before the AoE numbers
            if j >= i and j < len(range_code):
                shape_code = range_code[j].lower()
    
    return range_value, aoe_size, shape_code

def get_viable_spells(monster, spell_levels):
    """Get all spells the monster can currently cast, sorted by level (highest first)"""
    viable_spells = [
        (s, spell_levels[s])
        for s in spell_levels
        if monster.spellbook.can_cast(s, spell_levels[s])
    ]
    viable_spells.sort(key=lambda x: x[1], reverse=True)
    return viable_spells
# Spell Lookup Helper Functions

# Spellcasting GOD Functions
def can_move_into_spell_range(current_pos, target_pos, spell_range, monster_speed, unoccupied, occupied, monster_size_mod, target_distance):
    """
    Check if monster can move into spell range and return movement details
    Returns: (can_move, move_distance, new_position)
    """
    distance_needed = target_distance - spell_range
    
    if distance_needed <= monster_speed and len(unoccupied) > 0:
        move_distance = min(monster_speed, distance_needed + 5)  # +5 for safety margin
        
        # Calculate potential new position
        total_distance = mapl.distance(current_pos, target_pos) * 5
        dxy = mapl.subtract_coords(target_pos, current_pos)
        ratio = min(move_distance / total_distance, 1) if total_distance > 0 else 0
        
        potential_pos = mapl.add_coords(current_pos, mapl.scale_coords(dxy, ratio))
        potential_pos = (round(potential_pos[0]), round(potential_pos[1]))
        
        if potential_pos in unoccupied and potential_pos not in occupied:
            return True, move_distance, potential_pos
    
    return False, 0, current_pos

def attempt_spell_cast_in_range(monster, spell_name, spell_level, spell_range, target_distance, chosen_target, spell_aoe_info, teams, placed, indexed_combatant, overlays, desc, command_list, map_state, monster_pos, team_colors, width, height):
    """Handle spell casting when already in range"""
    debug_log = f"[CAST-IN-RANGE:{spell_name}:L{spell_level}:R{spell_range}:D{target_distance}]"
    
    # Build targeting and overlay
    target_string = f"-t {chosen_target}"
    
    # **AoE OVERLAY DRAWING**
    if spell_name in spell_aoe_info:
        aoe_data = spell_aoe_info[spell_name]
        aoe_shape = aoe_data["shape"]
        aoe_size = aoe_data["size"]
        aoe_origin = aoe_data["origin"]
        
        # Get team info and pre-compute positions once
        monster_team = mapl.get_combatant_team(indexed_combatant, teams)
        overlay_color = team_colors.get(monster_team, "r")
        team_positions, all_positions = get_team_positions(teams, placed, indexed_combatant)
        
        # **CIRCLE/SPHERE HANDLING**
        if aoe_shape in ["Radius", "Sphere"]:
            best_center, targets_in_aoe = find_optimal_circle_center(
                aoe_origin, aoe_size, chosen_target, monster_pos, 
                monster_team, all_positions, width, height, spell_range
            )
            
            # Create circle overlay and targeting string
            circle_overlay = f"c{aoe_size}{overlay_color}{best_center}"
            overlays.append(f"*{circle_overlay}")
            target_string = build_target_string(targets_in_aoe) if targets_in_aoe else f"-t {chosen_target}"
            
            # Generate description
            if targets_in_aoe:
                enemies = [t for t in targets_in_aoe if t["team"] != monster_team]
                allies = [t for t in targets_in_aoe if t["team"] == monster_team]
                enemy_names = ", ".join([t["name"] for t in enemies])
                ally_names = ", ".join([t["name"] for t in allies])
                hit_desc = f"{len(enemies)} enemies: {enemy_names}" + (f" + ⚠️{len(allies)} allies: {ally_names}" if allies else "")
                desc.append(f"{indexed_combatant} targets {best_center} with *{spell_name}* - {aoe_size} ft. radius hitting {hit_desc}")
            else:
                desc.append(f"{indexed_combatant} casts *{spell_name}* at {best_center}")
            
            # Display map with overlay
            map_state["combatants"] = map_state.get("combatants", {})
            map_url = mapl.generate_map_image(overlays)
            command_list.append(f'{pref}embed -title "{monster.name} casts an AoE Spell - {spell_name} on the map!" -desc "{desc[-1]}" -image "{map_url}"')
        else:
            # Non-circle AoE fallback
            desc.append(f"{indexed_combatant} casts *{spell_name}*")
    else:
        # Non-AoE spell
        desc.append(f"{indexed_combatant} casts *{spell_name}* (Level {spell_level}) - Target at {target_distance} ft, spell range {spell_range} ft.")
    
    # Build spell phrase
    spell_phrase = f":robot: _Auto Monster AI_ - Target: {target_distance} ft, Range: {spell_range} ft"
    if spell_name in spell_aoe_info:
        aoe = spell_aoe_info[spell_name]
        spell_phrase += f" :boom: {aoe['size']} ft. {aoe['shape']} from {aoe['origin']} :boom:"
    
    # Cast the spell
    command_list.append(f'{pref}i cast "{spell_name}" {target_string} -l {spell_level} -phrase "{spell_phrase}"')
    command_list.append(f'{pref}i n')
    
    return True, debug_log

def attempt_spell_cast_with_movement(monster, spell_name, spell_level, spell_range, target_distance, chosen_target, spell_aoe_info, teams, placed, indexed_combatant, overlays, desc, command_list, map_state, start_pos, target_pos, monster_speed, unoccupied, occupied, monster_size_mod, team_colors, width, height, monster_move_verb, location, out):
    """Handle spell casting that requires movement"""
    debug_log = f"[CAST-WITH-MOVE:{spell_name}:L{spell_level}:R{spell_range}:D{target_distance}]"
    
    can_move, move_distance, new_pos = can_move_into_spell_range(
        start_pos, target_pos, spell_range, monster_speed, unoccupied, occupied, monster_size_mod, target_distance
    )
    
    if not can_move:
        return False, f"{debug_log}[MOVE-FAILED]"
    
    # Calculate movement and update position
    new_location, arrow, new_pos = move_towards(start_pos, target_pos, move_distance, unoccupied, occupied)
    new_distance = round(mapl.get_nearest(new_pos, monster_size_mod, target_pos, placed[chosen_target]['size_mod'])[0])
    
    if new_distance > spell_range:
        return False, f"{debug_log}[STILL-OUT-OF-RANGE:{new_distance}>{spell_range}]"
    
    # Apply movement
    mapl.update_position(monster, placed, new_pos, out)
    
    if arrow:
        overlays.append(arrow)
    else:
        distance_moved = round(mapl.distance(start_pos, new_pos)) * 5
        overlays.append(create_arrow_overlay(distance_moved, location, mapl.coords_to_loc(new_pos)))
    
    # Handle AoE after movement (similar to in-range logic but with movement description)
    target_string = f"-t {chosen_target}"
    movement_desc = f"moves and casts *{spell_name}* (Level {spell_level})"
    
    if spell_name in spell_aoe_info:
        aoe_data = spell_aoe_info[spell_name]
        if aoe_data["shape"] in ["Radius", "Sphere"]:
            # AoE handling after movement
            monster_team = mapl.get_combatant_team(indexed_combatant, teams)
            overlay_color = team_colors.get(monster_team, "r")
            team_positions, all_positions = get_team_positions(teams, placed, indexed_combatant)
            
            best_center, targets_in_aoe = find_optimal_circle_center(
                aoe_data["origin"], aoe_data["size"], chosen_target, new_pos, 
                monster_team, all_positions, width, height, spell_range
            )
            
            circle_overlay = f"c{aoe_data['size']}{overlay_color}{best_center}"
            overlays.append(f"*{circle_overlay}")
            target_string = build_target_string(targets_in_aoe) if targets_in_aoe else f"-t {chosen_target}"
            
            if targets_in_aoe:
                enemies = [t for t in targets_in_aoe if t["team"] != monster_team]
                allies = [t for t in targets_in_aoe if t["team"] == monster_team]
                enemy_names = ", ".join([t["name"] for t in enemies])
                ally_names = ", ".join([t["name"] for t in allies])
                hit_desc = f"{len(enemies)} enemies: {enemy_names}" + (f" + ⚠️{len(allies)} allies: {ally_names}" if allies else "")
                movement_desc = f"targets {best_center} with *{spell_name}* (now {new_distance} ft. away, spell range {spell_range} ft.) - {aoe_data['size']} ft. radius hitting {hit_desc}"
    
    # Build final description
    movement_verb = 'move' if monster_move_verb == 'walk' else '*fly*'
    actual_distance = round(mapl.distance(start_pos, new_pos)) * 5
    desc.append(f"{indexed_combatant} uses {actual_distance} ft. out of their {monster_speed} ft. to {movement_verb} towards {chosen_target} (now {new_distance} ft. away, spell range {spell_range} ft.), then {movement_desc}")
    
    # Display updated map
    map_state["combatants"] = out
    map_url = mapl.generate_map_image(overlays)
    command_list.append(f'{pref}embed -title "Monster Movement & Spell: {monster.name}" -desc "{desc[-1]}" -image "{map_url}"')
    
    # Build spell phrase
    spell_phrase = f":robot: _Auto Monster AI_ - Target: {new_distance} ft, Range: {spell_range} ft"
    if spell_name in spell_aoe_info:
        aoe = spell_aoe_info[spell_name]
        spell_phrase += f" :boom: {aoe['size']} ft. {aoe['shape']} from {aoe['origin']} :boom:"
    
    # Cast the spell
    command_list.append(f'{pref}i cast "{spell_name}" {target_string} -l {spell_level} -phrase "{spell_phrase}"')
    command_list.append(f'{pref}i n')
    
    return True, f"{debug_log}[SUCCESS]"

def process_spellcasting(monster, indexed_combatant, chosen_target, distance, teams, placed, overlays, desc, command_list, map_state, start_pos, target_pos, monster_speed, unoccupied, occupied, monster_size_mod, team_colors, width, height, monster_move_verb, location, out):
    """Main spellcasting coordination function"""
    spell_monst = monster.spellbook.caster_level
    if not spell_monst:
        return False
    
    # Load spell data and get spell list
    spell_data = load_json(get_gvar("99f797c7-0c0e-4038-be4b-34f48cf4d26d"))
    spell_list = [spell.name for spell in monster.spellbook.spells]
    
    if not spell_list:
        return False
    
    # Pre-process spell data for O(1) lookups
    spell_levels, spell_ranges, spell_aoe_info = preprocess_spell_data(spell_list, spell_data)
    
    # Get viable spells
    viable_spells = get_viable_spells(monster, spell_levels)
    if not viable_spells:
        return False
    
    debug_log = f"[CASTER:L{spell_monst}][SPELLS:{len(spell_list)}][VIABLE:{len(viable_spells)}][TARGET-DIST:{distance}ft]"
    
    # Try each viable spell until one works
    for spell_name, spell_level in viable_spells:
        spell_range = spell_ranges.get(spell_name, 30)
        debug_log += f"[TRY:{spell_name}:L{spell_level}:R{spell_range}]"
        
        # Check if already in range
        if distance <= spell_range:
            success, attempt_log = attempt_spell_cast_in_range(
                monster, spell_name, spell_level, spell_range, distance, chosen_target,
                spell_aoe_info, teams, placed, indexed_combatant, overlays, desc,
                command_list, map_state, start_pos, team_colors, width, height
            )
            debug_log += attempt_log
            if success:
                ### Uncomment below line to enable 🔍 Spell Debug ###
                # command_list.append(f'{pref}echo {debug_log}')
                return True
        else:
            # Try moving into range
            success, attempt_log = attempt_spell_cast_with_movement(
                monster, spell_name, spell_level, spell_range, distance, chosen_target,
                spell_aoe_info, teams, placed, indexed_combatant, overlays, desc,
                command_list, map_state, start_pos, target_pos, monster_speed,
                unoccupied, occupied, monster_size_mod, team_colors, width, height,
                monster_move_verb, location, out
            )
            debug_log += attempt_log
            if success:
                ### Uncomment below line to enable 🔍 Spell Debug ###
                # command_list.append(f'{pref}echo {debug_log}')
                return True
    
    debug_log += "[FINAL:ALL-SPELLS-FAILED]"
    ### Uncomment below line to enable 🔍 Spell Debug ###
    # command_list.append(f'{pref}echo {debug_log}')
    return False
# Spellcasting GOD Functions


def build_target_string(targets):
    """Build -t target1 -t target2 string"""
    return " ".join(f"-t {target['name']}" for target in targets)

def create_aoe_overlay(shape_type, size, color, center, end_point=None):
    """Extensible AoE overlay creation for future shapes"""
    overlays = {
        "circle": f"c{size}{color}{center}",
        "cone": f"t{size}{color}{center}{end_point or ''}",
        "line": f"l{size},5{color}{center}{end_point or ''}",
        "square": f"s{size}{color}{center}"
    }
    return overlays.get(shape_type, f"c{size}{color}{center}")



def process_monster_turn(indexed_combatant, out, overlays, desc, command_list, snippets=""):
    monster = c.get_combatant(indexed_combatant)
    if not monster:
        desc.append(f"Could not find combatant: {indexed_combatant}")
        return
    
    monster_name = monster.monster_name
    curr_hp = monster.hp
    
    # Check if the monster is already dead at the start of its turn
    if monster.hp <= 0:
        remove_dead_monster(c, monster, out, desc)
        map_url = mapl.generate_map_image(overlays)
        command_list.append(f'{pref}embed -title "Skipping dead monster: {monster.name}" -desc "{monster.name} has been defeated and removed from the map. Its turn will be skipped." -image "{map_url}"')
        command_list.append(f'{pref}i n')  # Skip to next turn
        return

    # Get location from note
    map_data = placed[indexed_combatant]
    location = map_data["location"]
    
    phrase = ""
    team = 1
    for t in teams:
        if indexed_combatant in teams[t]:
            team = t
            break
    targets = [co for t in teams if t != team for co in teams[t]]
    
    # Check if map is present
    if map_attach and location:
        monster_speed, monster_move_verb = mobl.get_monster_speed(monster_name)

        start_pos, size_m = map_data["pos"], map_data["size_mod"]
        
        # Get occupied positions to avoid collisions
        unoccupied, occupied = mapl.get_move_coords(monster.name, placed, width, height)

        ### AoE ###
        aoe_attacks = mobl.get_aoe_attacks(monster.name)
        if aoe_attacks:
            aoe_attack = randchoice(aoe_attacks)

            # Create a list of all potential targets (excluding the monster itself)
            all_combatants = [c.name for c in c.combatants if c.name.lower() not in ['map', 'dm', 'lair']]
            potential_targets = [name for name in all_combatants if name != monster.name]

            # Find the best position for the AoE attack
            best_position = find_best_aoe_position(monster, aoe_attack, potential_targets)

            if best_position:
                # Calculate the distance to the best position
                end_pos = mapl.loc_to_coords(best_position)
                distance_to_position = mapl.distance(start_pos, end_pos) * 5

                # Move the monster if needed
                if distance_to_position > 0:
                    move_distance = min(monster_speed, distance_to_position)
                    new_location, arrow, new_pos = move_towards(start_pos, end_pos, move_distance, unoccupied)
                    mapl.update_position(monster, placed, new_pos, out)
                    if arrow:
                        overlays.append(arrow)
                    location = new_location
                    desc.append(f"{indexed_combatant} uses {int(move_distance)} ft. out of their {monster_speed} ft. to {'move' if monster_move_verb == 'walk' else '*fly*'} towards an optimal position for its AoE attack.")

                    # Display the updated map after movement
                    map_state["combatants"] = out
                    map_url = mapl.generate_map_image(overlays)
                    command_list.append(f'{pref}embed -title "Monster Movement: {monster.name}" -desc "{desc[-1]}" -image "{map_url}"')

                # Adjust the AoE position for cone and line attacks
                if aoe_attack['shape'] in ['cone', 'line']:
                    best_position = find_adjacent_position(location, best_position)

                # Create and add the AoE overlay
                overlay = draw_aoe_overlay(monster, aoe_attack, best_position, potential_targets)
                if overlay:
                    overlays.append(f"*{overlay}")
                    desc.append(f"{monster.name} uses {aoe_attack['name']} starting at {location} towards {best_position}")

                    # Display the map with the AoE overlay
                    map_url = mapl.generate_map_image(overlays)
                    command_list.append(f'{pref}embed -title "AoE Attack: {monster.name}" -desc "{desc[-1]}" -image "{map_url}"')

                    # Find targets within the AoE
                    affected_targets = get_targets_in_aoe(location, aoe_attack, potential_targets)

                    # Add the attack command targeting all affected combatants
                    if affected_targets:
                        target_string = " -t ".join(affected_targets)
                        command_list.append(f'{ctx.prefix}i a "{aoe_attack["name"]}" -t {target_string} -phrase ":robot: _Triggered by auto monster AI_"')
                    else:
                        desc.append(f"No targets were caught in the AoE of {aoe_attack['name']}.")

                    command_list.append(f'{ctx.prefix}i n')
                    return
        ### AoE ###

        placed_distances = mapl.get_placed_distances(monster.name, targets, placed)
        chosen_target, distance, melee = find_best_target(monster, targets, unoccupied, placed_distances)
        
        #return command_list.append(f"!echo {chosen_target}")
        target_combatant = c.get_combatant(chosen_target)
        if not target_combatant:
            desc.append(f"Could not find target: {chosen_target}")
            return

        target_location = placed[chosen_target].get('location', None)
        if target_location:
            max_attack_reach = get_max_attack_reach(monster.attacks)
            
            target_pos = placed[chosen_target]['pos']
            target_size_mod = placed[chosen_target]['size_mod']
            # distance = mapl.get_nearest(start_pos, size_m, target_pos, target_size_mod)[0] * 5
            
            map_state["combatants"] = out


            # Spellcasting GOD Func call - Attempt to cast spells if available
            spell_cast_successful = process_spellcasting(
                monster, indexed_combatant, chosen_target, distance, teams, placed, 
                overlays, desc, command_list, map_state, start_pos, target_pos, 
                monster_speed, unoccupied, occupied, size_m, team_colors, 
                width, height, monster_move_verb, location, out
            )

            # If we successfully cast a spell, return early
            if spell_cast_successful:
                return

            # **EXECUTION FALLS THROUGH TO EXISTING MELEE CODE BLOCK**
            # If no spells worked, the code naturally continues to the melee logic below...


            # Melee combat logic (if not a spellcaster or out of spell slots)
            if max_attack_reach < distance:
                move_distance = min(monster_speed, distance - max_attack_reach)
                go_distance = min(melee)
                go_coords = randchoice(melee[go_distance])
                
                # Determine if the monster has ranged attacks
                ranged_attacks = [
                    atk for atk in monster.attacks
                    if 'Ranged Weapon Attack' in getAttackText(atk)
                ]

                if ranged_attacks:
                    # Choose a ranged attack and its properties
                    chosen_ranged_attack = randchoice(ranged_attacks)

                    # Safely extract range from ranged attack
                    attack_range = extract_attack_range(chosen_ranged_attack)

                    # Check if the target is within range or move towards the edge of range
                    if distance > attack_range:
                        move_distance = min(monster_speed, distance - attack_range)
                        new_location, arrow, new_pos = move_towards(start_pos, target_pos, move_distance, unoccupied)
                        mapl.update_position(monster, placed, new_pos, out)

                        if new_pos != start_pos:
                            new_location = mapl.coords_to_loc(new_pos)  # Convert coordinates to location string
                            overlays.append(create_arrow_overlay(move_distance, location, new_location))
                            desc.append(f"{indexed_combatant} uses {int(move_distance)} ft. out of their {monster_speed} ft. to {'move' if monster_move_verb == 'walk' else '*fly*'} towards {chosen_target}, staying at the edge of their *{chosen_ranged_attack.name}* attack range of {attack_range} ft.")
                        else:
                            desc.append(f"{indexed_combatant} remains stationary ({distance} ft. away from {chosen_target}), already positioned within range for its ranged *{chosen_ranged_attack.name}* attack, which has a range of {attack_range} ft.")
                    else:
                        desc.append(f"{indexed_combatant} remains stationary ({distance} ft. away from {chosen_target}), already positioned within range for its ranged *{chosen_ranged_attack.name}* attack, which has a range of {attack_range} ft.")

                    # Update the map regardless of movement
                    map_state["combatants"] = out
                    map_url = mapl.generate_map_image(overlays)
                    command_list.append(f'{pref}embed -title "Monster Movement: {monster.name}" -desc "{desc[-1]}" -image "{map_url}"')

                    # Perform the ranged attack
                    # Check if this ranged attack can multiattack
                    can_multi, multi_count = autolib.canMultiattack(monster_name, chosen_ranged_attack.raw["name"], c)
                    
                    if can_multi and multi_count > 1:
                        # Perform multiattack with ranged weapon
                        command_list.append(f'{pref}i a "{chosen_ranged_attack.raw["name"]}" -rr {multi_count} autoc -t {chosen_target} -phrase ":robot: _Triggered by auto monster AI_ :crossed_swords: Ranged Multiattack :crossed_swords:"')
                    else:
                        # Perform single ranged attack
                        command_list.append(f'{pref}i a "{chosen_ranged_attack.raw["name"]}" -t {chosen_target} -phrase ":robot: _Triggered by auto monster AI_"')

                    # End the monster's turn
                    command_list.append(f'{pref}i n')
                    return

                # If no ranged attacks, fallback to dashing for melee
                # Monster needs to dash
                if monster_speed < go_distance: # distance - max_attack_reach:
                    new_location, arrow, new_pos = move_towards(start_pos, go_coords, monster_speed * 2, unoccupied, occupied)
                    mapl.update_position(monster, placed, new_pos, out)
                    if new_pos != start_pos:
                        overlays.append(create_arrow_overlay(go_distance, location, new_location))
                    go_distance = round(mapl.distance(start_pos, new_pos)) * 5
                    desc.append(f"{indexed_combatant} dashes {int(go_distance)} ft. out of their {monster_speed * 2} ft. dash distance, towards {chosen_target}.")
                    map_url = mapl.generate_map_image(overlays)
                    command_list.append(f'{pref}embed -title "Monster Dashes: {monster.name}" -desc "{desc[-1]}" -image "{map_url}"')
                    command_list.append(f'{pref}i n')
                    return
                else: # Monster can reach target  
                    new_location = mapl.coords_to_loc(go_coords)
                    mapl.update_position(monster, placed, go_coords, out)
                    overlays.append(create_arrow_overlay(go_distance, location, new_location))
                    distance = round(mapl.get_nearest(go_coords, size_m, target_pos, target_size_mod)[0])
                    desc.append(f"{indexed_combatant} uses {int(go_distance)} ft. out of their {monster_speed} ft. to {'move' if monster_move_verb == 'walk' else '*fly*'} towards {chosen_target}.")
                    
                # After movement, display the updated map
                map_state["combatants"] = out
                map_url = mapl.generate_map_image(overlays)
                command_list.append(f'{pref}embed -title "Monster Movement: {monster.name}" -desc "{desc[-1]}" -image "{map_url}"')
            else:
                phrase = f"\nHolding Position to Attack!"
        else:
            desc.append(f"Could not find location for target: {chosen_target}")

    else:
        chosen_target = targets[randint(len(targets))]
        distance = 8  # Assume adjacent if no map
        desc.append(f"{indexed_combatant} attacks {chosen_target}.")

    # Attack logic
    if distance <= get_max_attack_reach(monster.attacks) and (curr_hp > 0 or autolib.onDeath(indexed_combatant, c.combatants) == "relentless"):
        # Get multiattack data for this monster
        multi_atks = autolib.getMultiAttacks(monster_name, c)
        
        if multi_atks:
            # Monster has multiattack capability
            for atk, num in multi_atks.items():
                atkr = autolib.resolveVersatile(atk)
                command_list.append(f'{pref}i a "{atkr}" {snippets} -rr {num} autoc -t {chosen_target} -phrase ":robot: _Triggered by auto monster AI_ :crossed_swords: Multiattack :crossed_swords:{phrase}"')
            command_list.append(f'{pref}i n')
        else:
            # No multiattack, use single attack
            chosen_atk_string = autolib.getMeleeAttack(indexed_combatant, c.combatants)
            command_list.append(f'{pref}i a "{chosen_atk_string}" {snippets} -t {chosen_target} autoc -phrase ":robot: _Triggered by auto monster AI_{phrase}"')
            command_list.append(f'{pref}i n')    
    elif curr_hp <= 0:
        on_death = autolib.onDeath(indexed_combatant, c.combatants)
        if on_death:
            target_string = f"-t {chosen_target}" if "death" in on_death else ""
            command_list.append(f'{pref}i a "{on_death}" {snippets} {target_string} -phrase ":robot: _Triggered by auto monster AI_"')
        else:
            desc.append(f"Skipping dead monster: {indexed_combatant}")
            command_list.append(f'{pref}i n')
    else:
        desc.append(f"{indexed_combatant} couldn't reach {chosen_target} to attack.")
        command_list.append(f'{pref}i n')

    if monster.hp <= 0:
        remove_dead_monster(c, monster, out, desc)
        map_url = mapl.generate_map_image(overlays)
        command_list.append(f'{pref}embed -title "Skipping dead monster: {monster_name}" -desc "{monster_name} has been defeated and removed from the map. Its turn will be skipped." -image "{map_url}"')
        return

def remove_dead_monster(combat, monster, out, desc):
    if monster.name in out:
        out.pop(monster.name)
    desc.append(f"{monster.name} has fallen and been removed from the map.")

def toggle_monster_color(monster, new_color):
    note_dict = mapl.parse_note(monster.note)
    original_color = note_dict.get('color', 'r')
    note_dict['color'] = new_color
    new_note = ' | '.join(f"{k.title()}: {v}" for k, v in note_dict.items())
    monster.set_note(new_note)
    
    if monster.name in out:
        out[monster.name]['color'] = new_color
    
    return original_color

def process_map_absentee_monster_turn(indexed_combatant, command_list):
    title = f'New monster detected: {indexed_combatant}'
    desc_text = f'This monster is not currently on the map, please place the monster\'s token on the map manually using: ```{pref}map -t {indexed_combatant}|C4```\nReplace `C4` to any location you like.'
    command_list.append(f"""{pref}embed -title "{title}" -desc "{desc_text}" """)
    command_list.append(f'{pref}i n')



###### TEST SUITES ######


# Main code execution starts here

indexed_cname_list = []
curr_combatant = c.current

# map_url = mapl.generate_map_image(overlays)
# command_list.append(f'''{pref}embed -title "Monsters are deciding their actions..." -image "{map_url}"''')

snippets = " ".join(&ARGS&)
if inp.lower() in ('o', 'once'):
    # Implement the 'once' sub-command
    if current_init in monster_names:
        process_monster_turn(current_init, out, overlays, desc, command_list, snippets[1:])
        # Update map_state["combatants"] with 'out'
        map_state["combatants"] = out
        if overlays:
            map_url = mapl.generate_map_image(overlays)
            map_embed = f'{pref}embed -title "Updated Map" -desc "Monster movements displayed" -image "{map_url}"'
            command_list.append(map_embed)
        return command + nl.join(command_list)
    
# Build the indexed list starting from current initiative
# Sort the combatants by initiative (descending) and then by name
combatants_in_order = c.combatants
cname_list_sorted = [combatant.name for combatant in combatants_in_order]

indexed_cname_list = cname_list_sorted[cname_list_sorted.index(current_init):] + cname_list_sorted[:cname_list_sorted.index(current_init)]

if len(indexed_cname_list) > 4:
    indexed_cname_list = indexed_cname_list[:4]

current_enemy = autolib.isMonster(c.current)
for indexed_combatant in indexed_cname_list:
    if len(command_list) > 10:
        title = f'Whoa! You\'re pushing the limits of Avrae right now!'
        desc_text = f'Unfortunately, this is the maximum number of attacks you can automate to prevent unnecessarily over-stressing Avrae!\n\n**But no worries, you can simply use `{cmd}` again now to repeat the cycle!**'
        while len(command_list) > 10:
            command_list.reverse()
            last_n = command_list.index(f'{pref}i n')
            command_list = command_list[last_n+1:]
            command_list.reverse()
        command_list.append(f'{pref}i n')
        command_list.append(f"""{pref}embed -title "{title}" -desc "{desc_text}" """)
        command += nl.join(command_list)
        return command
    
    monster = c.get_combatant(indexed_combatant)    
    if monster.monster_name and not monster.get_effect('Stop Automation (auto)'):
        if autolib.isMonster(monster) != current_enemy:
            title = f'''Automation Complete! It\'s the other side's turn now! :mage:'''
            desc_text = f'Waiting on **{indexed_combatant}** to play their turn!'
            command_list.append(f"""{pref}embed -title "{title}" -desc "{desc_text}" """)
            return command + nl.join(command_list)
            
        note = mapl.parse_note(monster.note)
        if not note or not 'location' in note:
            process_map_absentee_monster_turn(indexed_combatant, command_list)
        else:
            process_monster_turn(indexed_combatant, out, overlays, desc, command_list, snippets)
            monster_team = mapl.get_combatant_team(monster.name, teams)
            toggle_monster_color(monster, team_colors.get(monster_team, 'r'))
    else: # Handle non-monster combatants
        if indexed_combatant.casefold() in ['map', 'dm', 'lair'] and c.get_combatant(indexed_combatant).init == 20:
            title = f'Automation Complete! Waiting on Lair Action :dragon:'
            desc_text = f'Use `{pref}i n` if there are no actions to take this round!'
        elif monster.get_effect('Stop Automation (auto)'):
            title = f'Automation Complete! {indexed_combatant} is pausing automation!'
            desc_text = f'Use `{pref}i n` to continue automation!'
        elif inp1.lower() in 'react':
            command_list.pop()
            title = f'Automation Complete! Pausing to allow player reaction! :mage:'
            desc_text = f'After taking any reaction use `{pref}i n`'
        else:
            title = f'Automation Complete! It\'s a player turn now! :mage:'
            desc_text = f'Waiting on **{indexed_combatant}** to play their turn!'
        command_list.append(f"""{pref}embed -title "{title}" -desc "{desc_text}" """)
        break

# Update map_state["combatants"] with 'out'
map_state["combatants"] = out

if overlays:
    map_url = mapl.generate_map_image(overlays)
    map_embed = f'{pref}embed -title "Monster Movement Summary" -desc "Monster movements so far:" -image "{map_url}"'
    command_list.append(map_embed)
return command + nl.join(command_list)
</drac2>
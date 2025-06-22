# Auto Map Monster Data Functions

c = combat()

# fmt: off
# Pre-prepared buckets for monsters based on the first letter of their name
monster_buckets = {
    'm': ["38132517-9fdc-4d90-8199-1b1c14efa134", "dff68592-2750-478a-9da0-d90f71d7ff60", "f34b0e24-c7c5-4958-b0a1-069c38ed19cf"],
    'q': ["86cd6230-162b-43a7-af64-350a65f1ba69", "f168a43a-3bd7-4f2f-9fd3-5647ee0acbc5"],
    'r': ["86cd6230-162b-43a7-af64-350a65f1ba69", "766a2982-25c7-495f-b8fa-3a3020439531"],
    'y': ["6d8cf226-8c2f-40aa-9fa8-d64a41847f11", "0c023161-c149-4485-9530-96ee05195570"],
    'z': ["6d8cf226-8c2f-40aa-9fa8-d64a41847f11"],
    'a': ["12bb091c-2db5-45bf-aaf5-4943c81ab2bf", "f49e0dfc-f28e-422c-be7e-c315b9e9c3b3", "b8217fe7-ef64-4d93-bc61-6df33f9fa3f6", "60e3c85b-7b54-4f41-a70a-d94f8da24064"],
    'i': ["e031ddab-5ecd-4fe2-98cf-dbbd6b077b1d"],
    'j': ["e031ddab-5ecd-4fe2-98cf-dbbd6b077b1d"],
    'k': ["e031ddab-5ecd-4fe2-98cf-dbbd6b077b1d", "dff68592-2750-478a-9da0-d90f71d7ff60"],
    's': ["b6a4a026-5ffb-435b-92c5-b7c8a6d3d389", "766a2982-25c7-495f-b8fa-3a3020439531", "b1d363be-bea7-4467-b213-b71b213450aa", "24554189-9fb3-474a-91eb-a4dd3606bdf9"],
    't': ["b6a4a026-5ffb-435b-92c5-b7c8a6d3d389", "5dc231e5-6af7-4350-9886-de5311f0eca1"],
    'l': ["dff68592-2750-478a-9da0-d90f71d7ff60"],
    'c': ["1e09647a-fc2a-421a-8c74-d223c80a0fd6", "120a0122-cb06-43e0-ae36-439adfc30c16", "19700ba3-51df-4e17-b3e8-c06c9d481767"],
    'd': ["147c2f03-fa4e-40ba-9572-18b4752acc7d", "120a0122-cb06-43e0-ae36-439adfc30c16", "8b186328-857c-432d-a3e8-ad486c08e62b"],
    'w': ["0c023161-c149-4485-9530-96ee05195570", "c0eb3c00-5b2d-44ea-bfc6-f37370afd945"],
    'x': ["0c023161-c149-4485-9530-96ee05195570"],
    'e': ["1ee78a97-8af6-4622-bbdb-1afda52b9eae", "8b186328-857c-432d-a3e8-ad486c08e62b"],
    'f': ["1ee78a97-8af6-4622-bbdb-1afda52b9eae", "45f6a963-9833-4437-9244-87708ae6ff0f"],
    'u': ["5dc231e5-6af7-4350-9886-de5311f0eca1"],
    'v': ["5dc231e5-6af7-4350-9886-de5311f0eca1", "c0eb3c00-5b2d-44ea-bfc6-f37370afd945"],
    'h': ["c7f6f98c-d812-43af-a1ca-2036a56c6c5e", "bd61c879-e6a7-49c1-af5b-022d7596501a"],
    'o': ["f168a43a-3bd7-4f2f-9fd3-5647ee0acbc5", "f34b0e24-c7c5-4958-b0a1-069c38ed19cf"],
    'p': ["f168a43a-3bd7-4f2f-9fd3-5647ee0acbc5"],
    'b': ["19700ba3-51df-4e17-b3e8-c06c9d481767", "6f830517-dfd1-491e-929a-a150a3adf053", "60e3c85b-7b54-4f41-a70a-d94f8da24064"],
    'g': ["45f6a963-9833-4437-9244-87708ae6ff0f", "e0d7c5e7-f53a-4c45-8589-71936d9144b9", "bd61c879-e6a7-49c1-af5b-022d7596501a"],
    'n': ["f34b0e24-c7c5-4958-b0a1-069c38ed19cf"]
}

#2025 MM
monster_buckets_2025 = {
    'a': ['27eeb980-bb4c-40aa-97a7-9a6df13f1524', '3e9963a1-eee7-4ffc-a703-3cb8290eea94'],
    'b': ['27eeb980-bb4c-40aa-97a7-9a6df13f1524'],
    'c': ['27eeb980-bb4c-40aa-97a7-9a6df13f1524', 'f50cf38b-e496-4782-b780-a0ca8490abc7'],
    'd': ['f50cf38b-e496-4782-b780-a0ca8490abc7'],
    'e': ['f50cf38b-e496-4782-b780-a0ca8490abc7'],
    'f': ['689fde77-d736-4b0a-af1e-dabe069185eb', 'f50cf38b-e496-4782-b780-a0ca8490abc7'],
    'g': ['689fde77-d736-4b0a-af1e-dabe069185eb', 'a18d8ff9-447e-47de-82db-c8c5c0acc748'],
    'h': ['a18d8ff9-447e-47de-82db-c8c5c0acc748'],
    'i': ['a18d8ff9-447e-47de-82db-c8c5c0acc748'],
    'j': ['a18d8ff9-447e-47de-82db-c8c5c0acc748'],
    'k': ['a18d8ff9-447e-47de-82db-c8c5c0acc748'],
    'l': ['a18d8ff9-447e-47de-82db-c8c5c0acc748'],
    'm': ['a18d8ff9-447e-47de-82db-c8c5c0acc748', 'a6fa567c-fc5a-40d2-a7e6-0ba302b221a1'],
    'n': ['a6fa567c-fc5a-40d2-a7e6-0ba302b221a1'],
    'o': ['a6fa567c-fc5a-40d2-a7e6-0ba302b221a1'],
    'p': ['a6fa567c-fc5a-40d2-a7e6-0ba302b221a1'],
    'q': ['a6fa567c-fc5a-40d2-a7e6-0ba302b221a1'],
    'r': ['3b9ad675-5607-4875-ba1a-7acb14cc3908', 'a6fa567c-fc5a-40d2-a7e6-0ba302b221a1'],
    's': ['3b9ad675-5607-4875-ba1a-7acb14cc3908', 'fb98d8f5-3519-4805-b8a4-b0b416473f15'],
    't': ['fb98d8f5-3519-4805-b8a4-b0b416473f15'],
    'u': ['fb98d8f5-3519-4805-b8a4-b0b416473f15'],
    'v': ['fb98d8f5-3519-4805-b8a4-b0b416473f15'],
    'w': ['fb98d8f5-3519-4805-b8a4-b0b416473f15'],
    'x': ['fb98d8f5-3519-4805-b8a4-b0b416473f15'],
    'y': ['ac575203-5c95-4813-ae1e-d68a6e78c7f7', 'fb98d8f5-3519-4805-b8a4-b0b416473f15'],
    'z': ['ac575203-5c95-4813-ae1e-d68a6e78c7f7']
}

dnd_version = ctx.guild.servsettings().version
if dnd_version == "2024":
    monster_buckets = monster_buckets_2025

override_db = load_json(get_gvar("07bc51ca-97bc-4927-bc92-3b3aea924634"))

def get_monster_data(monster_name, data_needed=None):
    if not monster_name:
        return None

    # Determine the bucket based on the first letter of the monster_name
    first_letter = monster_name[0].lower()
    if first_letter not in monster_buckets:
        return None

    # Load only the relevant databases and search for the monster directly
    relevant_gvars = monster_buckets[first_letter]
    for gvar_id in relevant_gvars:
        db = load_json(get_gvar(gvar_id))
        if monster_name in db:
            monster_data = db[monster_name]
            # If specific data is needed, return that field
            if data_needed:
                return monster_data.get(data_needed, None)
            return monster_data
    return None

def fetch_and_store_monster_data():
    monster_data = {}
    monster_names = list(set([c.monster_name for c in c.combatants if c.monster_name]))
    for monster in monster_names:
        full_data = get_monster_data(monster, None)
        if full_data:
            monster_data[monster] = full_data

    # Store the data in combat metadata
    c.set_metadata("monster_data", dump_json(monster_data))


def get_stored_monster_data(monster_name, field=None):
    monster_data = load_json(c.get_metadata("monster_data", "{}"))
    if monster_name in monster_data:
        if field:
            return monster_data[monster_name].get(field)
        return monster_data[monster_name]
    return None


def update_stored_monster_data(monster_name, data):
    monster_data = load_json(c.get_metadata("monster_data", "{}"))
    monster_data[monster_name] = data
    c.set_metadata("monster_data", dump_json(monster_data))


def remove_stored_monster_data(monster_name):
    monster_data = load_json(c.get_metadata("monster_data", "{}"))
    if monster_name in monster_data:
        del monster_data[monster_name]
        c.set_metadata("monster_data", dump_json(monster_data))


def get_monster_speed(monster_name):
    speed_data = get_stored_monster_data(monster_name, "speed")
    if not speed_data:
        return 30, "walk"  # Default if no data
    
    # Normalize the string
    data = speed_data.lower()
    
    # Remove units and extraneous spacing
    # We'll remove "ft." to simplify parsing
    data = data.replace("ft.", "").replace("ft", "")
    
    # Known speed types to look for
    speed_types = ["walk", "fly", "climb", "burrow", "swim"]
    # We'll store extracted speeds in a dictionary
    speeds = {st: 0 for st in speed_types}
    
    # We will split by commas first, as commas often separate speed entries
    parts = data.split(',')
    
    # Helper function to extract the first integer from a string
    def extract_first_int(s):
        # We'll scan character by character for digits
        digits = ""
        started = False
        for ch in s:
            if ch.isdigit():
                digits += ch
                started = True
            elif started:
                # Once we started collecting digits, if we hit a non-digit, we stop
                break
        if digits:
            return int(digits)
        return None
    
    # Process each part to find speeds
    # A part might look like "walk:40", "fly:{'number': 10, 'condition': '(hover)'}", or "burrow 30 "
    # We'll try to find known speed words in each part and extract a number
    for part in parts:
        p = part.strip()
        # Try to find which speed type this part corresponds to
        # We'll pick the first speed type keyword that appears in p
        found_type = None
        for st in speed_types:
            if st in p:
                found_type = st
                break
        
        if found_type is not None:
            # Try to extract the first integer after this type appears
            # We'll consider the substring after the speed type if possible, but let's just extract from the whole part
            val = extract_first_int(p)
            if val is not None:
                speeds[found_type] = val
    
    # If no speeds found, we might have a format without commas (like "50 ft., burrow 30 ft.")
    # We'll do a fallback: If all are zero, let's try another approach:
    if all(v == 0 for v in speeds.values()):
        # Let's split by spaces and see if we can find speed keywords inline
        words = data.replace(",", " ").split()
        # words might look like ["50", "burrow", "30"]
        # We'll scan for known speed types in words and pick the next integer after them
        for i, w in enumerate(words):
            # If this word matches a speed type or ends with it (e.g. "burrow" might appear directly)
            for st in speed_types:
                if w.startswith(st):
                    # Find next number after index i
                    # It might be in the same word or next words
                    val = extract_first_int(w)
                    if val is None:
                        # Check subsequent words for a number
                        for j in range(i+1, len(words)):
                            val = extract_first_int(words[j])
                            if val is not None:
                                break
                    if val is not None:
                        speeds[st] = val
    
    # Determine the final returned speeds
    walk_speed = speeds["walk"]
    fly_speed = speeds["fly"]
    
    # If both are 0, try picking any largest speed just in case
    if walk_speed == 0 and fly_speed == 0:
        # Check if there's any non-zero speed at all
        max_speed = max(speeds.values())
        if max_speed == 0:
            # No data found at all, return default
            return 30, "walk"
        else:
            # If we found some speed but no walk or fly, let's just treat it as walk
            return max_speed, "walk"
    
    # Return the max of walk and fly as per original function
    return (max(walk_speed, fly_speed), "fly" if fly_speed > walk_speed else "walk")


def get_monster_size(monster_name):
    if monster_name in override_db:
        parts = override_db[monster_name].split(";")
        return parts[0].split(":")[0]
    monster_data = get_stored_monster_data(monster_name)
    if monster_data:
        meta = monster_data.get("size", "")
        return meta if meta else "M"  # Default to M if not found
    return "M"


def get_aoe_attacks(monster_name):
    aoe_keywords = ["cone", "line", "radius", "sphere", "cube", "cylinder"]
    monster_attacks = []

    monster_data = get_stored_monster_data(monster_name)

    if not monster_data:
        return []

    action_fields = ["Actions", "Traits", "Legendary Actions"]
    actions_text = " ".join(monster_data.get(field, "") for field in action_fields)
    sentences = actions_text.replace("\n", " ").split(". ")

    for i, sentence in enumerate(sentences):
        sentence_lower = sentence.lower()
        if (
            any(keyword in sentence_lower for keyword in aoe_keywords)
            and "-foot" in sentence_lower
        ):
            attack_name = (
                sentences[i - 1].strip() if i > 0 else sentence.split("(")[0].strip()
            )
            size, shape, width = None, None, None
            words = sentence_lower.split()
            for j, word in enumerate(words):
                if "-foot" in word:
                    size_parts = word.split("-")
                    if size_parts[0].isdigit():
                        size = size_parts[0]
                if word in aoe_keywords:
                    shape = word
                    possible_widths = [
                        words[k] for k in range(max(0, j - 2), min(j + 4, len(words)))
                    ]
                    for item in possible_widths:
                        if item.isdigit() and (
                            words[words.index(item) + 1] in ["feet", "foot"]
                        ):
                            width = item
            if size and shape:
                attack_info = {
                    "name": attack_name,
                    "size": int(size),
                    "shape": shape,
                    "width": int(width) if width else None,
                }
                monster_attacks.append(attack_info)

    return monster_attacks

# Retrieve the multiattack text from the expanded mobl DB.
def getMonActionsFromMobl(monster_name):
    monster_data = get_monster_data(monster_name)
    if not monster_data:
        return ""
    actions = monster_data.get("actions", {})
    multiattack_text = ""
    # Look for a key that matches "Multiattack" (case-insensitive)
    for key in actions:
        if key.lower() == "multiattack":
            multiattack_text = actions[key]
            break
    return multiattack_text

# Parse the multiattack text (as returned by getMonActionsFromMobl) into a dictionary.
def getMultiAttacksFromMobl(monster_name):
    multi_atks = {}
    # Get the monster's data using the mobl module (assumes mobl.get_monster_data is available)
    monster_data = mobl.get_monster_data(monster_name)
    if not monster_data:
        return multi_atks

    actions = monster_data.get("actions", {})
    multiattack_text = ""
    # Look for a key matching "Multiattack" (case-insensitive)
    for key in actions:
        if key.lower() == "multiattack":
            multiattack_text = actions[key]
            break
    if multiattack_text == "":
        return multi_atks

    # Attempt to extract the attack segment.
    # If the text contains "attacks:" use the part after the colon, otherwise use the part after "makes "
    attack_segment = ""
    if "attacks:" in multiattack_text:
        parts = multiattack_text.split(":")
        if len(parts) > 1:
            attack_segment = parts[1].split(".")[0]
    elif "makes " in multiattack_text:
        parts = multiattack_text.split("makes ")
        if len(parts) > 1:
            attack_segment = parts[1].split(" attack")[0]
    attack_segment = attack_segment.strip()

    # Replace word numbers with digits
    num_map = {"one": "1", "two": "2", "three": "3", "four": "4",
               "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"}
    for word in num_map:
        # Replace with spaces around to avoid accidental replacements in longer words
        attack_segment = attack_segment.replace(word, num_map[word])
    # Remove extra instances of "and " to simplify parsing
    attack_segment = attack_segment.replace("and ", "")

    # The following loop looks for the pattern "X with its Y" where X is a digit and Y is an attack name.
    while " with its " in attack_segment:
        idx = attack_segment.find(" with its ")
        # Assume the digit is the last character before that phrase
        if idx >= 1:
            atk_num = attack_segment[idx-1]
        else:
            atk_num = "1"
        # Extract the attack name: take the word immediately following " with its "
        after_phrase = attack_segment[idx + len(" with its "):]
        # Use a simple split on space to get the first word as the attack name
        parts_after = after_phrase.split(" ")
        if parts_after:
            atk_name = parts_after[0]
            # Remove a trailing comma or period if present
            if atk_name.endswith(",") or atk_name.endswith("."):
                atk_name = atk_name[:-1]
            # Remove a trailing "s" if present (as in plural form)
            if atk_name.endswith("s"):
                atk_name = atk_name[:-1]
            multi_atks[atk_name.lower()] = atk_num
        # Remove the processed segment from attack_segment
        pattern = atk_num + " with its " + atk_name
        attack_segment = attack_segment.replace(pattern, "").strip()

    # If no "with its" pattern was found but there's still content, try splitting by space.
    if not multi_atks and " " in attack_segment:
        parts = attack_segment.split(" ")
        if len(parts) >= 2:
            atk_num = parts[0]
            atk_name = parts[1]
            # Clean up the attack name if needed
            if atk_name.endswith(",") or atk_name.endswith("."):
                atk_name = atk_name[:-1]
            multi_atks[atk_name.lower()] = atk_num

    # Fallback: if still no attacks were extracted, try converting the whole segment to a number.
    try:
        attacknum = int(attack_segment.strip())
        # If this works, you may decide to fall back on selecting random attacks,
        # similar to your previous logic (this code assumes you have indexed_combatant and combatants available)
        # For example:
        # x = 0
        # while x < attacknum:
        #     atk_name = autolib.getAttack(indexed_combatant, combatants)
        #     if atk_name in multi_atks:
        #         atk_num = str(int(multi_atks[atk_name]) + 1)
        #     else:
        #         atk_num = "1"
        #     multi_atks[atk_name.lower()] = atk_num
        #     x += 1
    except:
        pass

    return multi_atks
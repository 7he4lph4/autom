# Auto Map Monster Data Functions

c = combat()


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

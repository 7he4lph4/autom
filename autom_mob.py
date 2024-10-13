# Auto Map Monster Data Functions

c = combat()


def get_monster_data(monster_name, data_needed=None):
    if not monster_name:
        return None
    db1 = "21934e43-b1aa-49b5-b252-68c0d78ed04c"
    db2 = "24a1ea26-3c5b-4c2c-b528-113b857f9d34"
    db3 = "9ca349e9-96f9-499d-8a2b-1359a5b989ba"
    db4 = "48d73cd1-0224-4d8c-b723-d4a6bb4b2bf8"
    db5 = "506d5812-54b6-47d8-aa48-03b0d9436999"
    db6 = "710387e2-6c16-4b8f-9e04-65efa22a47b0"
    db7 = "f638dc80-082c-4aeb-aa03-6c8801ad9449"
    db = [db1, db2, db3, db4, db5, db6, db7]
    for gvar_str in db:
        db = load_json(get_gvar(gvar_str))
        for mon_datum in db:
            if monster_name.casefold() == mon_datum["name"].casefold():
                obtained_monster_data = (
                    mon_datum.get(data_needed, "") if data_needed else mon_datum
                )
                return obtained_monster_data
    return False


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
    speed_data = get_stored_monster_data(monster_name, "Speed")
    if speed_data:
        walk_speed, fly_speed = 0, 0
        speed_parts = speed_data.lower().replace(",", "").split()
        for i, part in enumerate(speed_parts):
            if part.isdigit():
                if i > 0 and speed_parts[i - 1] == "fly":
                    fly_speed = int(part)
                else:
                    walk_speed = int(part)
        return max(walk_speed, fly_speed), "fly" if fly_speed > walk_speed else "walk"
    return 30, "walk"  # Default speed if not found


def get_monster_size(monster_name):
    monster_data = get_stored_monster_data(monster_name)
    if monster_data:
        meta = monster_data.get("meta", "")
        return meta.split()[0] if meta else "Medium"  # Default to Medium if not found
    return "Medium"


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

# %%

import json, re

num_word = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
}

monster_data = json.load(open("monster_data_full_original.json"))
out = {}
for monster in monster_data:
    out_monster = {}

    name = monster.pop("name")
    if name in out:
        name = f"{name} ({monster['source']})"
    out_monster["name"] = name

    if "size" in monster:
        out_monster["size"] = ",".join(monster["size"])
    if "speed" in monster:
        out_monster["speed"] = ",".join(
            [f"{k}:{v}" for k, v in monster["speed"].items()]
        )

    items = list(monster.items())
    mon_keys = list(monster.keys())
    feature_remap = {
        "action": "actions",
        "bonus": "bonus_actions",
        "reaction": "reactions",
    }
    for feature, remap in feature_remap.items():
        if feature in monster:
            feature_pos = mon_keys.index(feature) + 1
            features = {}
            for f in monster[feature]:
                entry = f["entries"][0] if len([f["entries"]]) == 1 else f["entries"]
                features[f["name"]] = entry
            out_monster[remap] = features

# for monster in monster_data:
#     name = monster.pop("name")
#     if name in out:
#         name = f"{name} ({monster['source']})"
#     if "size" in monster:
#         monster["size"] = ",".join(monster["size"])
#     if "speed" in monster:
#         monster["speed"] = ",".join([f"{k}:{v}" for k, v in monster["speed"].items()])
#     if "passive" in monster:
#         monster.pop("passive")
#     if "senses" in monster:
#         monster["senses"] = ",".join(monster["senses"])
#     if "attachedItems" in monster:
#         monster["attachedItems"] = ",".join(monster["attachedItems"])

#     monster = {
#         k: v
#         for k, v in monster.items()
#         if ("Tags" not in k)
#         and k
#         not in ["str", "dex", "con", "int", "wis", "cha"]
#         + ["srd", "basicRules", "isNamedCreature", "source", "page", "otherSources"]
#         + ["type", "alignment", "alignmentPrefix", "ac", "hp", "save", "skill", "cr"]
#         + ["resist", "immune", "conditionImmune", "vulnerable", "environment"]
#         + ["group", "languages", "legendaryGroup", "variant", "_versions"]
#         + ["conditionInflict", "conditionInflictSpell", "conditionInflictLegendary"]
#         + ["savingThrowForced", "savingThrowForcedSpell", "savingThrowForcedLegendary"]
#         + ["altArt", "soundClip", "hasToken", "token", "hasFluff", "hasFluffImages"]
#     }
#     """if "source" and "page" in monster:
#         monster["source"] = f"{monster['source']}:{monster.pop('page')}"
#     if "otherSources" in monster:
#         monster["otherSources"] = ",".join(
#             [s["source"] for s in monster["otherSources"]]
#         )
#     if "type" in monster:
#         if "tags" in monster["type"] and type(monster["type"]["tags"][0]) == str:
#             tags = ",".join(monster["type"]["tags"])
#             monster["type"] = f"{monster['type']['type']}:{tags}"
#     if "alignment" in monster and type(monster["alignment"][0]) == str:
#         monster["alignment"] = "".join(monster["alignment"])
#     if "ac" in monster:
#         monster["ac"] = "".join(map(str, monster["ac"]))
#     if "hp" in monster:
#         if "formula" in monster["hp"]:
#             monster["hp"] = "".join(monster["hp"]["formula"]).replace(" ", "")
#     if "save" in monster:
#         monster["save"] = ",".join([f"{k}:{v}" for k, v in monster["save"].items()])
#     if "resist" in monster:
#         monster["resist"] = ",".join([str(r) for r in monster["resist"]])
#     if "immune" in monster:
#         monster["immune"] = ",".join([str(i) for i in monster["immune"]])
#     if "conditionImmune" in monster:
#         monster["conditionImmune"] = ",".join(
#             [str(i) for i in monster["conditionImmune"]]
#         )
#     if "vulnerable" in monster:
#         monster["vulnerable"] = ",".join([str(v) for v in monster["vulnerable"]])

#     if "languages" in monster:
#         monster["languages"] = ",".join(monster["languages"])
#     if "environment" in monster:
#         monster["environment"] = ",".join(monster["environment"])"""

#     items = list(monster.items())
#     mon_keys = list(monster.keys())
#     feature_remap = {
#         "trait": "traits",
#         "action": "actions",
#         "bonus": "bonus_actions",
#         "reaction": "reactions",
#         "legendary": "legendary_actions",
#     }
#     for feature, remap in feature_remap.items():
#         if feature in monster:
#             feature_pos = mon_keys.index(feature) + 1
#             features = {}
#             for f in monster[feature]:
#                 entry = f["entries"][0] if len([f["entries"]]) == 1 else f["entries"]
#                 features[f["name"]] = entry
#             items.insert(feature_pos, (remap, features))
#     monster = dict(items)

#     if "actions" in monster:
#         for a, action in monster["actions"].items():
#             # fmt: off
#             arange = (
#                 "mw" if "{@atk mw}" in action else
#                 "rw" if "{@atk rw}" in action else
#                 "mrw" if "{@atk mw,rw}" in action else
#                 "ms" if "{@atk sw}" in action else
#                 "rs" if "{@atk rs}" in action else
#                 "mrs" if "{@atk ms,rs}" in action else ""
#             )
#             # fmt: on
#             if "{@atk mw}" in action:
#                 monster["actions"][a] = action.replace("{@atk mw} ", "mw;")
#     #     if "Multiattack" in monster["actions"]:
#     #         monster["actions"]["multiattack"] = monster["actions"]["Multiattack"].re

#     if "traits" in monster:
#         discard_traits = [
#             "Limited Telepathy",
#             "Malison Type",
#             "Mimicry",
#             "Probing Telepathy",
#             "Psychic Defense",
#             "Rejuvenation",
#             "The Colors of Age",
#             "Unarmored Defense",
#             "Unusual Nature",
#         ]
#         for trait in discard_traits:
#             if trait in monster["traits"]:
#                 monster["traits"].pop(trait)
#         combined_traits = ["Hold Breath", "Magic Resistance", "Spider Climb"]
#         if all(t in combined_traits for t in monster["traits"]):
#             monster["traits"] = ",".join(list(monster["traits"].keys()))
#         """else:
#             for t in combined_traits:
#                 if t in monster["traits"]:
#                     monster["traits"][t] = """ ""

#     if "spellcasting" in monster:
#         for spellcasting in monster["spellcasting"]:
#             spells = spellcasting.get("spells", {})
#             for level, lspells in spells.items():
#                 if "spells" in lspells:
#                     for i, s in enumerate(lspells["spells"]):
#                         lspells["spells"][i] = s.replace("{@spell ", "").replace(
#                             "}", ""
#                         )
#                     lspells["spells"] = ",".join(lspells["spells"])
#                     if "slots" in lspells:
#                         lspells["spells"] = f"{lspells['slots']}:{lspells['spells']}"
#                     spells[level] = lspells["spells"]
#             daily = spellcasting.get("daily", {})
#             for frequency, fspells in daily.items():
#                 for i, s in enumerate(fspells):
#                     if type(s) == dict:
#                         s = s["entry"]
#                     fspells[i] = s.replace("{@spell ", "").replace("}", "")
#                 daily[frequency] = ",".join(fspells)
#             will = spellcasting.get("will", [])
#             if will:
#                 for i, s in enumerate(will):
#                     if type(s) == dict:
#                         s = s["entry"]
#                     will[i] = s.replace("{@spell ", "").replace("}", "")
#                 spellcasting["will"] = ",".join(will)
#             if "displayAs" in spellcasting:
#                 spellcasting.pop("displayAs")
#             if "hidden" in spellcasting:
#                 spellcasting.pop("hidden")

#     monster = {
#         k: v for k, v in monster.items() if k not in (list(feature_remap.keys()))
#     }

#     print(name)
#     if name in out:
#         name = f"{name} ({monster['source']})"
#     out[name] = monster

json.dump(out, open("standard_processed.json", "w"))

"""stats_pos = list(monster.keys()).index("str")
stats = ["str", "dex", "con", "int", "wis", "cha"]
stats_str = ",".join([f"{k}:{monster[k]}" for k in stats])
items.insert(stats_pos, ("stats", stats_str))

if "skill" in monster:
    skills_pos = mon_keys.index("skill") + 1
    skills_str = ",".join([f"{k}:{v}" for k, v in monster["skill"].items()])
    skills_str = skills_str.replace("+", "")
    items.insert(skills_pos, ("skills", skills_str))"""

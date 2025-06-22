# Auto Map Targeting Functions

using(autolib="ec14bc6e-81e4-4df7-86e9-5d64ed2fa9b7")
c = combat()

party = []
monsters, dead_monsters = [], []

if c:
    for co in c.combatants:
        if not co.hp or co.name.lower() in ["dm", "map", "lair"]:
            continue
        if 0 < co.hp:
            (monsters if autolib.isMonster(co) else party).append(co)
        elif autolib.isMonster(co):
            dead_monsters.append(co)


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

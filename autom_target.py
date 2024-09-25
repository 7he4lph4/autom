# Auto Map Targeting Functions

using(autolib="ec14bc6e-81e4-4df7-86e9-5d64ed2fa9b7")
c = combat()


def get_target_lists(targs={}):
    master_list = [
        co
        for co in c.combatants
        if co.name.lower() not in ["dm", "map", "lair"]
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

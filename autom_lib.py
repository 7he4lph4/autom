# autolib
# Additional functions to support the !auto alias
#
# Constants

ALLY_EFFECT = "Ally (auto)"
GHOST_EFFECT = "Ghost (auto)"
TARGET_ADV = [
    "Attacked Recklessly",
    "Restrained",
    "Prone",
    "Blinded",
    "Paralyzed",
    "Petrified",
    "Stunned",
    "Unconscious",
]
TARGET_DIS = ["Invisible", "Dodge", "Blur"]
MONSTER_ADV = ["Invisible"]
MONSTER_DIS = ["Restrained", "Prone", "Blinded", "Frightened", "Poisoned"]


# Find any groups in the combat and see if there are any monster groups. If so return True which will be used to avoid automating groups the wrong way
def hasMonsterGroup(c):
    monsterg = False
    if c.groups:
        for g in c.groups:
            grouphaschar = False
            for cbt in g.combatants:
                if not cbt.monster_name:
                    grouphaschar = True
                    break
            if not grouphaschar:
                monsterg = True
    return monsterg


# Check if a monster is disabled - i.e. has an effect that prevents it from taking actions
def isDisabled(c, indexed_combatant):
    disabled = False
    cbt = c.get_combatant(indexed_combatant)
    if cbt:
        # 		if cbt.get_effect("Incapacitated") or cbt.get_effect("Paralyzed") or cbt.get_effect("Petrified") or cbt.get_effect("Stunned") or cbt.get_effect("Unconscious") or cbt.get_effect("Hypnotic Pattern"):
        if (
            cbt.get_effect("Incapacitated")
            or cbt.get_effect("Paralyzed")
            or cbt.get_effect("Petrified")
            or cbt.get_effect("Stunned")
            or cbt.get_effect("Unconscious")
        ):

            disabled = True
    return disabled


# Apply ally status - marks a familar or pet as an ally
def setAllies(c, allylist):
    if c and allylist and len(allylist) > 0:
        for x in allylist:
            cbt = c.get_combatant(x)
            if cbt:
                if not cbt.get_effect(ALLY_EFFECT):
                    cbt.add_effect(ALLY_EFFECT)


# Apply ghost status - marks a combat as insubstantial or absent so cannot be attacked
# This method will toggle the status on or off.
def setGhost(c, ghostlist):
    if c and ghostlist and len(ghostlist) > 0:
        for x in ghostlist:
            cbt = c.get_combatant(x)
            if cbt:
                if cbt.get_effect(GHOST_EFFECT):
                    cbt.remove_effect(GHOST_EFFECT)
                else:
                    cbt.add_effect(GHOST_EFFECT)


# Remove allies from the monster list. Note that due to the sequence of processing this effectively adds them to the target list. Which is what we want
def isMonster(cbt):
    if cbt:
        if cbt.monster_name and not cbt.get_effect(ALLY_EFFECT):
            return True
    return False


# Remove ghosted entries from the target list
def isGhost(c, name):
    cbt = c.get_combatant(name)
    if cbt:
        if cbt.get_effect(GHOST_EFFECT):
            return True
    return False


# Generate a list of advantage and disadvantage due to target status - we need at most one of each so will break after generating one.
def resolveTargetAdv(cbt):
    advdis = " "
    for i in cbt.effects:
        for x in TARGET_ADV:
            if x.lower() in i.name.lower():
                advdis += "adv "
                break
        for y in TARGET_DIS:
            if y.lower() in i.name.lower():
                advdis += "dis "
                break
    return advdis


# Generate a list of advantage and disadvantage due to monster status - we need at most one of each so will break after generating one.
def resolveMonsterAdv(cbt):
    advdis = " "
    for i in cbt.effects:
        for x in MONSTER_ADV:
            if x.lower() in i.name.lower():
                advdis += "adv "
                break
        for y in MONSTER_DIS:
            if y.lower() in i.name.lower():
                advdis += "dis "
                break
    return advdis


# Resolve weapons as 2H if they are versatile
def resolveVersatile(attackstring):
    if attackstring.lower() in [
        "longsword",
        "spear",
        "quarterstaff",
        "battleaxe",
        "trident",
        "warhammer",
    ]:
        attackstring += " (2H)"
    return attackstring


# Read an attack from the init entry
def getAttack(indexed_combatant, combatants):
    atks = []
    for combatant in combatants:
        if combatant.name == indexed_combatant:
            atks = list(combatant.attacks)
            break
    filteratks = [x for x in atks if not x.activation_type]
    atks = filteratks if filteratks else atks
    chosen_atk = str(atks[randint(len(atks))])
    chosen_atk_string = str(chosen_atk).split(":")[0][2:-2].casefold()
    if "Action:" in chosen_atk:
        chosen_atk_string = chosen_atk.split(":")[1:-2][0][:-2]
    chosen_atk_string = resolveVersatile(chosen_atk_string)
    return chosen_atk_string


# Check if the monster has Relentless
def onDeath(indexed_combatant, combatants):
    onDeath = ""
    atks = ""
    cbt = ""
    for combatant in combatants:
        if combatant.name == indexed_combatant:
            atks = str(combatant.attacks)
            cbt = combatant
            break
    if "relentless" in atks.lower():
        if not cbt.get_effect("relentless"):
            onDeath = "relentless"
    elif "death burst" in atks.lower():
        onDeath = "death burst"
    return onDeath


# Build up the monster db
def buildDB():
    db1 = "21934e43-b1aa-49b5-b252-68c0d78ed04c"
    db2 = "24a1ea26-3c5b-4c2c-b528-113b857f9d34"
    db3 = "9ca349e9-96f9-499d-8a2b-1359a5b989ba"
    db4 = "48d73cd1-0224-4d8c-b723-d4a6bb4b2bf8"
    db5 = "506d5812-54b6-47d8-aa48-03b0d9436999"
    db6 = "710387e2-6c16-4b8f-9e04-65efa22a47b0"
    db7 = "f638dc80-082c-4aeb-aa03-6c8801ad9449"
    db = [db1, db2, db3, db4, db5, db6, db7]
    return db


# Read through the monster db to see if we have data for the monster
def getActions(monst_name, db):
    for gvar_str in db:
        db = load_json(get_gvar(gvar_str))
        for mon_datum in db:
            if monst_name.casefold() == mon_datum["name"].casefold():
                return mon_datum["Actions"]
    return ""


# Parse the monster data for multi-attacks
def getMultiAttacks(mon_actions):
    multi_atks = {}
    if "Multiattack" in mon_actions:
        multiattack = True
        if "attacks:" in mon_actions:
            attack_segment = mon_actions.split(":")[1].split(".")[0]
        else:
            attack_segment = mon_actions.split("makes ")[1].split(" attacks")[0].strip()
        # Computing multi-attacks
        remaining_atk_string = (
            attack_segment.replace("one", "1")
            .replace("two", "2")
            .replace("three", "3")
            .replace("four", "4")
            .replace("five", "5")
            .replace("six", "6")
            .replace("seven", "7")
            .replace("and ", "")
        )
        while " with its " in remaining_atk_string:
            atk_name = (
                remaining_atk_string.split(" with its ")[1]
                .split(",")[0]
                .split(" ")[0]
                .split(".")[0]
            )
            atk_num = remaining_atk_string.split(" with its ")[0][-1]
            remaining_atk_string = remaining_atk_string.replace(
                f"{atk_num} with its {atk_name}", ""
            ).strip()
            atk_name = atk_name[:-1] if atk_name.endswith("s") else atk_name
            multi_atks.update({atk_name: atk_num})

        if (
            not " with its " in remaining_atk_string
            and not multi_atks
            and " " in remaining_atk_string
        ):
            atk_num, atk_name = (
                remaining_atk_string.split(" ")[0],
                remaining_atk_string.split(" ")[1],
            )
            multi_atks.update({atk_name: atk_num})
        if not multi_atks:
            try:
                attacknum = int(remaining_atk_string)
                x = 0
                while x < attacknum:
                    atk_name = autolib.getAttack(indexed_combatant, combatants)
                    if atk_name in multi_atks:
                        atk_num = str(int(multi_atks[atk_name]) + 1)
                    else:
                        atk_num = "1"

                    multi_atks.update({atk_name: atk_num})
                    x += 1
            except:
                multiattack = False

    return multi_atks

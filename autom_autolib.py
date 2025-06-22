# autolib
# Additional functions to support the !auto alias
#
# Constants

ALLY_EFFECT = "Ally (auto)"
GHOST_EFFECT = "Ghost (auto)"
TARGET_ADV = ["Attacked Recklessly","Restrained","Prone","Blinded","Paralyzed","Petrified","Stunned","Unconscious"]
TARGET_DIS = ["Invisible","Dodge","Blur"]
MONSTER_ADV = ["Invisible"]
MONSTER_DIS = ["Restrained","Prone","Blinded","Frightened","Poisoned"]

# Find any groups in the combat and see if there are any monster groups. If so return True which will be used to avoid automating groups the wrong way
def hasMonsterGroup(c) :
    monsterg = False
    if c.groups :
        for g in c.groups :
            grouphaschar = False
            for cbt in g.combatants :
                if not cbt.monster_name :
                    grouphaschar = True
                    break
            if not grouphaschar:
                monsterg = True
    return monsterg

# Check if a monster is disabled - i.e. has an effect that prevents it from taking actions
def isDisabled(c, indexed_combatant) :
    disabled = False
    cbt = c.get_combatant(indexed_combatant)
    if cbt :
        if cbt.get_effect("Incapacitated") or cbt.get_effect("Paralyzed") or cbt.get_effect("Petrified") or cbt.get_effect("Stunned") or cbt.get_effect("Unconscious"):
            disabled = True
    return disabled
    
# Apply ally status - marks a familar or pet as an ally
def setAllies(c, allylist) :
    if c and allylist and len(allylist) > 0 :
        for x in allylist :
            cbt = c.get_combatant(x)
            if cbt :
                if not cbt.get_effect(ALLY_EFFECT):
                    cbt.add_effect(ALLY_EFFECT)
                    
# Apply ghost status - marks a combat as insubstantial or absent so cannot be attacked
# This method will toggle the status on or off.
def setGhost(c, ghostlist) :
    if c and ghostlist and len(ghostlist) > 0 :
        for x in ghostlist :
            cbt = c.get_combatant(x)
            if cbt :
                if cbt.get_effect(GHOST_EFFECT):
                    cbt.remove_effect(GHOST_EFFECT)
                else:
                    cbt.add_effect(GHOST_EFFECT)
                    
# Remove allies from the monster list. Note that due to the sequence of processing this effectively adds them to the target list. Which is what we want
def isMonster(cbt) :
    if cbt :
        if cbt.monster_name and not cbt.get_effect(ALLY_EFFECT):
            return True
    return False
    
# Remove ghosted entries from the target list
def isGhost(c,name) :
    cbt = c.get_combatant(name)
    if cbt :
        if cbt.get_effect(GHOST_EFFECT):
            return True
    return False

# Generate a list of advantage and disadvantage due to target status - we need at most one of each so will break after generating one.
def resolveTargetAdv(cbt) :
    advdis = " "
    for i in cbt.effects :
        for x in TARGET_ADV :
            if x.lower() in i.name.lower() :
                advdis += "adv "
                break
        for y in TARGET_DIS :
            if y.lower() in i.name.lower() :
                advdis += "dis "
                break
    return advdis
    
# Generate a list of advantage and disadvantage due to monster status - we need at most one of each so will break after generating one.
def resolveMonsterAdv(cbt) :
    advdis = " "
    for i in cbt.effects :
        for x in MONSTER_ADV :
            if x.lower() in i.name.lower() :
                advdis += "adv "
                break
        for y in MONSTER_DIS :
            if y.lower() in i.name.lower() :
                advdis += "dis "
                break
    return advdis
    
# Resolve weapons as 2H if they are versatile
def resolveVersatile(attackstring) :
    if attackstring.lower() in ["longsword", "spear", "quarterstaff", "battleaxe", "trident", "warhammer"] :
        attackstring += " (2H)"
    return attackstring
    
# Read an attack from the init entry
def getAttack(indexed_combatant,combatants) :
    atks = []
    for combatant in combatants:
        if combatant.name == indexed_combatant:
            atks = list(combatant.attacks)
            break
    filteratks = [x for x in atks if not x.activation_type]
    atks = filteratks if filteratks else atks
    chosen_atk = str(atks[randint(len(atks))])
    chosen_atk_string = str(chosen_atk).split(':')[0][2:-2].casefold()
    if 'Action:' in chosen_atk:
        chosen_atk_string = chosen_atk.split(':')[1:-2][0][:-2]
    chosen_atk_string = resolveVersatile(chosen_atk_string)
    return chosen_atk_string

#Get melee attack 
def getMeleeAttack(indexed_combatant, combatants):
    # Locate the specified combatant and their attacks
    atks = []
    for combatant in combatants:
        if combatant.name == indexed_combatant:
            atks = list(combatant.attacks)
            break
    
    # If no combatant found or no attacks, return None or handle gracefully
    if not atks:
        return None

    # Filter attacks by removing those that have an activation_type (if any)
    filtered_atks = [atk for atk in atks if not atk.activation_type]
    atks = filtered_atks if filtered_atks else atks

    def getAttackText(attack):
        """Extract the text from the attack's automation entries."""
        for entry in attack.raw.get('automation', []):
            if entry.get('type') == 'text' and 'text' in entry:
                return entry['text']
        return ''

    # Separate melee and ranged attacks by checking their descriptive text
    melee_attacks = [atk for atk in atks if "Melee" in getAttackText(atk)]
    ranged_attacks = [atk for atk in atks if "Ranged" in getAttackText(atk)]

    # Choose the appropriate attack
    if melee_attacks:
        chosen_atk = melee_attacks[randint(len(melee_attacks))]
    elif ranged_attacks:
        chosen_atk = ranged_attacks[randint(len(ranged_attacks))]
        chosen_atk = str(chosen_atk) + " dis"  # Add disadvantage indicator
    else:
        # If no clear melee/ranged found, just pick one at random
        chosen_atk = atks[randint(len(atks))]

    chosen_atk = str(chosen_atk)
    # Process chosen_atk_string if needed:
    chosen_atk_string = chosen_atk.split(':')[0][2:-2].casefold()
    if 'Action:' in chosen_atk:
        parts = chosen_atk.split(':')
        if len(parts) > 2:
            chosen_atk_string = parts[1:-2][0][:-2]

    chosen_atk_string = resolveVersatile(chosen_atk_string)
    return chosen_atk_string

# Check if the monster has Relentless
def onDeath(indexed_combatant,combatants) :
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
    db1 = '21934e43-b1aa-49b5-b252-68c0d78ed04c'
    db2 = '24a1ea26-3c5b-4c2c-b528-113b857f9d34'
    db3 = '9ca349e9-96f9-499d-8a2b-1359a5b989ba'
    db4 = '48d73cd1-0224-4d8c-b723-d4a6bb4b2bf8'
    db5 = '506d5812-54b6-47d8-aa48-03b0d9436999'
    db6 = '710387e2-6c16-4b8f-9e04-65efa22a47b0'
    db7 = 'f638dc80-082c-4aeb-aa03-6c8801ad9449'
    db = [db1,db2,db3,db4,db5,db6,db7]
    return db

# Read through the monster db to see if we have data for the monster
def getActions(monst_name, db) :
    for gvar_str in db:
        db = load_json(get_gvar(gvar_str))
        for mon_datum in db:
            if monst_name.casefold() == mon_datum["name"].casefold():
                return mon_datum["Actions"]
    return ""

# Improved version detection with better scoring
def detectMonsterVersion(monster_name, combat):
    """Detects whether a monster uses 2014 or 2025 format based on attack matching"""
    
    # Check servsettings first, code after this return is for a later feature
    override_version = ctx.guild.servsettings().version
    if override_version in ["2014", "2024", "2025"]:
        return override_version
    
    # Get the actual monster from combat to check attacks
    monster = None
    for c in combat.combatants:
        if c.monster_name and c.monster_name == monster_name:
            monster = c
            break
    
    # Load both GVARs
    multi_db_2014 = load_yaml(get_gvar("cae35870-4768-4f1b-9162-099de3659e6c"))
    multi_db_2025 = load_yaml(get_gvar("715b5fb1-c765-4212-add6-71cf61403ef5"))
    
    # Direct O(1) lookup
    exists_2014 = monster_name in multi_db_2014
    exists_2025 = monster_name in multi_db_2025
    
    # If only exists in one GVAR, return that version
    if exists_2014 and not exists_2025:
        return "2014"
    elif exists_2025 and not exists_2014:
        return "2025"
    
    # If doesn't exist in either or no monster attacks to check
    if not (exists_2014 or exists_2025) or not monster or not monster.attacks:
        return "2025"  # Default to 2025
    
    # Get attacks from both versions and normalize them
    def normalize_attack_name(name):
        """Normalize attack names for better matching"""
        # Remove common suffixes and prefixes
        name = name.lower().strip()
        # Remove parenthetical info
        if '(' in name:
            name = name.split('(')[0].strip()
        # Remove common attack descriptors
        for suffix in [' attack', ' weapon', ' spell', ' (2h)', ' 2h']:
            if name.endswith(suffix):
                name = name[:-len(suffix)].strip()
        return name
    
    attacks_2014 = set()
    attacks_2025 = set()
    
    if exists_2014:
        atkdata = multi_db_2014[monster_name]
        for entry in atkdata:
            names = entry["name"]
            if typeof(names) == 'str':
                attacks_2014.add(normalize_attack_name(names))
            else:
                for n in names:
                    attacks_2014.add(normalize_attack_name(n))
    
    if exists_2025:
        atkdata = multi_db_2025[monster_name]
        # Get base attacks
        base_attacks = atkdata.get("base_attacks", {})
        for atk in base_attacks.keys():
            attacks_2025.add(normalize_attack_name(atk))
        # Get possible substitutions
        can_replace = atkdata.get("can_replace", [])
        for sub_rule in can_replace:
            replace_options = sub_rule.get("to", [])
            for opt in replace_options:
                attacks_2025.add(normalize_attack_name(opt))
    
    # Score each version based on matches
    monster_attacks = [normalize_attack_name(atk.name) for atk in monster.attacks if atk.name.lower() != "multiattack"]
    
    score_2014 = 0
    score_2025 = 0
    
    # Count exact matches more heavily
    for matk in monster_attacks:
        if matk in attacks_2014:
            score_2014 += 3
        elif any(matk in a2014 or a2014 in matk for a2014 in attacks_2014):
            score_2014 += 1
            
        if matk in attacks_2025:
            score_2025 += 3
        elif any(matk in a2025 or a2025 in matk for a2025 in attacks_2025):
            score_2025 += 1
    
    # Normalize scores by number of attacks to avoid bias
    if len(attacks_2014) > 0:
        score_2014 = score_2014 / len(attacks_2014)
    if len(attacks_2025) > 0:
        score_2025 = score_2025 / len(attacks_2025)
    
    # Return version with higher normalized score
    if score_2014 > score_2025 * 1.2:  # Slight bias towards 2025 to prevent false 2014 detections
        return "2014"
    else:
        return "2025"

# Parse the monster data for multi-attacks - now with version detection
def getMultiAttacks(monster_name, combat=None):
    """Get multiattack data for a monster, auto-detecting version if combat provided"""
    
    # Detect version if combat object provided
    if combat:
        version = detectMonsterVersion(monster_name, combat)
    else:
        # Fall back to svar or default
        version = get_svar("autoVersion", "2025")
    
    if version == "2014":
        return getMultiAttacks2014(monster_name)
    else:
        return getMultiAttacks2025(monster_name)

def getMultiAttacks2014(monster_name):
    """Get multiattack data for 2014 format monsters"""
    multi_db = load_yaml(get_gvar("cae35870-4768-4f1b-9162-099de3659e6c"))
    
    # Direct O(1) lookup
    if monster_name not in multi_db:
        return {}
        
    atkdata = multi_db[monster_name]
    multi = {}
    
    for entry in atkdata:
        count = entry["count"]
        typ = entry.get("type", "")
        names = entry["name"]
        
        if typeof(names) == 'str':
            names = [names]
            
        if typ == "or":
            # Pick one of the options randomly
            pick = names[roll("1d" + str(len(names))) - 1]
            if pick in multi:
                multi[pick] = str(int(multi[pick]) + count)
            else:
                multi[pick] = str(count)
        else:
            # Add all attacks
            for name in names:
                if name in multi:
                    multi[name] = str(int(multi[name]) + count)
                else:
                    multi[name] = str(count)
    
    return multi

def getMultiAttacks2025(monster_name):
    """Get multiattack data for 2025 format monsters"""
    multi_db = load_yaml(get_gvar("715b5fb1-c765-4212-add6-71cf61403ef5"))
    
    # Direct O(1) lookup
    if monster_name not in multi_db:
        return {}
        
    atkdata = multi_db[monster_name]
    multi = {}
    
    # Add base attacks
    base_attacks = atkdata.get("base_attacks", {})
    for atk_name, count in base_attacks.items():
        multi[atk_name] = str(count)
    
    # Handle substitutions
    can_replace = atkdata.get("can_replace", [])
    if can_replace:
        # For each substitution rule
        for sub_rule in can_replace:
            replace_from = sub_rule.get("from", "any")
            replace_count = sub_rule.get("count", 1)
            replace_options = sub_rule.get("to", [])
            
            if replace_options:
                # Roll to see if substitution happens (50% chance by default)
                if roll("1d2") == 2:
                    # Pick a random substitution option
                    chosen = replace_options[roll("1d" + str(len(replace_options))) - 1]
                    
                    # Apply substitution
                    if replace_from == "any":
                        # Replace from any attack that has count >= replace_count
                        replaced = False
                        for atk in list(multi.keys()):
                            if int(multi[atk]) >= replace_count:
                                multi[atk] = str(int(multi[atk]) - replace_count)
                                if multi[atk] == "0":
                                    multi.pop(atk)
                                replaced = True
                                break
                        
                        # Only add the substitution if we successfully removed attacks
                        if replaced:
                            if chosen in multi:
                                multi[chosen] = str(int(multi[chosen]) + replace_count)
                            else:
                                multi[chosen] = str(replace_count)
                    else:
                        # Replace from specific attack
                        if replace_from in multi and int(multi[replace_from]) >= replace_count:
                            multi[replace_from] = str(int(multi[replace_from]) - replace_count)
                            if multi[replace_from] == "0":
                                multi.pop(replace_from)
                            
                            # Add the substituted attack
                            if chosen in multi:
                                multi[chosen] = str(int(multi[chosen]) + replace_count)
                            else:
                                multi[chosen] = str(replace_count)
    
    return multi

# Helper function to check if a specific attack can multiattack
def canMultiattack(monster_name, attack_name, combat=None):
    """Check if a specific attack can be used in multiattack"""
    multi_attacks = getMultiAttacks(monster_name, combat)
    
    if not multi_attacks:
        return False, 0
    
    # Normalize the attack name for comparison
    attack_lower = attack_name.lower()
    
    for multi_atk, count in multi_attacks.items():
        if multi_atk.lower() in attack_lower or attack_lower in multi_atk.lower():
            return True, int(count)
    
    return False, 0
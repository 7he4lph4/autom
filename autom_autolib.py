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
#		if cbt.get_effect("Incapacitated") or cbt.get_effect("Paralyzed") or cbt.get_effect("Petrified") or cbt.get_effect("Stunned") or cbt.get_effect("Unconscious") or cbt.get_effect("Hypnotic Pattern"):
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

# Read through the monster db to see if we have data for the monster
def getActions(monster_name):
    monster_data = get_monster_data(monster_name)
    if monster_data:
        actions_dict = monster_data.get('actions', {})
        return actions_dict
    else:
        return None

# Parse the monster data for multi-attacks
def replace_number_words(text):
    number_words = {
        'zero': '0',
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9',
        'ten': '10',
    }
    words = text.split()
    new_words = []
    for word in words:
        word_clean = word.strip('.,').lower()
        if word_clean in number_words:
            new_word = number_words[word_clean]
            # Preserve any punctuation
            if word.endswith('.'):
                new_word += '.'
            elif word.endswith(','):
                new_word += ','
            new_words.append(new_word)
        else:
            new_words.append(word)
    return ' '.join(new_words)

def is_attack_action(action_name, actions_dict):
    action_desc = actions_dict[action_name]
    # Check if the action description indicates an attack
    if '@atk' in action_desc or 'Melee Weapon Attack' in action_desc or 'Ranged Weapon Attack' in action_desc:
        return True
    else:
        return False

def getMultiAttacks(actions_dict):
    multi_atks = {}
    # Find the 'Multiattack' action
    multiattack_text = None
    for key in actions_dict:
        if 'Multiattack' in key:
            multiattack_text = actions_dict[key]
            break

    if not multiattack_text:
        return multi_atks  # Empty dict

    # Replace number words with digits
    multiattack_text = replace_number_words(multiattack_text)

    # Remove any text before 'makes'
    makes_index = multiattack_text.find('makes')
    if makes_index != -1:
        after_makes = multiattack_text[makes_index + len('makes'):].strip()
    else:
        after_makes = multiattack_text.strip()
    
    # Check for colon indicating further attack details
    colon_index = after_makes.find(':')
    if colon_index != -1:
        attack_details = after_makes[colon_index+1:].strip()
    else:
        attack_details = after_makes

    # Split the attack details into parts
    separators = [' and ', '; ', ', ', '. ']
    for sep in separators:
        if sep in attack_details:
            attack_parts = attack_details.split(sep)
            break
    else:
        attack_parts = [attack_details]

    for part in attack_parts:
        part = part.strip()
        # Replace 'and' with '' to simplify parsing
        part = part.replace(' and ', ' ')
        words = part.split()
        num = None
        attack_name = None

        # Attempt to find 'X with its AttackName' pattern
        if 'with its' in part or 'with their' in part:
            words = part.replace('with its', 'with').replace('with their', 'with').split()
            if words[0].isdigit() and 'with' in words:
                num = int(words[0])
                with_index = words.index('with')
                if with_index + 1 < len(words):
                    attack_name = words[with_index + 1].strip('.,')
        else:
            # Attempt to find 'X AttackName' pattern
            if words[0].isdigit() and len(words) > 1:
                num = int(words[0])
                attack_name = words[1].strip('.,')
            elif len(words) >= 2 and words[1].isdigit():
                num = int(words[1])
                attack_name = words[0].strip('.,')
            else:
                # Handle 'The dragon can use its Lightning Breath' case
                if 'can use' in part:
                    words = part.split()
                    use_index = words.index('use')
                    if use_index + 1 < len(words):
                        attack_name = words[use_index + 1].strip('.,')
                        num = 1

        if num and attack_name:
            attack_name = attack_name.rstrip('s').capitalize()
            # Update attack count, combining if necessary
            if attack_name in multi_atks:
                multi_atks[attack_name] += num
            else:
                multi_atks[attack_name] = num

    # If multi_atks is still empty, distribute attacks among available attack actions
    if not multi_atks:
        words = after_makes.split()
        if words[0].isdigit():
            num_attacks = int(words[0])
            # Get all attack actions excluding 'Multiattack'
            attack_names = [name for name in actions_dict if 'Multiattack' not in name and is_attack_action(name, actions_dict)]
            if attack_names:
                for i in range(num_attacks):
                    atk_name = attack_names[i % len(attack_names)]
                    if atk_name in multi_atks:
                        multi_atks[atk_name] += 1
                    else:
                        multi_atks[atk_name] = 1
    return multi_atks

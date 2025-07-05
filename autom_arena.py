<drac2>
#arena
# Epic Arena Battle System with Refined Betting

pref, al = ctx.prefix, ctx.alias
cmd = pref + al
args = &ARGS&
c = combat()
nl = '\n'
char = character()

# Import required libraries
using(
    autolib="b02daf2d-7cfc-4b0c-8fd2-f7be253e8f13",
    core = "49f5f503-1c00-4f24-ba43-92e65c2c2fb6",
)

# Load monster data from hunt system
def load_monster_data():
    """Load monster data from hunt system GVARs"""
    monster_yaml1 = get_gvar("cabb59f1-a0c5-4b6d-80b8-71560d2ac3fc")
    monster_yaml2 = get_gvar("873e4047-cb10-4928-ba07-a7e1631d7b2d")
    monster_data = load_yaml(monster_yaml1 + monster_yaml2)
    return monster_data

def preprocess_monster_data(monster_data):
    """Pre-process monster data into indexed categories to avoid repeated filtering"""
    if not monster_data or 'header' not in monster_data or 'data' not in monster_data:
        return {}
    
    header = monster_data['header']
    try:
        name_idx = header.index('Creature')
        xp_idx = header.index('XP')
        type_idx = header.index('Type')
        biome1_idx = header.index('Biome1')
        biome2_idx = header.index('Biome2')
    except ValueError:
        return {}
    
    # Create indexed categories: (biome, creature_type) -> list of monsters
    categories = {}
    
    # Process in batches to avoid statement limits
    for i, monster in enumerate(monster_data['data']):
        if i > 800:  # Limit processing to avoid statement limits
            break
            
        if len(monster) <= max(name_idx, xp_idx, type_idx, biome1_idx, biome2_idx):
            continue
            
        creature_type = monster[type_idx]
        biomes = [str(monster[biome1_idx]), str(monster[biome2_idx])]
        
        for biome in biomes:
            if biome and biome != 'None' and biome.strip():
                key = (biome, creature_type)
                if key not in categories:
                    categories[key] = []
                categories[key].append(monster)
    
    return categories

def get_monsters_from_category(categories, biome, creature_type, target_xp, max_monsters=4, exact_count=None):
    """Get monsters from pre-processed categories - respects exact_count when specified"""
    key = (biome, creature_type)
    if key not in categories:
        return []
    
    monsters = categories[key]
    if not monsters:
        return []
    
    # Get XP index (assuming standard format from hunt system)
    xp_idx = 2  # XP is typically index 2 in the monster data structure
    
    # If exact count is specified, select that many monsters with balanced XP
    if exact_count is not None:
        # For exact counts, try to find monsters close to target_xp per monster
        per_monster_target = target_xp / exact_count if exact_count > 0 else target_xp
        
        # Create XP ranges around the target
        min_xp = max(1, per_monster_target * 0.3)  # At least 30% of target
        max_xp = per_monster_target * 2.0  # At most 200% of target
        ideal_min = per_monster_target * 0.7  # Prefer 70-130% of target
        ideal_max = per_monster_target * 1.3
        
        # Categorize available monsters
        ideal_monsters = []
        acceptable_monsters = []
        
        for monster in monsters:
            if len(monster) > xp_idx:
                monster_xp = monster[xp_idx]
                if ideal_min <= monster_xp <= ideal_max:
                    ideal_monsters.append(monster)
                elif min_xp <= monster_xp <= max_xp:
                    acceptable_monsters.append(monster)
        
        # Select monsters preferring ideal range
        selected = []
        candidates = ideal_monsters[:] if ideal_monsters else acceptable_monsters[:]
        
        if not candidates:
            # Fallback to any available monsters if none in range
            candidates = [m for m in monsters if len(m) > xp_idx][:20]
        
        # Select exactly the requested count
        for i in range(min(exact_count, len(candidates))):
            if candidates:
                monster = randchoice(candidates)
                selected.append(monster)
                candidates.remove(monster)  # Avoid duplicates
        
        return selected
    
    # Original XP-based selection logic for when exact_count is not specified
    # Filter by XP and select monsters
    suitable = []
    for monster in monsters:
        if len(monster) > xp_idx and monster[xp_idx] <= target_xp:
            suitable.append(monster)
        if len(suitable) >= max_monsters * 3:  # Early termination
            break
    
    if not suitable:
        return []
    
    # Simple selection - pick monsters that fit the XP budget
    selected = []
    current_xp = 0
    
    # Sort by XP (highest first for better selection)
    suitable.sort(key=lambda m: m[xp_idx], reverse=True)
    
    # Select monsters to meet target XP
    for monster in suitable:
        if len(selected) >= max_monsters:
            break
        monster_xp = monster[xp_idx]
        if current_xp + monster_xp <= target_xp * 1.3:  # Allow 30% overage
            selected.append(monster)
            current_xp += monster_xp
    
    # If we don't have enough monsters, fill with smaller ones
    if len(selected) < max_monsters // 2:
        for monster in suitable:
            if len(selected) >= max_monsters:
                break
            if monster not in selected:
                selected.append(monster)
    
    return selected

def generate_monster_commands(teams_data, players):
    """Generate the actual monster addition and team assignment commands"""
    command_list = []
    monster_data = load_monster_data()
    
    # Pre-process monster data once for all teams
    monster_categories = preprocess_monster_data(monster_data)
    
    # STEP 1: Select and process monsters for all teams
    announcement_teams = []
    
    for team_num, team in enumerate(teams_data['teams'], 1):
        announcement_team = {
            'num': team_num,
            'name': team.get('faction_name', 'Monsters'),
            'players': team.get('players', []),
            'monsters': []
        }
        
        # Get monsters for this team
        if 'faction_data' in team:
            biome, creature_type = team['faction_data']
            target_xp = team.get('target_xp', 400)
            exact_count = team.get('exact_count')  # NEW: exact monster count
            
            if exact_count is not None:
                selected_monsters = get_monsters_from_category(
                    monster_categories, biome, creature_type, target_xp, exact_count, exact_count
                )
            else:
                selected_monsters = get_monsters_from_category(
                    monster_categories, biome, creature_type, target_xp
                )
            
            # Store raw monster data for combat addition later
            team['_selected_monsters'] = selected_monsters
            
            # Process for display
            if selected_monsters:
                monster_counts = {}
                for monster in selected_monsters:
                    name = monster[0]  # Creature name is first element
                    monster_counts[name] = monster_counts.get(name, 0) + 1
                
                # Create display strings
                for monster_name, count in monster_counts.items():
                    if count == 1:
                        announcement_team['monsters'].append(monster_name)
                    else:
                        announcement_team['monsters'].append(f"{count}x {monster_name}")
        
        announcement_teams.append(announcement_team)
    
    # STEP 2: Generate announcement
    title = "🏟️ Arena Battle Beginning!"
    
    # Team color emojis for consistent identification
    team_color_emojis = {1: "🔵", 2: "🔴", 3: "🟡", 4: "🟢", 5: "🟠", 6: "🟣"}
    
    desc = f"**🏟️ {teams_data['type']}**\n"
    desc += f"⚔️ **Format:** {teams_data['format']}"
    if 'difficulty' in teams_data:
        desc += f" | **Difficulty:** {teams_data['difficulty']}"
    
    desc += "\n\n" + "═" * 35 + "\n"
    desc += "🏟️ **TEAMS ASSEMBLING** 🏟️\n"
    desc += "═" * 35 + "\n\n"
    
    for team in announcement_teams:
        # Get team color emoji
        team_emoji = team_color_emojis.get(team['num'], "⚪")
        
        desc += f"{team_emoji} **TEAM {team['num']}** | {team['name']}\n"
        
        members = []
        # Add players with special formatting
        if team['players']:
            for player in team['players']:
                members.append(f"├─ 👤 {player['name']} (Level {player['level']})")
        
        # Add monsters without individual emojis
        if team['monsters']:
            for i, monster in enumerate(team['monsters']):
                # Determine correct tree prefix
                is_last_monster = (i == len(team['monsters']) - 1)
                is_last_overall = is_last_monster and not team['players']
                
                if is_last_overall:
                    prefix = "└─"
                else:
                    prefix = "├─"
                
                members.append(f"{prefix} {monster}")
        
        if not members:
            members.append("└─ ❌ Empty Team")
        
        desc += "\n".join(members) + "\n\n"
    
    desc += "🎯 Adding monsters to combat with team assignments..."
    desc += f"\n\n💰 **Place your bets!** Use `{cmd} bet team1 10gp` to bet on a team!"
    desc += f"\n⚠️ **Note:** Betting closes once any monster takes damage."
    
    command_list.append(f'{pref}embed -title "{title}" -desc "{desc}" -color 0x4ecdc4')
    
    # STEP 3: Handle player team assignments  
    if players:
        for team_num, team in enumerate(teams_data['teams'], 1):
            if 'players' in team:
                for player in team['players']:
                    # Add team effect directly
                    if team_num == 1:
                        command_list.append(f'{pref}i effect {player["name"]} "Ally (auto)"')
                    else:
                        command_list.append(f'{pref}i effect {player["name"]} "Team {team_num} (auto)"')
    
    # STEP 4: Add monsters to combat using stored selections
    monster_team_assignments = []  # Store for later effect assignment
    
    for team_num, team in enumerate(teams_data['teams'], 1):
        if '_selected_monsters' in team:
            selected_monsters = team['_selected_monsters']
            
            if selected_monsters:
                # Count monsters for addition
                monster_counts = {}
                for monster in selected_monsters:
                    name = monster[0]
                    monster_counts[name] = monster_counts.get(name, 0) + 1
                
                # Add each monster type first
                for monster_name, count in monster_counts.items():
                    command_list.append(f'{pref}i madd "{monster_name}" -n {count} -name "{monster_name}#"')
                    
                    # Store team assignments for later
                    for i in range(count):
                        if count == 1:
                            instance = f"{monster_name}1"
                        else:
                            instance = f"{monster_name}{i+1}"
                        monster_team_assignments.append((instance, team_num))
    
    # STEP 5: Apply team effects after all monsters are added
    for instance, team_num in monster_team_assignments:
        if team_num == 1:
            command_list.append(f'{pref}i effect "{instance}" "Ally (auto)"')
        else:
            command_list.append(f'{pref}i effect "{instance}" "Team {team_num} (auto)"')
    
    # Final commands
    command_list.append(f'{pref}i next')
    command_list.append(f'{pref}embed -title "🏟️ Arena Battle Ready!" -desc "All teams assembled!\n\n💰 **Betting Open:** Use `{cmd} bet team1 10gp` to place bets!\n⚠️ **Betting closes** once any monster takes damage.\n⚔️ **Start Combat:** Use `{pref}auto` to begin automated monster combat." -color 0x95e1d3')
    
    return command_list

# ==================== REFINED BETTING SYSTEM ====================

def get_arena_bets():
    """Get all bets for current arena from combat metadata"""
    if not c:
        return {}
    
    bets_data = c.get_metadata('arena_bets')
    if bets_data:
        return load_json(bets_data)
    return {}

def set_arena_bets(bets_data):
    """Store all bets for current arena in combat metadata"""
    if not c:
        return False
    
    c.set_metadata('arena_bets', dump_json(bets_data))
    return True

def parse_bet_amount(amount_str):
    """Parse bet amount and currency from string like '10gp' or '10'"""
    amount_str = amount_str.lower().strip()
    
    # Check for currency suffixes
    currencies = ['pp', 'gp', 'ep', 'sp', 'cp']
    
    for currency in currencies:
        if amount_str.endswith(currency):
            try:
                amount = int(amount_str[:-len(currency)])
                return amount, currency
            except ("ValueError", "TypeError"):
                return None, None
    
    # No currency specified, default to gp
    try:
        amount = int(amount_str)
        return amount, 'gp'
    except ("ValueError", "TypeError"):
        return None, None

def parse_team_number(team_str):
    """Parse team number from string like 'team1', 'team2', etc."""
    team_str = team_str.lower().strip()
    
    if team_str.startswith('team'):
        try:
            return int(team_str[4:])
        except ("ValueError", "TypeError"):
            return None
    
    # Try parsing as direct number
    try:
        return int(team_str)
    except ("ValueError", "TypeError"):
        return None

def get_existing_teams():
    """Get list of teams that exist in current combat"""
    if not c:
        return []
    
    teams = set()
    
    for combatant in c.combatants:
        for effect in combatant.effects:
            if "Ally (auto)" in effect.name:
                teams.add(1)
            elif "Team" in effect.name and "(auto)" in effect.name:
                # More precise extraction: parse "Team X (auto)" format
                effect_name = effect.name
                if effect_name.startswith("Team ") and effect_name.endswith(" (auto)"):
                    # Extract the part between "Team " and " (auto)"
                    team_part = effect_name[5:-7]  # Remove "Team " and " (auto)"
                    try:
                        team_num = int(team_part.strip())
                        teams.add(team_num)
                    except ("ValueError", "TypeError"):
                        continue
    
    return core.sorted(list(teams))

def is_combat_in_progress():
    """Check if combat has started (any monster has taken damage)"""
    if not c:
        return False
    
    for combatant in c.combatants:
        if autolib.isMonster(combatant):
            # Check if monster has taken any damage
            if combatant.hp < combatant.max_hp:
                return True
    
    return False

def get_battle_status():
    """
    Determine the current battle status
    Returns: (status, winning_team)
    Status can be: 'ongoing', 'victory', 'disqualification', 'no_combat'
    """
    if not c:
        return 'no_combat', None
    
    # Get all teams and their alive monster counts
    team_alive_counts = {}
    team_total_counts = {}
    combat_has_started = False
    
    for combatant in c.combatants:
        # FIXED: Check ALL combatants with team effects, not just autolib.isMonster()
        team_num = None
        
        # Check for team assignment effects
        for effect in combatant.effects:
            effect_name = effect.name.strip()
            
            if effect_name == "Ally (auto)":
                team_num = 1
                break
            elif effect_name.startswith("Team ") and effect_name.endswith(" (auto)"):
                team_part = effect_name[5:-7].strip()
                try:
                    team_num = int(team_part)
                    break
                except ValueError:
                    continue
        
        # If this combatant has a team assignment, count it
        if team_num and combatant.hp is not None and combatant.max_hp is not None:
            # Count total combatants per team
            team_total_counts[team_num] = team_total_counts.get(team_num, 0) + 1
            
            # Check if this combatant has taken damage (combat started)
            if combatant.hp < combatant.max_hp:
                combat_has_started = True
            
            # Count alive combatants per team (hp > 0)
            if combatant.hp > 0:
                team_alive_counts[team_num] = team_alive_counts.get(team_num, 0) + 1
    
    # No teams found
    if not team_total_counts:
        return 'no_combat', None
    
    # Count how many teams have at least one alive member
    teams_with_survivors = len([team for team, count in team_alive_counts.items() if count > 0])
    
    # Determine battle status based on combat state and survivor count
    if not combat_has_started:
        # No damage dealt yet - battle is ready but not started
        return 'ongoing', None
    elif teams_with_survivors == 0:
        # Combat started but all team members dead - disqualification
        return 'disqualification', None
    elif teams_with_survivors == 1:
        # Combat started and only one team has survivors - victory
        winning_team = [team for team, count in team_alive_counts.items() if count > 0][0]
        return 'victory', winning_team
    else:
        # Combat started and multiple teams have survivors - battle ongoing
        return 'ongoing', None

def is_combat_in_progress():
    """Check if combat has started (any team member has taken damage)"""
    if not c:
        return False
    
    for combatant in c.combatants:
        # Check ALL combatants with team effects for damage
        team_num = None
        for effect in combatant.effects:
            effect_name = effect.name.strip()
            if effect_name == "Ally (auto)" or (effect_name.startswith("Team ") and effect_name.endswith(" (auto)")):
                team_num = True
                break
        
        # If this is a team member and has taken damage
        if team_num and combatant.hp is not None and combatant.max_hp is not None:
            if combatant.hp < combatant.max_hp:
                return True
    
    return False

def convert_to_gold_value(amount, currency):
    """Convert any currency amount to gold equivalent for comparison"""
    conversion_rates = {
        'pp': 10.0,    # 1 pp = 10 gp
        'gp': 1.0,     # 1 gp = 1 gp
        'ep': 0.5,     # 1 ep = 0.5 gp
        'sp': 0.1,     # 1 sp = 0.1 gp
        'cp': 0.01     # 1 cp = 0.01 gp
    }
    return amount * conversion_rates.get(currency, 1.0)

def check_player_funds(amount, currency):
    """Check if player has enough funds for the bet using total coinpurse value"""
    required_gold_value = convert_to_gold_value(amount, currency)
    total_gold_value = char.coinpurse.total
    
    return total_gold_value >= required_gold_value

def place_bet(team_num, amount, currency):
    """Place a bet on a team with refined restrictions"""
    # Check if combat has already started
    if is_combat_in_progress():
        return False, f"🔒 **Betting is closed!** Combat has already begun and damage has been dealt.\n\nBets can only be placed before any monster takes damage."
    
    # Check battle status
    battle_status, _ = get_battle_status()
    if battle_status == 'no_combat':
        return False, f"No arena battle in progress. Use `{cmd} 1v1` or `{cmd} random` to start a battle first."
    elif battle_status in ['victory', 'disqualification']:
        return False, f"This arena battle has already concluded. Use `{cmd} 1v1` or `{cmd} random` to start a new battle."
    
    # Validate team exists
    existing_teams = get_existing_teams()
    if team_num not in existing_teams:
        team_list = ", ".join([f"team{t}" for t in existing_teams])
        return False, f"Team {team_num} doesn't exist in this arena battle.\n\n**Available teams:** {team_list}"
    
    # Check funds using total coinpurse value
    if not check_player_funds(amount, currency):
        required_gold = convert_to_gold_value(amount, currency)
        return False, f"💸 **Insufficient funds!**\n\nRequired: **{amount}{currency}** ({required_gold}gp equivalent)\nYour balance: **{char.coinpurse.total}gp total**"
    
    # Get existing bets
    bets_data = get_arena_bets()
    player_name = char.name
    
    # Check if player already has a bet
    if player_name in bets_data:
        existing_bet = bets_data[player_name]
        return False, f"🎯 **You already have a bet placed!**\n\nCurrent bet: **{existing_bet['amount']}{existing_bet['currency']}** on **team{existing_bet['team']}**\n\nYou can only bet once per arena battle. Wait for this battle to conclude before placing new bets."
    
    # Deduct funds from player using autoconvert
    try:
        modify_args = {currency: -amount, 'autoconvert': True}
        char.coinpurse.modify_coins(**modify_args)
    except:
        return False, f"💸 **Transaction failed!** Unable to deduct {amount}{currency} from your coinpurse."
    
    # Store the bet
    bets_data[player_name] = {
        'team': team_num,
        'amount': amount,
        'currency': currency
    }
    
    set_arena_bets(bets_data)
    
    # Enhanced success message with personal flair
    team_color_emojis = {1: "🔵", 2: "🔴", 3: "🟡", 4: "🟢", 5: "🟠", 6: "🟣"}
    team_emoji = team_color_emojis.get(team_num, "⚪")
    
    success_msg = f"""🎰 **{player_name} steps up to the betting booth with confidence!**

**Arena Wager Placed:**
{team_emoji} **Team {team_num}** - **{amount}{currency}**

💰 **Transaction Details:**
• Bet Amount: **{amount}{currency}**
• Potential Winnings: **{amount * 2}{currency}** (2:1 odds)
• Your Remaining Funds: **{char.coinpurse.total}gp**

🏟️ **The crowd murmurs as {player_name} places their faith in Team {team_num}!**

Good luck! May the odds be in your favor! 🍀

⚠️ **Remember:** Betting closes once any monster takes damage!"""
    
    return True, success_msg

def collect_bets():
    """Process bet collection and payouts with refined logic"""
    battle_status, winning_team = get_battle_status()
    
    # Check if battle is concluded
    if battle_status == 'ongoing':
        return False, "⏳ **Arena battle is still ongoing!**\n\nWait for one team to eliminate all others before collecting winnings."
    elif battle_status == 'no_combat':
        return False, f"❌ **No arena battle found.**\n\nStart a battle with `{cmd} 1v1` or `{cmd} random` first."
    
    # Get bets data
    bets_data = get_arena_bets()
    if not bets_data:
        return False, "💸 **No bets were placed** on this arena battle.\n\nNothing to collect!"
    
    player_name = char.name
    if player_name not in bets_data:
        return False, f"🤷 **You didn't place any bets** on this arena battle.\n\nUse `{cmd} bet team1 10gp` in future battles to participate in betting!"
    
    player_bet = bets_data[player_name]
    bet_team = player_bet['team']
    bet_amount = player_bet['amount']
    bet_currency = player_bet['currency']
    
    # Team emojis for visual flair
    team_color_emojis = {1: "🔵", 2: "🔴", 3: "🟡", 4: "🟢", 5: "🟠", 6: "🟣"}
    bet_emoji = team_color_emojis.get(bet_team, "⚪")
    winning_emoji = team_color_emojis.get(winning_team, "⚪")
    
    # Handle disqualification (all teams eliminated)
    if battle_status == 'disqualification':
        # Refund the bet
        try:
            modify_args = {bet_currency: bet_amount, 'autoconvert': True}
            char.coinpurse.modify_coins(**modify_args)
        except:
            return False, f"❌ **Refund failed!** Unable to return {bet_amount}{bet_currency} to your coinpurse."
        
        # Clear all bets
        c.set_metadata('arena_bets', '{}')
        
        disqualification_msg = f"""💀 **TOTAL CARNAGE! ALL TEAMS ELIMINATED!** 💀

🏟️ **Battle Result:** Complete Mutual Destruction

💰 **Bet Refund:**
• Your Bet: {bet_emoji} **Team {bet_team}** - **{bet_amount}{bet_currency}**
• Status: **REFUNDED** (no survivors)
• Refund Amount: **{bet_amount}{bet_currency}**
• Your New Balance: **{char.coinpurse.total}gp**

🎭 **{player_name} approaches the betting booth as the dust settles over the empty arena. The bookkeeper shakes their head and pushes your coins back across the table.**

"Well, that was... unexpected. Nobody wins when everybody loses. Here's your money back!"

Better luck in the next battle! 🎯"""
        
        return True, disqualification_msg
    
    # Handle victory (one team survived)
    elif battle_status == 'victory':
        
        if bet_team == winning_team:
            # Player won! Double the bet
            winnings = bet_amount * 2
            try:
                modify_args = {bet_currency: winnings, 'autoconvert': True}
                char.coinpurse.modify_coins(**modify_args)
            except:
                return False, f"❌ **Payout failed!** Unable to add {winnings}{bet_currency} to your coinpurse."
            
            # Clear all bets
            c.set_metadata('arena_bets', '{}')
            
            win_msg = f"""🎉 **VICTORY! THE CROWD GOES WILD!** 🎉

{winning_emoji} **Team {winning_team} Emerges Triumphant!**

💰 **Winning Payout:**
• Your Bet: {bet_emoji} **Team {bet_team}** - **{bet_amount}{bet_currency}**
• Payout: **{winnings}{bet_currency}** (2:1 odds)
• Profit: **+{bet_amount}{bet_currency}**
• Your New Balance: **{char.coinpurse.total}gp**

🏟️ **{player_name} approaches the betting booth with a triumphant grin as coins clink into their purse!**

Your instincts proved correct! The crowd cheers as you collect your well-earned winnings! 🏆✨"""
            
            return True, win_msg
        
        else:
            # Player lost, bet was already taken
            # Clear all bets
            c.set_metadata('arena_bets', '{}')
            
            loss_msg = f"""{winning_emoji} **Team {winning_team} Claims Victory!**

📉 **Bet Resolution:**
• Your Bet: {bet_emoji} **Team {bet_team}** - **{bet_amount}{bet_currency}**
• Winning Team: {winning_emoji} **Team {winning_team}**
• Result: **LOST**
• Your Remaining Funds: **{char.coinpurse.total}gp**

🏟️ **{player_name} watches the victorious team with a rueful smile, already planning their next wager!**

The arena gods were not with you this time. Fortune favors the bold - try again next battle! 🎯"""
            
            return True, loss_msg
    
    # This should never happen, but just in case
    return False, "❌ **Unknown battle status.** Please report this error."

def show_betting_status():
    """Show current betting status with essential information"""
    battle_status, winning_team = get_battle_status()
    
    if battle_status == 'no_combat':
        return False, f"No arena battle in progress. Use `{cmd} 1v1` or `{cmd} random` to start a battle."
    
    existing_teams = get_existing_teams()
    bets_data = get_arena_bets()
    combat_in_progress = is_combat_in_progress()
    
    desc = ""
    
    # Battle status
    if battle_status == 'ongoing':
        if combat_in_progress:
            desc += f"**Battle Status:** ⚔️ **ACTIVE COMBAT** (ongoing battle)\n"
        else:
            desc += f"**Battle Status:** 🟡 **READY** (no damage yet)\n"
    elif battle_status == 'victory':
        desc += f"**Battle Status:** 🏆 **CONCLUDED** (Team {winning_team} victorious)\n"
    elif battle_status == 'disqualification':
        desc += f"**Battle Status:** 💀 **DISQUALIFIED** (all teams eliminated)\n"
    
    desc += f"**Available Teams:** {', '.join([f'team{t}' for t in existing_teams])}\n"
    
    # Betting status
    if battle_status in ['victory', 'disqualification']:
        desc += f"**Betting Status:** 🔒 **CLOSED** (battle concluded)\n\n"
    elif combat_in_progress:
        desc += f"**Betting Status:** 🔒 **CLOSED** (combat active)\n\n"
    else:
        desc += f"**Betting Status:** 🔓 **OPEN**\n\n"
    
    # Current bets
    if bets_data:
        desc += "**Current Bets:**\n"
        team_color_emojis = {1: "🔵", 2: "🔴", 3: "🟡", 4: "🟢", 5: "🟠", 6: "🟣"}
        for player, bet_info in bets_data.items():
            team_emoji = team_color_emojis.get(bet_info['team'], "⚪")
            desc += f"• {player}: {bet_info['amount']}{bet_info['currency']} on {team_emoji}team{bet_info['team']}\n"
    else:
        desc += "**Current Bets:** None placed yet\n"
    
    # Action instructions
    desc += "\n**Commands:**\n"
    if battle_status == 'ongoing' and not combat_in_progress:
        desc += f"• **Place bet:** `{cmd} bet team1 10gp`\n"
    if battle_status in ['victory', 'disqualification']:
        desc += f"• **Collect winnings:** `{cmd} collect bets`\n"
    if battle_status == 'ongoing':
        desc += f"• **Start combat:** `{pref}auto` (automated monster combat)\n"
        if combat_in_progress:
            desc += f"• **Continue combat:** `{pref}auto` (until one team remains)\n"
    
    return True, desc

# ==================== BATTLE LOGIC ====================

# XP Thresholds for encounter balancing (from hunt system)
XP_THRESHOLDS = {
    1: {"Easy": 25, "Medium": 50, "Hard": 75, "Deadly": 100},
    2: {"Easy": 50, "Medium": 100, "Hard": 150, "Deadly": 200},
    3: {"Easy": 75, "Medium": 150, "Hard": 225, "Deadly": 400},
    4: {"Easy": 125, "Medium": 250, "Hard": 375, "Deadly": 500},
    5: {"Easy": 250, "Medium": 500, "Hard": 900, "Deadly": 1100},
    6: {"Easy": 300, "Medium": 600, "Hard": 900, "Deadly": 1400},
    7: {"Easy": 350, "Medium": 750, "Hard": 1100, "Deadly": 1700},
    8: {"Easy": 450, "Medium": 900, "Hard": 1400, "Deadly": 2100},
    9: {"Easy": 550, "Medium": 1100, "Hard": 1600, "Deadly": 2400},
    10: {"Easy": 600, "Medium": 1200, "Hard": 1900, "Deadly": 2800}
}

# Multi-team multipliers for chaos battles
MULTI_TEAM_MULTIPLIERS = {
    2: 1.0, 3: 1.2, 4: 1.4, 5: 1.6, 6: 1.8, 7: 2.0, 8: 2.2, 9: 2.4, 10: 2.5
}

# Available monster factions (simplified from full system)
MONSTER_FACTIONS = [
    ("Forest", "Beast", ["Wolf", "Brown Bear", "Dire Wolf", "Giant Spider"]),
    ("Forest", "Humanoid", ["Goblin", "Hobgoblin", "Bugbear", "Bandit"]),
    ("Mountain", "Giant", ["Ogre", "Hill Giant"]),
    ("Mountain", "Humanoid", ["Orc", "Orc Warrior"]),
    ("Underdark", "Monstrosity", ["Owlbear", "Displacer Beast"]),
    ("Forest", "Monstrosity", ["Worg", "Griffon"]),
    ("Haunted", "Undead", ["Skeleton", "Zombie", "Ghoul", "Wight"]),
    ("Desert", "Beast", ["Giant Scorpion", "Camel"]),
    ("Grassland", "Beast", ["Lion", "Hyena"]),
    ("Grassland", "Humanoid", ["Gnoll", "Gnoll Fang"])
]

def get_help_text():
    return f"""
**🏟️ Arena Battle System with Betting**

**Basic Commands:**
`{cmd} 1v1` - Classic duel (1 monster vs 1 monster)
`{cmd} 2v2` - Team battle (2 monsters vs 2 monsters)
`{cmd} random` - Random 2-3 faction battle
`{cmd} player [difficulty]` - Players + monsters vs monsters
`{cmd} help` - Show this help
`{cmd} advanced` - Show detailed battle modes

**💰 Betting Commands:**
`{cmd} bet team1 10gp` - Bet 10 gold on team 1
`{cmd} bet team2 5sp` - Bet 5 silver on team 2
`{cmd} collect bets` - Collect winnings after battle ends
`{cmd} bets` - Show current betting status

**🎯 Betting Rules:**
• **One bet per player** per arena battle
• **Betting closes** once any monster takes damage
• **Winning bets pay double** (2:1 odds)

**⚔️ Battle Mechanics:**
Teams are automatically balanced for fair fights. Use `{pref}auto` for automated monster combat after setup.
"""

def get_advanced_text():
    return f"""
**🏟️ Advanced Arena Battle Modes**

**🎲 Random Mode:**
`{cmd} random` - Generates 2-3 random monster factions fighting each other

**⚔️ Player vs Monster Mode:**
`{cmd} player [difficulty]` - Players team up with monsters against enemy monsters
**Note:** Difficulty scaling only applies when players are present in teams

**🏟️ Custom Battle Formats:**
`{cmd} [format] [difficulty]` - Specify exact team compositions

**Format Syntax:**
• Numbers = monster count per team (exactly that many monsters)
• `v` = separates teams
• `p` = suffix indicating which team gets players
• Examples: `1v1` (1 vs 1), `2v3v4` (2 vs 3 vs 4), `1v2p` (1 vs 2+players)

**Format Examples:**
• `{cmd} 1v1` - Classic duel (1 monster vs 1 monster, balanced XP)
• `{cmd} 1v1v1` - Triple threat (3 teams of 1 monster each, equal power)
• `{cmd} 1v2` - David vs Goliath (1 strong monster vs 2 weaker monsters)
• `{cmd} 2v2v2v2` - Quad alliance (4 teams of 2 monsters each)
• `{cmd} 1v2v3p` - 1 monster vs 2 monsters vs (3 monsters + all players)
• `{cmd} 2v2p` - 2 monsters vs (2 monsters + all players)

**Difficulty Scaling (Player Teams Only):**
When players are present, specify difficulty to scale monster power:
• Easy - Weaker monsters, good for new players
• Medium - Balanced encounters (default)
• Hard - Challenging but fair
• Deadly - Maximum difficulty, use with caution

**💰 Betting System:**
Place bets on teams before combat begins. Winners receive double their bet! Arena battles always produce a clear victor or mutual destruction (refunds).

**Auto-Balancing:**
System automatically selects appropriate monsters from different factions to create engaging battles. For exact count battles (like `1v1`, `2v3`), teams are balanced by total XP - each team gets roughly equal total power regardless of monster count, ensuring fair and exciting fights.

**Other Commands:**
`{cmd} clear` - Clear current arena and reset for new battle
`{cmd} bets` - Show detailed betting status
"""

def check_existing_combat():
    """Check if combat has existing teams/monsters that need clearing"""
    if not c:
        return False, ""
        
    # Check for existing team assignments
    team_effects = []
    for combatant in c.combatants:
        for effect in combatant.effects:
            if "Ally (auto)" in effect.name or ("Team" in effect.name and "(auto)" in effect.name):
                team_effects.append(f"{combatant.name}: {effect.name}")
    
    # Check for existing monsters
    monsters = [co for co in c.combatants if autolib.isMonster(co)]
    
    if team_effects or monsters:
        warning = f"""
**⚠️ Existing Arena Battle Detected**

Current combat contains existing team assignments or monsters:
"""
        if team_effects:
            warning += f"\n**Team Assignments:**\n" + "\n".join(f"• {effect}" for effect in team_effects[:5])
            if len(team_effects) > 5:
                warning += f"\n• ... and {len(team_effects) - 5} more"
                
        if monsters:
            warning += f"\n**Monsters:** {', '.join(monster.name for monster in monsters[:5])}"
            if len(monsters) > 5:
                warning += f" and {len(monsters) - 5} more"
        
        warning += f"""

Use `{pref}i end` to end combat and reset the arena for a fresh battle.
"""
        return True, warning
    
    return False, ""

def get_players_in_combat():
    """Get all players currently in combat initiative"""
    if not c:
        return []
        
    players = []
    for combatant in c.combatants:
        # Check if it's a player (not a monster, has race, etc.)
        if (combatant.creature_type is None and 
            combatant.monster_name is None and 
            not autolib.isMonster(combatant) and 
            combatant.race):
            players.append({
                'name': combatant.name,
                'level': combatant.levels.total_level,
                'combatant': combatant
            })
    
    return players

def parse_arena_format(format_str):
    """Parse arena format string into team structure"""
    if not format_str or format_str.lower() == "random":
        return "random", None, None
    elif format_str.lower() == "player":
        return "player", None, None
    else:
        # Parse advanced format like "1v2v3p"
        try:
            teams = format_str.lower().split('v')
            player_team_index = None
            team_sizes = []
            
            for i, team in enumerate(teams):
                if team.endswith('p'):
                    player_team_index = i
                    team_sizes.append(int(team[:-1]))
                else:
                    team_sizes.append(int(team))
            
            return "advanced", team_sizes, player_team_index
        except ("ValueError", "TypeError"):
            return "invalid", None, None

def calculate_target_xp(players, difficulty="Medium"):
    """Calculate target XP for encounter using hunt system logic"""
    if not players:
        # Pure monster battle - use moderate XP target
        return 800
    
    # Calculate party XP thresholds
    total_xp = 0
    for player in players:
        level = min(player['level'], 10)  # Cap at level 10 for table lookup
        total_xp += XP_THRESHOLDS[level][difficulty.title()]
    
    return total_xp

def select_random_factions(needed_factions):
    """Select random monster factions for battle"""
    available = MONSTER_FACTIONS[:]
    selected = []
    
    # First pass - unique factions
    while len(selected) < needed_factions and available:
        faction = randchoice(available)
        selected.append(faction)
        available.remove(faction)
    
    # Second pass - allow repeats if needed
    while len(selected) < needed_factions:
        if not MONSTER_FACTIONS:
            break
        faction = randchoice(MONSTER_FACTIONS)
        selected.append(faction)
    
    return selected

def build_faction_team(faction, target_xp, team_count, exact_count=None):
    """Build a team from a faction with target XP and optional exact monster count"""
    biome, creature_type, monsters = faction
    
    # Apply multi-team multiplier
    multiplier = MULTI_TEAM_MULTIPLIERS.get(team_count, 2.5)
    adjusted_target = target_xp / multiplier
    
    team_data = {
        'faction_name': f"{biome} {creature_type}s",
        'faction_data': (biome, creature_type),  # Store for monster selection
        'target_xp': adjusted_target,
        'estimated_xp': adjusted_target * multiplier
    }
    
    # NEW: Store exact count if specified
    if exact_count is not None:
        team_data['exact_count'] = exact_count
    
    return team_data

# ==================== MAIN COMMAND PROCESSING ====================

subcommand = args[0].lower() if args else "help"

# Handle betting commands first
if subcommand == "bet":
    if len(args) < 3:
        title = "❌ Invalid Bet Format"
        desc = f"""**Usage:** `{cmd} bet team1 10gp`

**Examples:**
• `{cmd} bet team1 10gp` - Bet 10 gold on team 1
• `{cmd} bet team2 5sp` - Bet 5 silver on team 2  
• `{cmd} bet team1 10` - Bet 10 gold (default currency)

**Supported currencies:** cp, sp, ep, gp, pp

⚠️ **Remember:** Betting closes once any monster takes damage!"""
        return f'embed -title "{title}" -desc "{desc}" -color 0xff6b35 -footer "{cmd} help | Arena Betting System"'
    
    team_str = args[1]
    amount_str = args[2]
    
    team_num = parse_team_number(team_str)
    if team_num is None:
        title = "❌ Invalid Team Format"
        desc = f"""Could not parse team from **'{team_str}'**.

**Correct format:** `team1`, `team2`, `team3`, etc.
**Example:** `{cmd} bet team1 10gp`"""
        return f'embed -title "{title}" -desc "{desc}" -color 0xff6b35 -footer "{cmd} help | Arena Betting System"'
    
    amount, currency = parse_bet_amount(amount_str)
    if amount is None or amount <= 0:
        title = "❌ Invalid Amount"
        desc = f"""Could not parse amount from **'{amount_str}'**.

**Correct formats:**
• `10gp` - 10 gold pieces
• `5sp` - 5 silver pieces  
• `10` - 10 gold (default)

**Minimum bet:** 1 of any currency"""
        return f'embed -title "{title}" -desc "{desc}" -color 0xff6b35 -footer "{cmd} help | Arena Betting System"'
    
    success, message = place_bet(team_num, amount, currency)
    
    if success:
        title = "🎰 Arena Wager Accepted!"
        color = "0x95e1d3"
    else:
        title = "❌ Betting Rejected"
        color = "0xff6b35"
    
    return f'embed -title "{title}" -desc "{message}" -color {color} -thumb {image} -footer "{cmd} help | Arena Betting System"'

elif subcommand in ["collect", "collect_bets", "collectbets"] or (subcommand == "collect" and len(args) > 1 and args[1].lower() in ["bet", "bets"]):
    success, message = collect_bets()
    
    if success:
        if "🎉" in message:
            title = "🎉 Winning Payout!"
            color = "0x95e1d3"
        elif "💀" in message:
            title = "💀 Battle Disqualified - Bet Refunded"
            color = "0xffd23f"
        else:
            title = "💸 Better Luck Next Time"
            color = "0xff6b35"
    else:
        title = "❌ Cannot Collect Winnings"
        color = "0xff6b35"
    
    return f'embed -title "{title}" -desc "{message}" -color {color} -thumb {image} -footer "{cmd} help | Arena Betting System"'

elif subcommand in ["bets", "betting", "status"]:
    success, message = show_betting_status()
    
    if success:
        title = "💰 Arena Betting Dashboard"
        color = "0x4ecdc4"
    else:
        title = "❌ No Arena Battle"
        color = "0xff6b35"
    
    return f'embed -title "{title}" -desc "{message}" -color {color} -thumb {image} -footer "{cmd} help | Arena Betting System"'

# Handle help and utility commands
elif subcommand in "help?":
    title = "🏟️ Arena Battle System"
    desc = get_help_text()
    return f'embed -title "{title}" -desc "{desc}" -color 0x4ecdc4 -thumb {image} -footer "{cmd} help | made by @alpha983"'

elif subcommand == "advanced":
    title = "🎯 Advanced Arena Battle Modes"
    desc = get_advanced_text()
    return f'embed -title "{title}" -desc "{desc}" -color 0x4ecdc4 -thumb {image} -footer "{cmd} help | made by @alpha983"'

elif subcommand in ["clear", "end"]:
    if not c:
        return f'embed -title "No Active Combat" -desc "No combat session to clear." -color 0xffd23f -footer "{cmd} help | Arena Battle System"'
    
    # Clear bets when clearing arena
    bets_data = get_arena_bets()
    bet_count = len(bets_data) if bets_data else 0
    
    command_list = []
    
    # Refund all pending bets before ending
    if bet_count > 0:
        for player_name, bet_info in bets_data.items():
            try:
                # Note: This only works if the player who ran the command has the bet
                # In practice, clearing should be done by a DM or when all players agree
                if player_name == char.name:
                    modify_args = {bet_info['currency']: bet_info['amount'], 'autoconvert': True}
                    char.coinpurse.modify_coins(**modify_args)
            except:
                pass  # Silently fail individual refunds during clear
        
        clear_msg = f"🧹 **Arena Cleared!** {bet_count} pending bet(s) cancelled and refunded."
    else:
        clear_msg = "🧹 **Arena Cleared!** Combat ended and arena reset."
    
    clear_msg += f"\n\nUse `{cmd} 1v1` or `{cmd} random` to start a fresh arena battle!"
    
    command_list.append(f'{pref}embed -title "🧹 Arena Reset" -desc "{clear_msg}" -color 0x95e1d3')
    command_list.append(f'{pref}i end')
    
    # Clear arena metadata
    c.set_metadata('arena_bets', '{}')
    
    command = f"multiline{nl}"
    command += nl.join(command_list)
    return command

# Handle battle creation - treat everything else as a format
else:
    # Check for existing combat that needs clearing
    needs_clear, warning = check_existing_combat()
    if needs_clear:
        return f'embed -title "⚠️ Arena Reset Required" -desc "{warning}" -color 0xff6b35 -thumb {image} -footer "{cmd} help | Arena Battle System"'
    
    # Parse format and difficulty - first arg is the format now
    format_str = subcommand
    difficulty = args[1] if len(args) > 1 else "Medium"
    
    # Initialize combat if not already active
    init_combat = not c
    
    # Validate difficulty
    if difficulty.title() not in ["Easy", "Medium", "Hard", "Deadly"]:
        difficulty = "Medium"
    
    # Parse the format
    battle_type, team_sizes, player_team_index = parse_arena_format(format_str)
    
    if battle_type == "invalid":
        return f'embed -title "❌ Invalid Format" -desc "Could not parse format `{format_str}`. Use `{cmd} help` for examples." -color 0xff6b35 -thumb {image} -footer "{cmd} help | Arena Battle System"'
    
    # Get players in combat
    players = get_players_in_combat()
    
    # Calculate target XP
    target_xp = calculate_target_xp(players, difficulty)
    
    # Generate battle based on type
    battle_info = None
    
    if battle_type == "random":
        # Random 2-3 team monster battle
        team_count = randint(2, 3)
        factions = select_random_factions(team_count)
        
        teams = []
        for faction in factions:
            team = build_faction_team(faction, target_xp, team_count)
            teams.append(team)
        
        battle_info = {
            'type': f"{team_count}-Way Monster Battle",
            'format': f"{team_count} Random Factions",
            'teams': teams
        }
        
    elif battle_type == "player":
        # Players + monsters vs monsters
        if not players:
            return f'embed -title "❌ No Players Found" -desc "Player mode requires players in combat initiative. Use `{pref}i join` to add players." -color 0xff6b35 -thumb {image} -footer "{cmd} help | Arena Battle System"'
        
        # Create 2 teams: players+monsters vs monsters
        factions = select_random_factions(2)
        
        # Team 1: Players + monsters
        team1 = build_faction_team(factions[0], target_xp / 2, 2)
        team1['players'] = players
        
        # Team 2: Pure monsters
        team2 = build_faction_team(factions[1], target_xp, 2)
        
        teams = [team1, team2]
        
        battle_info = {
            'type': 'Players & Monsters vs Monsters',
            'format': 'Player Alliance Battle',
            'difficulty': difficulty.title(),
            'teams': teams
        }
        
    elif battle_type == "advanced":
        # Advanced format like 1v2v3p - FIXED TO USE EXACT COUNTS WITH BALANCED XP
        team_count = len(team_sizes)
        
        if team_count < 2:
            return f'embed -title "❌ Invalid Team Count" -desc "Need at least 2 teams. Format: `{format_str}`" -color 0xff6b35 -thumb {image} -footer "{cmd} help | Arena Battle System"'
        elif team_count > 6:
            return f'embed -title "❌ Too Many Teams" -desc "Maximum 6 teams supported due to performance limits. Format: `{format_str}`" -color 0xff6b35 -thumb {image} -footer "{cmd} help | Arena Battle System"'
        
        # Check if we need players but don't have any
        if player_team_index is not None and not players:
            return f'embed -title "❌ No Players Found" -desc "Format `{format_str}` requires players in combat initiative. Use `{pref}i join` to add players." -color 0xff6b35 -thumb {image} -footer "{cmd} help | Arena Battle System"'
        
        # Select factions
        factions = select_random_factions(team_count)
        
        if len(factions) < team_count:
            return f'embed -title "❌ Insufficient Factions" -desc "Cannot create {team_count} balanced teams. Try reducing team count or use a simpler format." -color 0xff6b35 -thumb {image} -footer "{cmd} help | Arena Battle System"'
        
        teams = []
        
        # For balanced arena battles, each team should get roughly equal total XP
        # regardless of monster count, so a 1v2 fight has similar power levels:
        # - Team 1 (1 monster): Gets 1 strong monster (e.g., 400 XP)
        # - Team 2 (2 monsters): Gets 2 weaker monsters (e.g., 200 XP each = 400 total)
        # This creates tactical variety while maintaining balance
        base_team_xp = target_xp / team_count  # Equal XP per team for balance
        
        for i, (team_size, faction) in enumerate(core.zip(team_sizes, factions)):
            # FIXED: Use base_team_xp for all teams to ensure balance
            # The exact_count parameter will handle distributing this XP across monsters
            team = build_faction_team(faction, base_team_xp, team_count, exact_count=team_size)
            
            # Add players to designated team
            if i == player_team_index:
                team['players'] = players
                # Give player teams a bit more XP to account for player coordination
                team['target_xp'] = base_team_xp * 1.2
            
            teams.append(team)
        
        battle_info = {
            'type': f"{team_count}-Way Custom Battle",
            'format': format_str.upper(),
            'difficulty': difficulty.title() if players else None,
            'teams': teams
        }
    
    # Generate monster commands and return multiline
    if battle_info:
        command_list = []
        
        # Initialize combat if needed
        if init_combat:
            command_list.append(f'{pref}init begin')
        
        # Clear any existing bets
        if c:
            c.set_metadata('arena_bets', '{}')
        
        # Generate monster commands
        command_list.extend(generate_monster_commands(battle_info, players))
        
        command = f"multiline{nl}"
        command += nl.join(command_list)
        return command
    else:
        return f'embed -title "❌ Battle Generation Failed" -desc "Could not generate battle. Please try again." -color 0xff6b35 -thumb {image} -footer "{cmd} help | Arena Battle System"'
</drac2>
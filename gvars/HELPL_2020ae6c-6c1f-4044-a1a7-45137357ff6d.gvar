# Help Text
pref, al = ctx.prefix, ctx.alias
cmd = pref + al

help_title = f"{character().name} needs help breathing life into these monsters!"
# Simple Help Text
help_text = f"""**Quick Start:**
- Start combat with `{pref}i begin` and add players/monsters
- Use `{cmd}` to setup map and automate monsters
- Use `{cmd}` again to continue automation

**Basic Commands:**
- `{cmd}` - Automate all monsters until next player turn
- `{cmd} once` - Automate current monster only
- `{cmd} map list` - View available maps
- `{cmd} map <name>` - Load specific map

**Team Setup:**
- `{pref}team goblin1` - Assign goblin1 to your team
- `{pref}team 2 orc1` - Assign orc1 to Team 2
- `{pref}team ghost familiar` - Make familiar untargetable

**Arena Battles:** (auto-assigns teams)
- `{pref}arena 1v1` - Monster duel with betting
- `{pref}arena random` - Random faction warfare
- `{pref}arena bet team1 10gp` - Bet 10 gold on team 1

**Automation Control:**
- `{pref}stopauto boss1` - Pause automation on boss1's turn
- `{cmd} react` - Pause before next player for reactions

:warning: For an in-depth and comprehensive guide to `{cmd}`:
- Use: `{cmd} advanced`

*Pro Tip*: Use the [Encounter Generator](https://avrae.io/dashboard/workshop/654fbc27ac7cd2bc90723133/) for balanced encounters

**Community & Support**
- Support the OTFBM map service: [OTFBM Patreon](https://www.patreon.com/otfbm)
- Support alias development: [Ko-fi Support Page](https://ko-fi.com/hedy4u)

Need help or have questions?
Join our [🤖 Auto Monster AI - Discord Support Server](https://discord.gg/E3rYxfCVH8)
"""

advanced_help_text = f"""**CORE COMMANDS**
`{cmd}` - Automate all monsters until next player turn
`{cmd} once` | `{cmd} o` - Automate current monster only
`{cmd} react` | `{cmd} r` - Automate until next player, pause for reactions
`{cmd} help` | `{cmd} ?` - Show basic help
`{cmd} advanced` - Show this complete reference
`{cmd} lair` - Add Lair Actions object at initiative 20

**MAP SYSTEM**
`{cmd}` - Auto-setup map and place all combatants
`{cmd} map <name>` - Load specific preset map (forest, arena, winter, etc.)
`{cmd} map list` | `{cmd} m list` - List available preset maps
`{cmd} m <name>` - Shorthand for map loading

**TEAM MANAGEMENT**
`{pref}team <combatant>` - Assign to Team 1 (your team)
`{pref}team <number> <combatant>` - Assign to specific team (1-6)
`{pref}team 0 <combatant>` - Reset team assignment
`{pref}team <number> "all:<monster_type>"` - Bulk assign all monsters of type
`{pref}team <number> <name1> <name2>` - Assign multiple combatants to team
`{pref}team ghost <combatant>` - Toggle untargetable status
`{pref}team ghost "all:<monster_type>"` - Bulk toggle ghost status

**AUTOMATION CONTROL**
`{pref}stopauto <combatant>` - Stop automation on monster's turn
`{pref}stopauto "all:<monster_type>"` - Stop automation for all monster type
`{pref}stopauto <name1> <name2>` - Stop automation for multiple monsters
`{pref}stopauto -clear <combatant>` - Re-enable automation
`{pref}stopauto -clear "all:<monster_type>"` - Re-enable for all monster type

**ARENA BATTLES**
`{pref}arena 1v1` - Monster duel
`{pref}arena 2v2` - Team battle  
`{pref}arena random` - Random faction warfare
`{pref}arena player [difficulty]` - Players + monsters vs monsters
`{pref}arena <format>` - Custom formats (1v2, 1v2v3, 1v2p, etc.)
`{pref}arena clear` | `{pref}arena end` - Clear arena and refund bets
`{pref}arena help` - Basic arena help
`{pref}arena advanced` - Detailed arena help

**ARENA DIFFICULTY LEVELS** (for player battles)
`easy` - Weaker monsters for new players
`medium` - Balanced encounters (default)
`hard` - Challenging but fair fights
`deadly` - Maximum difficulty encounters

**BETTING SYSTEM**
`{pref}arena bet team<X> <amount><currency>` - Place bet (cp/sp/gp/pp)
`{pref}arena collect` | `{pref}arena collect bets` | `{pref}arena collectbets` - Collect winnings
`{pref}arena bets` | `{pref}arena betting` | `{pref}arena status` - Show betting status

**ADVANCED USAGE WITH ARGUMENTS**
`{cmd} o -t <target>` - Override random target selection
`{cmd} o -t player1 adv` - Target player1 with advantage
`{cmd} o -t player2 dis` - Target player2 with disadvantage
`{cmd} o -rr 2` - Reroll 2 dice on attacks
`{cmd} o guidance` - Add guidance bonus
`{cmd} o bless` - Add bless bonus
`{cmd} o magical` - Treat attacks as magical
All `{pref}init attack` arguments work with `{cmd} once`

**AUTO-APPLIED EFFECTS**
- `Ally (auto)` - Team 1 assignment (players and allies)
- `Team 2 (auto)` - Team 2 assignment (default for monsters)
- `Team 3 (auto)` through `Team 6 (auto)` - Additional team assignments
- `Ghost (auto)` - Untargetable status (familiars, summons, etc.)
- `Stop Automation (auto)` - Pauses automation on monster's turn

**USAGE EXAMPLES**
• `{pref}team 2 "all:orc"` - All orcs join Team 2
• `{pref}team 3 goblin1 goblin2` - Assign both goblins to Team 3
• `{pref}arena 1v2p medium` - 1 monster vs 2 monsters + players (medium difficulty)
• `{pref}arena bet team1 25gp` - Bet 25 gold on team 1
• `{pref}stopauto boss1` - Pause automation when boss1's turn comes up
• `{cmd} o -t player1 adv guidance` - Target player1 with advantage + guidance bonus

**COMPATIBILITY & LIMITS**
- Supports D&D 2014 & 2024 Monsters (auto-detects `{pref}servsettings`)
- Maximum 10 automated attacks per execution
- Supports up to 6 teams simultaneously
- `{cmd} once` compatible with all standard `{pref}init` arguments

**COMMUNITY & SUPPORT**
- Support the OTFBM map service: [OTFBM Patreon](https://www.patreon.com/otfbm)
- Support alias development: [Ko-fi Support Page](https://ko-fi.com/hedy4u)

Need help or have questions?
Join our [🤖 Auto Monster AI - Discord Support Server](https://discord.gg/E3rYxfCVH8)"""
no_map = f"""
> *Note*: `{cmd}` now comes with a new update integrating OTFBM map-based combat with a full AI battle engine! If you'd still like to use the old legacy version without maps support, worry not, it is still live on:
> `{pref}autol` (`l` stands for legacy)
\n__**Suggested Actions**__:
- For monsters with Lair Actions, add a Lair object with `{cmd} lair`
- Check out how to assign teams with `{pref}team`.
\nChoose from one of the many map presets:
`{cmd} map list`
### __Quick Setup Tips__
- **Random Map:** `{cmd}`
- **Small Map**: `{cmd} map arena`
- **Medium Map**: `{cmd} map winter` / `{cmd} map sky` / `{cmd} map silent`
- **Large Map**: `{cmd} map large`
\n__Note__: Using any of the above quick setup commands will automatically add all players and monsters currently in the combat initiative to either end of the map.
\n:warning: Make sure to add all the players and monsters to combat initiative before loading the map with one of the above commands for a seamless assignment of combat positions.
"""

no_players = f"""No playable characters found within Combat Initiative to target!

Please join the combat initiative using `{pref}i join` or remove ghost effect from characters.
"""

move_help = f"""
        
To move your player character on the map:

1. Ensure that you or the server you are in is subscribed to the `{pref}map` alias.
    - You can quickly add it as a personal alias using:
    ```{pref}alias subscribe https://avrae.io/dashboard/workshop/5f6a4623f4c89c324d6a5cd3```

2. Move your character using the `{pref}move` alias: (companion alias to `{pref}map`)
    - For example:
```{pref}move C4```
(Replace "C4" with the cell address of your desired location on the map.)
"""

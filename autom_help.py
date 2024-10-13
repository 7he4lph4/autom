# Help Text
pref, al = ctx.prefix, ctx.alias
cmd = pref + al

help_title = f"{character().name} needs help breathing life into these monsters!"
help_text = f"""How to use `{cmd}`:

- Start combat initiative with `{pref}i begin`, and add all the necessary players and monsters
    - *Pro Tip*: use the [Encounter Generator](https://avrae.io/dashboard/workshop/654fbc27ac7cd2bc90723133/) alias to quickly setup a balanced encounter for any party
- Once all monsters and players are added, use `{cmd}` to auto-magically add the *Map* combatant
- Use `{cmd} map list` to see all preset maps
- Use `{cmd} map <map name>` to load one of the preset maps
- Or, simply use `{cmd}` again to randomly pick one of the preset maps
    - (ideally you can keep spamming `{cmd}` after adding all players and monsters to combat initiative)
- Use `{cmd}` to automate all monsters until the next player in combat initiative

*Note*: If you'd like to keep using the old alias without maps support, you can use:
`{pref}autol`
(`l` stands for legacy)

This alias relies on the OTFBM backend service for map generation. They have server costs to cover, so please consider supporting their work through their [Patreon page](https://www.patreon.com/otfbm) if you're able

You can also support the development of this alias on [Ko-fi](https://ko-fi.com/hedy4u)!
"""

no_map = f"""
> *Note*: `{cmd}` now comes with a new update integrating OTFBM map-based combat with a full AI battle engine! If you'd still like to use the old legacy version without maps support, worry not, it is still live on:
> `{pref}autol` (`l` stands for legacy)
\n__**Suggested Actions**__:
\nIf you are fighting a monster with Lair Actions, add a Lair object with:
`{cmd} lair`
\nChoose from one of the many map presets:\n`{cmd} map list`
### __Quick Setup Tips__
- **Random Map:** `{cmd}`
- **Small Map**: `{cmd} map pit`
- **Medium Map**: `{cmd} map winter` / `{cmd} map sky` / `{cmd} map silent`
- **Large Map**: `{cmd} map light`
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

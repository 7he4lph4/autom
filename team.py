<drac2>
args = &ARGS&
pref, al = ctx.prefix, ctx.alias
cmd = pref + al


if (len(args) < 1
    or (len(args) == 1 and args[0].isdigit())
    or args[0].casefold() in ["help", "h", "?"]
):
    return f'''embed -title "Set Teams for Automation" -desc "
Players without an assigned team, as well as monsters with the `Ally (auto)` effect, will default to Team 1. Monsters without an assigned team will default to the highest team number greater than 1, or Team 2 if there are none.

**Usage Examples:**
- `{cmd} as1` assigns AS1 to your team.
- `{cmd} 1 as1` assigns AS1 to Team 1.
- `{cmd} 2 \\"all:awakened shrub\\"` assigns all Awakened Shrubs to Team 2.
- `{cmd} 3 as1 all:badger` assigns AS1 and all Badgers to Team 3.
- `{cmd} 0 \\"all:awakened shrub\\"` resets teams for all Awakened Shrubs.

Ghosts are ignored by automation:
- `{cmd} ghost \\"all:awakened shrub\\"` sets all Awakened Shrubs to Ghost.\nRun the command again to remove the Ghost effect."
-footer "{cmd}"'''

c = combat()
if not c:
    return f'embed -title "Unable to Assign Teams" -desc "No combat found." -footer "{cmd}"'

team = 1
if args[0].isdigit():
    team = int(args.pop(0))
elif "ghost" in args[0].casefold():
    team = "ghost"
elif c.me:
    for effect in c.me.effects:
        if effect.name.startswith("Team "):
            team = int("".join([e for e in effect.name if e.isdigit()]))
            break

teammates = []
for a in args:
    if a.startswith("all:"):
        monster_name = a[4:].lower()
        for combatant in c.combatants:
            if combatant.monster_name and combatant.monster_name.lower() == monster_name:
                teammates.append(combatant)
    else:
        combatant = c.get_combatant(a)
        if combatant:
            teammates.append(combatant)

command = 'multiline\n!embed -title "'
if team == "ghost":
    ghost = False
    for t in teammates:
        for e in t.effects:
            if "Ghost (auto)" in e.name:
                t.remove_effect(e.name)
                break
        else:
            ghost = True
    if ghost:
        for t in teammates:
            t.add_effect("Ghost (auto)")
        command += 'Set Ghosts" -desc "**Set Ghosts ignored by automation:**\n'
    else:
        command += 'Unset Ghosts" -desc "**Unset Ghosts ignored by automation:**\n'
else:
    for t in teammates:
        for effect in t.effects:
            if "Ally (auto)" in effect.name or all(
                e in effect.name for e in ["Team", "(auto)"]
            ):
                t.remove_effect(effect.name)
        if 0 < team:
            t.add_effect("Ally (auto)" if team == 1 else f"Team {team} (auto)")
    command += f"Set Team {team}" if 0 < team else "Reset Teams"
    command += (
        f'" -desc "Added combatants to Team {team}:\n'
        if 0 < team
        else f'" -desc "Reset combatant Teams:\n'
    )
return command + ", ".join([t.name for t in teammates]) + '"\n!i list'
</drac2>
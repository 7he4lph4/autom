<drac2>
args = &ARGS&
pref, al = ctx.prefix, ctx.alias
cmd = pref + al

if len(args) < 1:
    return (
        (
            'embed -title "Set Monsters to Stop Automation" -desc "'
            + f"""
Monsters with the `Stop Automation (auto)` effect will stop automation.
Add `-clear` to re-enable automation for monsters.

**Usage Examples:**
- `{cmd} as1` stops automation on AS1's turn.
- `{cmd} \\"all:awakened shrub\\"` stops automation on the turns of all Awakened Shrubs.
- `{cmd} as1 all:badger` stops automation on the turns of AS1 and all Badgers.
- `{cmd} -clear \\"all:awakened shrub\\"` re-enables automation for all Awakened Shrubs."""
        )
        + f'" -footer "{cmd}"'
    )

if not combat():
    err("Channel is not in combat!")

monsters, names = [], []
for a in args:
    if a.startswith("all:"):
        monsters.append(a[4:].lower())
    else:
        names.append(a.lower())

teammates = [
    c
    for c in combat().combatants
    if c.name.lower() in names
    or (c.monster_name and c.monster_name.lower() in monsters)
]

stop_auto = not all([t.get_effect("Stop Automation (auto)") for t in teammates])
if "-clear" in args:
    stop_auto = False

commands = ["multiline"]
embed = "embed -title "

command = 'multiline\n!embed -title "'

for t in teammates:
    for effect in t.effects:
        if "Stop Automation (auto)" in effect.name:
            t.remove_effect(effect.name)
    if stop_auto:
        t.add_effect("Stop Automation (auto)")

embed += (
    f""""Set Monsters to Stop Automation" -desc "**Automation will stop on these combatants' turns:**\n"""
    if stop_auto
    else """"Cleared Stop Automation for Monsters" -desc "**Automation will no longer stop on these combatants' turns:**\n"""
)
embed += ", ".join([t.name for t in teammates]) + f'" -footer "{cmd}"'
commands += [embed, "i list"]
return "\n!".join(commands)
</drac2>

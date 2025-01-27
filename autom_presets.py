# Auto Map Presets

using(
    core="49f5f503-1c00-4f24-ba43-92e65c2c2fb6",
    mapl="51af2e97-64e3-444a-994c-61c45c3f0994",
)

### DEPRECATED BBCODE ###
bbcode = """
[url=https://ibb.co/TW0G3zm][img]https://i.ibb.co/y4kCjLW/Arena-of-Earth-Desert-Day-32x24.jpg[/img][/url]
[url=https://ibb.co/KxbXvj7][img]https://i.ibb.co/yFdXjn5/Arena-of-Earth-Desert-Night-32x24.jpg[/img][/url]
[url=https://ibb.co/h87YZkY][img]https://i.ibb.co/s3mW6hW/Arena-of-Earth-Jade-Day-32x24.jpg[/img][/url]
[url=https://ibb.co/wLLbXvd][img]https://i.ibb.co/PYYbnSr/Arena-of-Earth-Jade-Day-Retracted-Stairs-Overlay-22x22.jpg[/img][/url]
[url=https://ibb.co/r4nZSNZ][img]https://i.ibb.co/PwB5n05/Beach-Dunes-32x22.jpg[/img][/url]
[url=https://ibb.co/Jzk5ghD][img]https://i.ibb.co/1928jSF/Crab-Rock-Seaside-Clear-31x23.jpg[/img][/url]
[url=https://ibb.co/1Qxrqx1][img]https://i.ibb.co/NCz9jz5/Crab-Rock-Seaside-Dreary-31x23.jpg[/img][/url]
[url=https://ibb.co/zXph82q][img]https://i.ibb.co/F52bsYR/Crystal-Hill-25x17.jpg[/img][/url]
[url=https://ibb.co/YdkQNLf][img]https://i.ibb.co/8x5sm7P/Desert-Island-Tropical-Day-31x23.jpg[/img][/url]
[url=https://ibb.co/28sWx1B][img]https://i.ibb.co/5YnGmgV/Desert-Island-Tropical-Night-31x23.jpg[/img][/url]
[url=https://ibb.co/JRZ7xF0][img]https://i.ibb.co/hR0WX1h/Desert-Crossroads-Gridded-32x21-Map-Public.jpg[/img][/url]
[url=https://ibb.co/GkNRynS][img]https://i.ibb.co/DkTQhz2/Desert-Oasis-25x17.jpg[/img][/url]
[url=https://ibb.co/HP0WHpT][img]https://i.ibb.co/gWG5RFZ/Fallen-Star-Fallen-Star-Day-31x23.jpg[/img][/url]
[url=https://ibb.co/xYGP0dH][img]https://i.ibb.co/jzGB2sR/Fallen-Star-Fallen-Star-Night-31x23.jpg[/img][/url]
[url=https://ibb.co/cwHBJZb][img]https://i.ibb.co/bFZ01CH/Fighting-Pit-Muddy-Dark-16x10.jpg[/img][/url]
[url=https://ibb.co/TYZ5BfR][img]https://i.ibb.co/ckPdcBt/Fighting-Pit-Muddy-Light-27x18.jpg[/img][/url]
[url=https://ibb.co/QfDRW0s][img]https://i.ibb.co/KXKktnC/Green-Hill-Old-Oak-Day-32x22.jpg[/img][/url]
[url=https://ibb.co/m8WP5p4][img]https://i.ibb.co/FVTd4pz/Green-Hill-Old-Oak-Day-Canopy-32x22.jpg[/img][/url]
[url=https://ibb.co/cbt4BrT][img]https://i.ibb.co/FsJRrD7/Green-Hill-Old-Oak-Night-32x22.jpg[/img][/url]
[url=https://ibb.co/qdNLyQm][img]https://i.ibb.co/37p5rZS/Green-Hill-Old-Oak-Night-Canopy-32x22.jpg[/img][/url]
[url=https://ibb.co/hX4vtyV][img]https://i.ibb.co/B4QRStB/Greybanner-Coliseum-Day-Large-31x23.jpg[/img][/url]
[url=https://ibb.co/SXPg6tx][img]https://i.ibb.co/Rp9Kg3S/Greybanner-Coliseum-Day-Small-22x16.jpg[/img][/url]
[url=https://ibb.co/WcxKM9g][img]https://i.ibb.co/qRy1cGk/Haunted-Marsh-26x18.jpg[/img][/url]
[url=https://ibb.co/7YCTjgy][img]https://i.ibb.co/0D2WmBJ/Hillside-Altar-26x18.jpg[/img][/url]
[url=https://ibb.co/xCY248P][img]https://i.ibb.co/r73QWfT/Hillside-Cave-26x19.jpg[/img][/url]
[url=https://ibb.co/DMJzKby][img]https://i.ibb.co/6tMrsZx/Jungle-River-Crossing-Lily-Field-Day-23x16.jpg[/img][/url]
[url=https://ibb.co/gd5qtgH][img]https://i.ibb.co/9hFKyYz/Jungle-River-Crossing-Lily-Field-Night-23x16.jpg[/img][/url]
[url=https://ibb.co/8D9L3XH][img]https://i.ibb.co/7JKdcbq/Lakebed-Monolith-26x18.jpg[/img][/url]
[url=https://ibb.co/sjRX6Hm][img]https://i.ibb.co/LSRsJ5k/Ocean-calm-16x16.jpg[/img][/url]
[url=https://ibb.co/k6k5Y3G][img]https://i.ibb.co/Z1tGyHf/Ocean-nighttime-16x16.jpg[/img][/url]
[url=https://ibb.co/L9R6wjS][img]https://i.ibb.co/6Dwbh9Y/Ocean-rough-16x16.jpg[/img][/url]
[url=https://ibb.co/fGGDFNG][img]https://i.ibb.co/7NNkCpN/Ocean-storm-16x16.jpg[/img][/url]
[url=https://ibb.co/FhGjdRg][img]https://i.ibb.co/nwh5Kxz/Ocean-tropical-16x16.jpg[/img][/url]
[url=https://ibb.co/qrwWPwj][img]https://i.ibb.co/4VxY5xt/Pumpkin-Hill-26x18.jpg[/img][/url]
[url=https://ibb.co/HY9r0Y2][img]https://i.ibb.co/J2SzN2d/Roadside-Rise-26x20.jpg[/img][/url]
[url=https://ibb.co/m63dq69][img]https://i.ibb.co/qkvhskN/Shattered-Sky-Astral-Blue-Star-Background-22x16.jpg[/img][/url]
[url=https://ibb.co/XjqfPCr][img]https://i.ibb.co/zQzWg4T/Shattered-Sky-Astral-Red-Star-Background-22x16.jpg[/img][/url]
[url=https://ibb.co/VNQDkT0][img]https://i.ibb.co/7zRV0Kx/Shattered-Sky-Astral-Sea-Blue-Star-22x16.jpg[/img][/url]
[url=https://ibb.co/TRjdMTM][img]https://i.ibb.co/mtZg5B5/Shattered-Sky-Astral-Sea-Red-Star-22x16.jpg[/img][/url]
[url=https://ibb.co/qxwPXQD][img]https://i.ibb.co/mS7M1WR/Shifting-Swamp-Jungle-26x18.jpg[/img][/url]
[url=https://ibb.co/y4Xd3yh][img]https://i.ibb.co/0scmwMB/Shifting-Swamp-26x18.jpg[/img][/url]
[url=https://ibb.co/y859r1w][img]https://i.ibb.co/WcFhLwb/Silent-Snowy-Cemetery-26x18.jpg[/img][/url]
[url=https://ibb.co/ZK0FL8J][img]https://i.ibb.co/NpMJVj3/Sinister-Woodland-Swamp-Day-Closed-31x23.jpg[/img][/url]
[url=https://ibb.co/kHCZN9n][img]https://i.ibb.co/6nCQj1h/Sinister-Woodland-Swamp-Day-Open-31x23.jpg[/img][/url]
[url=https://ibb.co/q5xG7m3][img]https://i.ibb.co/GTFwnC4/Sinister-Woodland-Swamp-Night-Closed-31x23.jpg[/img][/url]
[url=https://ibb.co/bQgRFJW][img]https://i.ibb.co/4KZg2dm/Sinister-Woodland-Swamp-Night-Open-31x23.jpg[/img][/url]
[url=https://ibb.co/y8mQLt2][img]https://i.ibb.co/JzWsXVZ/Winter-Wilderness-Lonely-Oak-Day-A-25x18.jpg[/img][/url]
[url=https://ibb.co/FmZftmS][img]https://i.ibb.co/BcW7RcX/Winter-Wilderness-Lonely-Oak-Day-B-25x18.jpg[/img][/url]
[url=https://ibb.co/3Nn9wyC][img]https://i.ibb.co/QN43ZFK/Winter-Wilderness-Lonely-Oak-Night-A-25x18.jpg[/img][/url]
[url=https://ibb.co/PWNMF7m][img]https://i.ibb.co/4S72K6m/Winter-Wilderness-Lonely-Oak-Night-B-25x18.jpg[/img][/url]
"""


map_data = {
    "Arena Of Earth Desert Day": {"size": "16x12", "image": "https://live.staticflickr.com/65535/54283121081_68314133e4_c.jpg"},
    "Arena Of Earth Desert Night": {"size": "16x12", "image": "https://live.staticflickr.com/65535/54283121021_4be7bd4d80_c.jpg"},
    "Arena Of Earth Jade Day": {"size": "16x12", "image": "https://live.staticflickr.com/65535/54283544950_f2de74070e_c.jpg"},
    "Arena Of Earth Jade Day Retracted Stairs Overlay": {"size": "16x16", "image": "https://live.staticflickr.com/65535/54282231892_b84927d724_c.jpg"},
    "Beach Dunes": {"size": "32x22", "image": "https://live.staticflickr.com/65535/54283367093_1e25e56240_h.jpg"},
    "Crab Rock Seaside Clear": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54282231882_ae4cd236ca_b.jpg"},
    "Crab Rock Seaside Dreary": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54283357524_ae886bf1d9_b.jpg"},
    "Crystal Hill": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54282231427_1353bdff4a_b.jpg"},
    "Desert Crossroads Gridded Map Public": {"size": "20x13", "image": "https://live.staticflickr.com/65535/54283544970_52fb57f448_b.jpg"},
    "Desert Island Tropical Day": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54283121506_667a5e0346_b.jpg"},
    "Desert Island Tropical Night": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54283367433_fe213bab13_b.jpg"},
    "Desert Oasis": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54283356989_07c436a612_b.jpg"},
    "Fallen Star Fallen Star Day": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54283367448_9888545087_b.jpg"},
    "Fallen Star Fallen Star Night": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54283357469_205773d0cd_b.jpg"},
    "Fighting Pit Muddy Dark": {"size": "20x12", "image": "https://live.staticflickr.com/65535/54282231327_1cc640d4cf_b.jpg"},
    "Fighting Pit Muddy Light": {"size": "22x14", "image": "https://live.staticflickr.com/65535/54283366878_4ebed98257_o.jpg"},
    "Green Hill Old Oak Day": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54282231792_2463dd423b_b.jpg"},
    "Green Hill Old Oak Day Canopy": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54283367333_88dc9bf00d_b.jpg"},
    "Green Hill Old Oak Night": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54283367308_b34775b44f_b.jpg"},
    "Green Hill Old Oak Night Canopy": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54283357384_d8b6334047_b.jpg"},
    "Greybanner Coliseum Day Large": {"size": "32x23", "image": "https://live.staticflickr.com/65535/54283367323_a30865b35c_h.jpg"},
    "Greybanner Coliseum Day Small": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54283121376_1a04e52939_b.jpg"},
    "Haunted Marsh": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54283366958_f42eca5b89_b.jpg"},
    "Hillside Altar": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54283120881_39125dfdfc_b.jpg"},
    "Hillside Cave": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54283366813_df8bd3722b_b.jpg"},
    "Jungle River Crossing Lily Field Day": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54283121406_371a3ff40e_b.jpg"},
    "Jungle River Crossing Lily Field Night": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54282231702_a5ef052bfb_b.jpg"},
    "Lakebed Monolith": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54283356979_1833580b11_b.jpg"},
    "Ocean Calm": {"size": "16x16", "image": "https://live.staticflickr.com/65535/54282231677_cf72a9d14f_c.jpg"},
    "Ocean Nighttime": {"size": "16x16", "image": "https://live.staticflickr.com/65535/54282231642_b6ac409f92_c.jpg"},
    "Ocean Rough": {"size": "16x16", "image": "https://live.staticflickr.com/65535/54283545075_d2df331017_c.jpg"},
    "Ocean Storm": {"size": "16x16", "image": "https://live.staticflickr.com/65535/54283545110_d7accd4c79_c.jpg"},
    "Ocean Tropical": {"size": "16x16", "image": "https://live.staticflickr.com/65535/54283121251_a51af52cec_c.jpg"},
    "Pumpkin Hill": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54283356929_60b3db522e_b.jpg"},
    "Roadside Rise": {"size": "20x15", "image": "https://live.staticflickr.com/65535/54283120676_b788ca562e_b.jpg"},
    "Shattered Sky Astral Blue Star Background": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54283357264_931cfe3d21_b.jpg"},
    "Shattered Sky Astral Red Star Background": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54283367158_b8db23c1fb_b.jpg"},
    "Shattered Sky Astral Sea Blue Star": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54283367188_4874a0d0d2_b.jpg"},
    "Shattered Sky Astral Sea Red Star": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54283121141_2809b39b4e_b.jpg"},
    "Shifting Swamp Jungle": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54283121131_35d8824810_b.jpg"},
    "Shifting Swamp": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54283120701_f0e4727d5d_b.jpg"},
    "Silent Snowy Cemetery": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54283367143_c78ace08fb_b.jpg"},
    "Sinister Woodland Swamp Day Closed": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54283367138_16de39e282_b.jpg"},
    "Sinister Woodland Swamp Day Open": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54283366763_4a343e9983_b.jpg"},
    "Sinister Woodland Swamp Night Closed": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54283544535_8a51601722_b.jpg"},
    "Sinister Woodland Swamp Night Open": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54283356799_a5e5e72ea7_b.jpg"},
    "Winter Wilderness Lonely Oak Day A": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54283120581_5eac27568c_b.jpg"},
    "Winter Wilderness Lonely Oak Day B": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54283356774_a8c4fb3c68_b.jpg"},
    "Winter Wilderness Lonely Oak Night A": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54282231167_18afeb6e61_b.jpg"},
    "Winter Wilderness Lonely Oak Night B": {"size": "20x14", "image": "https://live.staticflickr.com/65535/54282231152_9f5369fc4e_b.jpg"}
}


def extract_map_info():
    cell_pixel = "c50"  # Default cell pixel value
    map_dict = {}
    for name, data in map_data.items():
        map_dict[name] = {
            "cell_pixel": cell_pixel,
            "size": data["size"],
            "image": data["image"]
        }
    return map_dict

map_presets = extract_map_info()

def get_cell_pixel(size, map_name):
    return "c50"


map_presets = extract_map_info()


def initialize_map(map_name, map_state):
    if map_name in map_presets:
        map_state["current_map"] = map_name
        map_state["size"] = map_presets[map_name]["size"]
        map_state["mapoptions"] = map_presets[map_name]["cell_pixel"]
        map_state["bg_image"] = map_presets[map_name]["image"]
        return map_state["size"], map_state["bg_image"], map_state["mapoptions"]
    return None, None, None


def find_map_by_subtext(subtext):
    subtext_l = subtext.lower()
    matches = [name for name in map_presets if subtext_l in name.lower()]
    matches = core.bubble_sort(matches)
    name, data = "", None
    if 0 < len(matches):
        name, data = matches[0], map_presets[matches[0]]
    return name, data, matches


def generate_list_embeds(footer):
    pref, al = ctx.prefix, ctx.alias
    cmd = pref + al
    # Generate the list of map options
    map_list = [f'**{m}** ({map_presets[m]["size"]})' for m in map_presets]
    map_list = core.bubble_sort(map_list)
    map_list.append(
        f'\n__Usage Example__:\n`{cmd} map \\"Silent Snowy Cemetery\\"`\n(or)\n`{cmd} m sil`\n\n**Map-Art Courtesy of**:\n[2-Minute Tabletop](https://2minutetabletop.com/) under the [CC BY-NC 4.0 License](https://creativecommons.org/licenses/by-nc/4.0/)\nFeel free to check their other maps if you like this type of map art!'
    )

    # Split the list into chunks of 20 maps each
    chunk_size = 60
    chunks = [map_list[i : i + chunk_size] for i in range(0, len(map_list), chunk_size)]
    return [
        (
            f'{pref}embed -title "Available Map Presets (Page {i+1}/{len(chunks)})" -desc "'
            + "\n".join(chunk)
            + f'" -footer "{footer}"'
        )
        for i, chunk in enumerate(chunks)
    ]


def load_specific_map(map_state, map_attach, map_name=""):
    if not map_name:
        map_name = randchoice(list(map_presets.keys()))
    map_name, map_data, matches = find_map_by_subtext(map_name)
    error_base = '-title "Map Setup Pending:" -desc '
    if not matches:
        return (
            error_base
            + f'''"No maps found matching '{map_name}'. Use `{ctx.prefix + ctx.alias} map list` to see available maps."'''
        )

    # Update map_state with new map data
    map_state["current_map"] = map_name
    map_state["size"] = map_data["size"]
    map_state["mapoptions"] = map_data["cell_pixel"]
    map_state["bg_image"] = map_data["image"]

    # Update the map effect on the map attach
    neweffect = f"Size: {map_state['size']} ~ Background: {map_state['bg_image']} ~ Options: {map_state['mapoptions']}"
    map_attach.remove_effect("map")
    map_attach.add_effect(
        "map",
        attacks=[
            {
                "attack": {
                    "name": "map",
                    "automation": [{"type": "text", "text": neweffect}],
                    "_v": 2,
                }
            }
        ],
    )
    base_message = f"`{map_name}` map loaded successfully. Combat positions assigned.\n\n**Map-Art Courtesy of**:\n[2-Minute Tabletop](https://2minutetabletop.com/) under the [CC BY-NC 4.0 License](https://creativecommons.org/licenses/by-nc/4.0/)"
    if len(matches) > 1:
        other_matches = "\n".join(matches[1:])
        base_message += f"\n\nYou may also be looking for: ```{other_matches}```"
    return f'-title "Map Updated" -desc "{base_message}"'


def get_channel_name():
    if ctx.channel.parent:
        return ctx.channel.parent.name
    return ctx.channel.name

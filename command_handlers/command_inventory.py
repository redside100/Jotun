import discord
import items.item_map as item_map

class_colors = {
    'None': 9807270,
    'Knight': 0xC0C0C0,
    'Priest': 3066993,
    'Wizard': 3447003,
    'Paladin': 0xF8C300
}


# Inventory command
async def handle(message, db):
    id = message.author.id
    name = message.author.name
    info = db.get_player_info(id)

    if info is None:
        db.add_new_player(id)
        info = db.get_player_info(id)

    embed = discord.Embed(title="{}'s Inventory".format(name), description="Class: {}".format(info['class']), color=class_colors[info['class']])
    embed.set_thumbnail(url=message.author.avatar_url)
    content = "\u200B"

    for item_id in info['items']:
        item = item_map.item_map[item_id]()
        content += "{} {} (x{})\n".format(item.get_emoji(), item.get_name(), info['items'][item_id])

    if content == "\u200B":
        content = "_(Empty)_"

    embed.add_field(name="\u200B", value=content)
    await message.channel.send(embed=embed)

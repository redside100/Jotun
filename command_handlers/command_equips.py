import discord
import items.item_map as item_map

class_colors = {
    'None': 9807270,
    'Knight': 0xC0C0C0,
    'Priest': 3066993,
    'Wizard': 3447003,
    'Paladin': 0xF8C300
}


# Equips command
async def handle(message, db):
    id = message.author.id
    name = message.author.name
    info = db.init_info_check(message)

    embed = discord.Embed(title="{}'s Equips".format(name),
                          description="Class: {}".format(info['class']), color=class_colors[info['class']])
    embed.set_thumbnail(url=message.author.avatar_url)
    content = "\u200B"

    for item_id in info['equips']:
        item = item_map.item_map[item_id]()
        content += "{} {}\n".format(item.get_emoji(), item.get_name())

    if content == "\u200B":
        content = "_(Empty)_"

    embed.add_field(name="\u200B", value=content)
    await message.channel.send(embed=embed)

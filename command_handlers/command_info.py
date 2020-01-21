import discord
import messages


class_colors = {
    'None': 9807270,
    'Knight': 0xC0C0C0,
    'Priest': 3066993,
    'Wizard': 3447003,
    'Paladin': 0xF8C300
}


# Info command
async def handle(message, db):
    id = message.author.id
    name = message.author.name
    info = db.init_info_check(message)


    embed = discord.Embed(title=name, description="Class: {}".format(info['class']), color=class_colors[info['class']])
    embed.set_thumbnail(url=message.author.avatar_url)
    embed.add_field(name="**HP** :heart:", value="{}/{}".format(info['hp'], info['max_hp']))
    embed.add_field(name="**MP** {}".format(messages.data['emoji_mana']), value="{}/{}".format(info['mp'], info['max_mp']))
    embed.add_field(name="\u200B", value="\u200B")
    embed.add_field(name="**ATK** :crossed_swords:", value=info['atk'])
    embed.add_field(name="**EVA** :dash:", value=info['eva'])
    embed.add_field(name="\u200B", value="\u200B")
    embed.add_field(name="**Level** {}".format(messages.data['emoji_level']), value=info['level'])
    embed.add_field(name="**XP** {}".format(messages.data['emoji_xp']), value="{}/{}".format(info['xp'], info['xp_to_next']))
    embed.add_field(name="**Gold** {}".format(messages.data['emoji_gold']), value="{}".format(info['gold']), inline=True)

    await message.channel.send(embed=embed)

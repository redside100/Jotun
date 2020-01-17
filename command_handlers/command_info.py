import discord


class_colors = {
    'None': 9807270
}


# Info command
async def handle(message, db):
    id = message.author.id
    name = message.author.name
    info = db.get_player_info(id)

    if info is None:
        db.add_new_player(id)
        info = db.get_player_info(id)

    embed = discord.Embed(title=name, description="Class: {}".format(info['class']), color=class_colors[info['class']])
    embed.set_thumbnail(url=message.author.avatar_url)
    embed.add_field(name="**HP**", value="{}/{}".format(info['hp'], info['max_hp']))
    embed.add_field(name="**MP**", value="{}/{}".format(info['mp'], info['max_mp']))
    embed.add_field(name="\u200B", value="\u200B")
    embed.add_field(name="**Level**", value=info['level'])
    embed.add_field(name="**XP**", value="{}/{}".format(info['xp'], info['xp_to_next']))
    embed.add_field(name="**Gold**", value="{}".format(info['gold']), inline=True)

    await message.channel.send(embed=embed)

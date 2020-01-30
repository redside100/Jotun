import messages
import items.item_map as item_map
import discord


# Shop command
async def handle(message, db):
    embed = discord.Embed(title="Shop")
    # TODO Replace avatar with shop image
    embed.set_thumbnail(url=message.author.avatar_url)
    content = "\u200B"

    for item_name in item_map.item_shop_map:
        item = item_map.item_shop_map[item_name]()
        content += "{} {} ({} x{})\n".format(item.get_emoji(), item.get_name(), messages.data['emoji_gold'],
                                             item.get_gold_amount())

    embed.add_field(name="\u200B", value=content)
    await message.channel.send(embed=embed)

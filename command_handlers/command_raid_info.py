import discord
import messages
import raids.raid_manager as raid_manager
from entities.raid_boss import BossTier

tier_colors = {
    BossTier.COMMON: 0xC0C0C0,
    BossTier.RARE: 0x33B8FF,
    BossTier.EPIC: 0x7A33FF,
    BossTier.LEGENDARY: 0xFFB533,
    BossTier.MYTHICAL: 0xFF3333
}


# Get server raid info
async def handle(message, db):
    id = message.author.id
    server_id = message.guild.id
    info = db.init_info_check(message)

    if not raid_manager.has_raid(server_id):
        await message.channel.send(messages.data['no_raid'])
        return

    raid_boss = raid_manager.get_raid(server_id).get_raid_boss()

    embed = discord.Embed(title=raid_boss.get_name(), description="Tier: {}".format(raid_boss.get_tier().value),
                          color=tier_colors[raid_boss.get_tier()])
    embed.set_thumbnail(url=raid_boss.get_url())
    embed.add_field(name="**HP** :heart:", value="{}/{}".format(raid_boss.get_hp(), raid_boss.get_max_hp()))
    embed.add_field(name="**Level** {}".format(messages.data['emoji_level']), value=raid_boss.get_level())
    embed.add_field(name="\u200B", value="\u200B")
    embed.add_field(name="**ATK** :crossed_swords:", value=raid_boss.get_atk())
    embed.add_field(name="**EVA** :dash:", value=raid_boss.get_eva())
    embed.add_field(name="\u200B", value="\u200B")

    footer = raid_manager.get_raid(server_id).get_raid_state().value

    # Check if there are players
    if len(raid_manager.get_raid(server_id).get_players().values()) > 0:
        # Add player list
        footer += '\n(' + ", ".join(raid_manager.get_raid(server_id).get_players().values()) + ')'

    embed.set_footer(text=footer)

    await message.channel.send(embed=embed)


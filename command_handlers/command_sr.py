import messages
import asyncio
import command_handlers.command_raid_info as command_raid_info
import raids.raid_manager as raid_manager
from entities.boss_slime_king import SlimeKingBoss


# Force spawn a raid
async def handle(message, db):
    id = message.author.id
    server_id = message.guild.id
    info = db.init_info_check(message)

    if raid_manager.has_raid(server_id):
        await message.channel.send("Raid already in progress")
        return

    raid_manager.add_raid(server_id, SlimeKingBoss(1), message.channel, asyncio.get_event_loop())
    await message.channel.send("Raid started (Slime King)")

    # Call this cause why not
    await command_raid_info.handle(message, db)



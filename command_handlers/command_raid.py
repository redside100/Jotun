import messages
import raids.raid_manager as raid_manager
from raids.raid import RaidState


# Join raid command
async def handle(message, db):
    id = message.author.id
    name = message.author.name
    server_id = message.guild.id
    info = db.init_info_check(message)

    # Check if there is a raid going on
    if not raid_manager.has_raid(server_id):
        await message.channel.send(messages.data['no_raid'])
        return

    raid = raid_manager.get_raid(server_id)

    # Check if it's in the lobby state (open to joining)
    if not raid.get_raid_state() == RaidState.LOBBY:
        await message.channel.send(message.data['raid_already_started'].replace("%name%", name))
        return

    # Check if the player is already in the raid
    if raid.has_player(id):
        await message.channel.send(messages.data['already_in_raid'].replace("%name%", name))
        return

    if raid.add_player(id, name):
        await message.channel.send(messages.data['raid_join_successful'].replace('%name%', name))
    else:
        await message.channel.send(messages.data['raid_full'].replace("%name%", name))


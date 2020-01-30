import messages
import raids.raid_manager as raid_manager
from raids.raid import RaidState
from time import strftime, gmtime


# Join raid command
async def handle(message, db):
    id = message.author.id
    name = message.author.name
    server_id = message.guild.id
    info = db.init_info_check(message)

    # Check if the player has a class
    if info['class'] == "None":
        await message.channel.send(messages.data['no_class_raid'].replace("%name%", name))
        return

    # Check if there is a raid going on
    if not raid_manager.has_raid(server_id):
        await message.channel.send(messages.data['no_raid'])
        return

    raid = raid_manager.get_raid(server_id)

    # Check if it's in the lobby state (open to joining)
    if not raid.get_raid_state() == RaidState.LOBBY:
        await message.channel.send(messages.data['raid_already_started'].replace("%name%", name))
        return

    # Check if the player is already in the raid
    if raid.has_player(id):
        await message.channel.send(messages.data['already_in_raid'].replace("%name%", name))
        return

    # Check if the player is already in a raid (in another server)
    if raid_manager.is_player_in_raid(id):
        await message.channel.send(messages.data['raid_in_other_server'].replace("%name%", name))
        return

    if raid.add_player(id, name, db):
        time_left = strftime("%M:%S", gmtime(raid.get_timer().get_time_left()))
        await message.channel.send(messages.data['raid_join_successful'].replace('%name%', name)
                                   .replace('%time%', time_left))
    else:
        await message.channel.send(messages.data['raid_full'].replace("%name%", name))


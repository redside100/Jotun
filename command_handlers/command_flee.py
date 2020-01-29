import messages
import raids.raid_manager as raid_manager
from raids.raid import RaidState


"""
Flee command
"""


async def handle(message, db):
    id = message.author.id
    server_id = message.guild.id
    name = message.author.name
    info = db.init_info_check(message)

    # Check if there's a raid going on
    if not raid_manager.has_raid(server_id):
        return

    raid = raid_manager.get_raid(server_id)

    # Check if player is in raid
    if not raid_manager.is_player_in_raid(id, server_id=server_id):
        return

    # Check if raid state is player's turns
    if not raid.get_raid_state() == RaidState.PLAYER_TURN:
        return

    if raid.get_current_player() is not None:
        # Check if it's the player's turn
        if raid.get_current_player().id == id:
            player = raid.get_current_player()

            # In case of buffer... we immediately disable player moves by setting current player to none
            raid.current_player = None
            await message.channel.send(messages.data['raid_fled'].replace('%name%', name))

            # Remove player from list
            raid.players.pop(raid.current_player_index)

            await raid.next_player(raid.default_channel, flee=True)

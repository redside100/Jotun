import messages
from items.item import Item, ItemType
import items.item_map
import raids.raid_manager as raid_manager
from raids.raid import RaidState


"""
Attack command...
So apparently there are lots of race conditions.
To prevent players from spamming attack and doing damage multiple times a turn,
we have to immediately set the raid's current player to None once a valid attack command goes through.
Then, we restore that by calling next player *at the very end*.
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

            # In case of buffer... we immediately disable attacking ability by setting current player to none
            raid.current_player = None

            if not raid.get_raid_boss().evaded_roll():
                # Damage the boss
                damage = player.get_info()['atk'] + player.extra_atk

                raid.get_raid_boss().damage(damage)

                await message.channel.send(messages.data['raid_attack_hit']
                                           .replace('%boss_name%', raid.get_raid_boss().get_name())
                                           .replace('%amount%', str(damage))
                                           .replace('%hp%', str(raid.get_raid_boss().get_hp())))

            else:
                await message.channel.send(messages.data['raid_attack_dodged'].replace('%boss_name%',
                                                                                       raid.get_raid_boss().get_name()))

            # Alive check
            if raid.get_raid_boss().is_alive():
                # This should update the current player
                await raid.next_player(raid.default_channel)
            else:
                await raid.end_raid(raid.default_channel)
                await message.channel.send(messages.data['raid_defeated'].replace('%boss_name%',
                                                                                  raid.get_raid_boss().get_name()))

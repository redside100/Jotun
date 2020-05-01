import messages
from items.item import Item, ItemType
import items.item_map
import raids.raid_manager as raid_manager


# Equip item command
async def handle(message, db):
    id = message.author.id
    name = message.author.name
    info = db.init_info_check(message)

    # Check if the player is in a raid, and if it's their turn
    if raid_manager.is_player_in_raid(id):
        await message.channel.send(messages.data['invalid_in_raid'].replace('%name%', name))
        return

    # check if there's more than one argument
    if len(message.content.split(" ")) > 1:

        item_name = message.content[message.content.find(" ") + 1:].lower()
        item_id_equips = info['equips']

        # Get the requested item's ID, from the name
        requested_item_id = items.item_map.item_name_to_id.get(item_name, None)
        if requested_item_id is None or requested_item_id not in item_id_equips:
            await message.channel.send(messages.data['invalid_dequip_item'].replace('%name%', name))
            return

        item = items.item_map.item_map[requested_item_id]()
        # De-equip the item
        await item.dequip(message, db)

    else:
        await message.channel.send(messages.data['equip_usage'])

import messages
from items.item import Item, ItemType
import items.item_map


# Use item command
async def handle(message, db):
    id = message.author.id
    name = message.author.name
    info = db.init_info_check(message)

    # check if there's more than one argument
    if len(message.content.split(" ")) > 1:

        item_name = message.content[message.content.find(" ") + 1:].lower()
        item_id_inventory = info['items']

        # Get the requested item's ID, from the name
        requested_item_id = items.item_map.item_name_to_id.get(item_name, None)
        if requested_item_id is None or requested_item_id not in item_id_inventory:
            await message.channel.send(messages.data['invalid_use_item'].replace('%name%', name))
            return

        # We know it's an item, just check if it's a consumable
        item = items.item_map.item_map[requested_item_id]()
        if not item.get_item_type() == ItemType.CONSUMABLE:
            await message.channel.send(messages.data['invalid_use_item'].replace('%name%', name))
            return

        # Use the item
        await item.use(message, db)
    else:
        await message.channel.send(messages.data['use_usage'])
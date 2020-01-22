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
        if requested_item_id is None or requested_item_id not in items.item_map.item_shop_map:
            await message.channel.send(messages.data['invalid_shop_item'].replace('%name%', name))
            return

        # We know it's an item, just check if it's purchasable
        item = items.item_map.item_shop_map[requested_item_id]()
        if info['gold'] >= item.get_gold_amount():
            if requested_item_id in info['items']:
                info['items'][requested_item_id] += 1
            else:
                info['items'][requested_item_id] = 1
            info['gold'] -= item.get_gold_amount()
            db.set_player_info(id, info)
        else:
            await message.channel.send(messages.data['invalid_gold_amount'].replace('%name%', name))
            return

        # Item purchased message
        await message.channel.send(messages.data['purchase_successful']
                                   .replace('%name%', name).replace('%item_name%', item.get_name()))
    else:
        await message.channel.send(messages.data['buy_usage'])

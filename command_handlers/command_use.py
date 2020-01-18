import messages
from items.item import Item, ItemType


# Use item command
async def handle(message, db):
    id = message.author.id
    name = message.author.name
    info = db.get_player_info(id)

    if info is None:
        db.add_new_player(id)
        info = db.get_player_info(id)

    # check if there's more than one argument
    if len(message.content.split(" ")) > 1:
        pass
    else:
        await message.channel.send(messages.data['use_usage'])
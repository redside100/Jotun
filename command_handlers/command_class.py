import messages

valid_classes = [
    "Knight",
    "Priest",
    "Wizard",
    "Paladin"
]

class_info = {
    "Knight": {
        "hp": 200,
        "mp": 100,
        "atk": 20,
        "eva": 1
    },
    "Priest": {
        "hp": 100,
        "mp": 175,
        "atk": 10,
        "eva": 10
    },
    "Wizard": {
        "hp": 100,
        "mp": 200,
        "atk": 10,
        "eva": 10
    },
    "Paladin": {
        "hp": 150,
        "mp": 100,
        "atk": 20,
        "eva": 5
    }
}


# Class command (not finished)
async def handle(message, db):
    id = message.author.id
    name = message.author.name
    info = db.get_player_info(id)

    if info is None:
        db.add_new_player(id)
        info = db.get_player_info(id)

    # We don't let the user change their class if they already have one!
    if not info['class'] == "None":
        await message.channel.send(messages.data['class_already_chosen']
                                   .replace('%name%', name).replace('%class%', info['class']))
        return

    # check if there's more than one argument
    if len(message.content.split(" ")) > 1:
        requested_class = message.content.split(" ")[1]
        requested_class = requested_class.lower().capitalize()

        if requested_class not in valid_classes:
            await message.channel.send(messages.data['invalid_class'].replace('%name%', name))
        else:
            # Set class stats and info
            info['class'] = requested_class
            info['hp'] = class_info[requested_class]['hp']
            info['max_hp'] = class_info[requested_class]['hp']
            info['mp'] = class_info[requested_class]['mp']
            info['max_mp'] = class_info[requested_class]['mp']
            info['atk'] = class_info[requested_class]['atk']
            info['eva'] = class_info[requested_class]['eva']

            db.set_player_info(id, info)
            await message.channel.send(messages.data['class_successful'].replace('%name%', name)
                                       .replace('%class%', requested_class))
    else:
        await message.channel.send(messages.data['class_usage'])

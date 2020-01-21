import messages


# Class command (not finished)
async def handle(message, db):
    id = message.author.id
    name = message.author.name
    info = db.init_info_check(message)

    if 'potion_hp' in info['items']:
        info['items']['potion_hp'] += 1
    else:
        info['items']['potion_hp'] = 1

    db.set_player_info(id, info)
    await message.channel.send("Gave you a health potion!")


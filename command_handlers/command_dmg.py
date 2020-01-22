import messages


# Class command (not finished)
async def handle(message, db):
    id = message.author.id
    info = db.init_info_check(message)

    info['hp'] = 1
    db.set_player_info(id, info)
    await message.channel.send("Set your HP to 1!")

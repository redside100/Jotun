import messages


# gold command
async def handle(message, db):
    id = message.author.id
    info = db.init_info_check(message)

    info['gold'] += 1000
    db.set_player_info(id, info)
    await message.channel.send("Added 1000 gold!")

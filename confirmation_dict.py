from enum import Enum
import messages


class ConfirmationType(Enum):
    RESET = 'RESET'
    DONE = 'DONE'


confirmations = {}


async def nop(args, db):
    pass


async def handle_reset(message, db):
    id = message.author.id
    db.reset_player(id)
    confirmations[id] = None
    await message.channel.send(messages.data['reset_successful'])


handlers = {ConfirmationType.RESET: handle_reset}


async def handle(message, db):
    id = message.author.id
    if id in confirmations:
        if confirmations[id] is not None:
            await handlers.get(confirmations[id][0], nop)(message, db)




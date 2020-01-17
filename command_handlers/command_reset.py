import messages
import confirmation_dict
from confirmation_dict import ConfirmationType
import asyncio


# Reset command
async def handle(message, db):
    id = message.author.id
    name = message.author.name

    await message.channel.send(messages.data['reset_confirmation'].replace('%name%', name))
    confirmation_dict.confirmations[id] = (confirmation_dict.ConfirmationType.RESET, message.id)

    await cancel(message)


async def cancel(message):
    await asyncio.sleep(15)  # Wait 15 seconds before cancelling
    if message.author.id in confirmation_dict.confirmations:
        # If user hasn't done anything yet
        confirmation = confirmation_dict.confirmations[message.author.id]
        if confirmation is not None:
            # check if it's the right message id
            if confirmation[1] == message.id:
                confirmation_dict.confirmations[message.author.id] = None
                await message.channel.send(messages.data['reset_cancelled'])


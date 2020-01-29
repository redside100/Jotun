import discord
import logging
import yaml
import os
import messages
from command_handlers import command_ping, command_info, command_reset, command_class, command_inventory, command_buy, \
    command_use, command_dmg, command_gold, command_shop, command_sr, command_raid_info, command_raid, command_heal, \
    command_attack, command_flee
from database import Database
import confirmation_dict

prefix = '>'


logging.basicConfig(filename='files/app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

db = Database()


class InvalidTokenException(Exception):
    pass


async def noop(args, db):
    pass

# ======================== HANDLERS ======================== #
command_handlers = {'ping': command_ping.handle, 'info': command_info.handle, 'reset': command_reset.handle,
                    'class': command_class.handle, 'inventory': command_inventory.handle, 'buy': command_buy.handle,
                    'use': command_use.handle, 'dmg': command_dmg.handle, 'heal': command_heal.handle,
                    'gold': command_gold.handle, 'shop': command_shop.handle, 'sr': command_sr.handle,
                    'raid': command_raid.handle, 'raidinfo': command_raid_info.handle, 'attack': command_attack.handle,
                    'flee': command_flee.handle}
# ========================================================== #


class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):

        guild = message.guild

        # don't respond to ourselves or DMs
        if message.author == self.user or guild is None:
            return

        # Command handler
        if message.content.startswith(prefix):
            cmd = message.content.replace(prefix, '')
            if len(message.content.split(" ")) > 0:
                cmd = message.content.replace(prefix, '').split(" ")[0]

            await command_handlers.get(cmd.lower(), noop)(message, db)

        # Confirmation listener
        if message.content.lower() == 'confirm':
            await confirmation_dict.handle(message, db)


def init():
    messages.init()


def get_token_from_file():

    # Create if it doesn't exist
    if not os.path.exists("files/token.yaml"):
        f = open('files/token.yaml', 'w')
        f.close()

    # Read token
    with open('files/token.yaml', 'r+') as token_file:
        cred = yaml.safe_load(token_file)
        if cred is None:
            raise InvalidTokenException('File is empty.')
        if 'token' in cred.keys():
            return cred['token']


def start():
    init()
    token = get_token_from_file()
    client = MyClient()
    client.run(token)


if __name__ == '__main__':
    start()

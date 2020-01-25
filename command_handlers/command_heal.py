import messages
from items.item import Item, ItemType
import items.item_map
import time
import random
import raids.raid_manager as raid_manager


# Heal command
async def handle(message, db):
    id = message.author.id
    name = message.author.name
    info = db.init_info_check(message)

    player_cds = db.init_cd_check(message)
    curr_time = int(time.time())

    # Check if the player is in a raid!
    if raid_manager.is_player_in_raid(id):
        await message.channel.send(messages.data['invalid_in_raid'].replace('%name%', name))
        return

    if curr_time >= player_cds['heal']:
        amount = int(info['max_hp'] * random.uniform(0.4, 0.7))  # 40-70% of max hp

        info['hp'] += amount
        if info['hp'] > info['max_hp']:
            info['hp'] = info['max_hp']

        # Update db
        db.set_player_info(id, info)

        # set cd (3 hrs)
        player_cds['heal'] = curr_time + 10800   # 10800 for 3 hrs, lower for testing
        db.set_player_cds(id, player_cds)

        await message.channel.send(messages.data['heal_successful'].replace('%name%', name)
                                   .replace('%amount%', str(amount)))

        pass
    else:
        seconds = player_cds['heal'] - curr_time
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        time_msg = ''

        if h > 0:
            time_msg += "{}h {:02d}m".format(h, m)
        elif m > 0:
            time_msg += "{} min".format(m)
        else:
            time_msg += "{} sec".format(s)

        await message.channel.send(messages.data['cooldown_timer'].replace('%name%', name).replace('%action%', 'Heal')
                                   .replace('%time%', time_msg))


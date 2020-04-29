import asyncio

import messages
import time
import random
import utils
import raids.raid_manager as raid_manager
from command_handlers import command_raid_info
from entities.boss_slime_king import SlimeKingBoss
from entities.raid_boss import BossTier

boss_pool = {
    BossTier.COMMON: [SlimeKingBoss],
    BossTier.RARE: [],
    BossTier.EPIC: [],
    BossTier.LEGENDARY: [],
    BossTier.MYTHICAL: []
}


# Search command
async def handle(message, db):
    id = message.author.id
    name = message.author.name
    info = db.init_info_check(message)
    server_id = message.guild.id

    player_cds = db.init_cd_check(message)
    curr_time = int(time.time())

    # Check if the server already has a raid ongoing
    if raid_manager.has_raid(server_id):
        await message.channel.send(messages.data['raid_ongoing'])
        return

    if curr_time >= player_cds['search']:
        roll = random.uniform(0, 1)
        chance = 0.1 + (0.01 * info['level'])
        if chance > 0.5:
            chance = 0.5

        if roll < chance:
            # Spawn a random raid
            roll = random.uniform(0, 1)
            # Well... only one boss rn so just common
            boss = None
            if 0 <= roll <= 1:
                boss = random.choice(boss_pool[BossTier.COMMON])

            boss_ref = boss(1, server_id)
            raid_manager.add_raid(server_id, boss_ref, message.channel, asyncio.get_event_loop())
            await message.channel.send(messages.data['raid_found'].replace('%boss_name%', boss_ref.name))
            # Call this cause why not
            await command_raid_info.handle(message, db)

        else:
            await message.channel.send(messages.data['no_raid_found'])

        # set cd (3 hrs)
        player_cds['search'] = curr_time + 10   # 3600 for 1 hr, lower for testing
        db.set_player_cds(id, player_cds)

    else:
        seconds = player_cds['search'] - curr_time
        time_msg = utils.format_time(seconds)

        await message.channel.send(messages.data['cooldown_timer'].replace('%name%', name).replace('%action%', 'Search')
                                   .replace('%time%', time_msg))


from entities.raid_boss import RaidBoss, BossTier
import messages
import random

from entities.status_effect import StatusEffect
from items.item_health_ring import HealthRingItem

"""
HP: 100
ATK: 0
EVA: 5
TIER: Common
TIME: 300 seconds
"""

rewards = [
    None,
    None,
    None,
    None,
    ("ring_hp", 1)
]


class UselessGoddessBoss(RaidBoss):
    def __init__(self, level, server_id):
        # Scale w/ level

        hp = int(100 + ((level - 1) * 50))
        atk = 0

        super(UselessGoddessBoss, self).__init__("Useless Goddess", hp, atk, 5, BossTier.COMMON, level, 300, rewards,
                                            messages.data['img_useless_goddess'], server_id)

    # need to return an event log
    def handle_turn(self, players):

        # Normal attack (cry)
        choice = random.randint(1, 2)
        if choice == 1:
            event_log = messages.data['useless_goddess_cry'].replace('%boss_name%', self.name)
            return event_log
        else:
            event_log = messages.data['useless_goddess_complain'].replace('%boss_name%', self.name) + '\n\n'
            # Stun a random player
            player = random.choice(players)
            if not player.evaded_roll():

                if StatusEffect.STUNNED not in player.status_effects:
                    player.status_effects.append(StatusEffect.STUNNED)

                event_log += '**{}** was stunned!\n'.format(player.get_name())

            else:
                event_log += '**{}** dodged the attack!\n'.format(player.get_name())

            return event_log

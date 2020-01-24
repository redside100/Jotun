from entities.raid_boss import RaidBoss, BossTier
import messages

"""
HP: 500
ATK: 12
EVA: 15
XP: 50
GOLD: 100
TIER: Common
TIME: 600 seconds
"""


class SlimeKingBoss(RaidBoss):
    def __init__(self, level):
        super(SlimeKingBoss, self).__init__("Slime King", 500, 12, 15, 50, 100, BossTier.COMMON, level, 600,
                                            messages.data['img_slime_king'])

    def handle_turn(self):
        pass

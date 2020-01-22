from entities.raid_boss import RaidBoss, BossTier
import messages


class SlimeKingBoss(RaidBoss):
    def __init__(self, level):
        super(SlimeKingBoss, self).__init__("Slime King", 500, 12, 15, 50, 100, BossTier.COMMON, level,
                                            messages.data['img_slime_king'])

    def handle_turn(self):
        pass

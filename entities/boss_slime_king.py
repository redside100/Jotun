from entities.raid_boss import RaidBoss, BossTier
import messages
import random

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
        # Scale w/ level

        hp = int(400 + ((level - 1) * 50))
        atk = int(10 + ((level - 1) * 2))
        xp = int(50 + ((level - 1) * 10))
        gold = int(100 + ((level - 1) * 20))

        super(SlimeKingBoss, self).__init__("Slime King", hp, atk, 15, xp, gold, BossTier.COMMON, level, 600,
                                            messages.data['img_slime_king'])
        self.preparing_crash = False
        self.mitosis_used = False
        self.old_max_hp = self.max_hp
        self.old_atk = self.atk

    # need to return an event log
    def handle_turn(self, players):

        # Use mitosis (set to minion, "invincible")
        if self.hp <= self.max_hp / 2 and not self.mitosis_used:
            self.preparing_crash = False
            self.mitosis_used = True
            self.set_minion(True)
            self.name = "Lesser Slime"

            event_log = messages.data['slime_king_mitosis']

            self.hp = int(self.max_hp / 4)
            self.max_hp = int(self.max_hp / 4)
            self.atk = int(self.atk / 2)

            return event_log

        # Mitosis dead, reset stats
        if self.hp <= 0 and self.is_minion:
            self.preparing_crash = False
            self.set_minion(False)
            self.name = "Slime King"
            event_log = messages.data['slime_king_mitosis_dead']

            self.max_hp = self.old_max_hp
            self.hp = int(self.max_hp / 2)
            self.atk = self.old_atk

            return event_log

        # Slime crash
        if self.preparing_crash:
            self.preparing_crash = False
            event_log = messages.data['slime_king_crash'].replace('%boss_name%', self.name) + '\n\n'
            target_player = random.choice(players)
            damage = random.randint(self.atk, self.atk * 2)
            if not target_player.evaded_roll():
                target_player.damage(damage)
                hp_left = str(target_player.get_info()['hp'])
                if target_player.extra_hp > 0:
                    hp_left += ' [+ {}]'.format(target_player.extra_hp)

                event_log += '**{}** took **{}** damage (**{}** HP left).'.format(target_player.get_name(),
                                                                                 damage, hp_left)
            else:
                event_log += '**{}** dodged the attack!'.format(target_player.get_name())

            return event_log

        # Normal attack (prepare crash, or tackle)
        choice = random.randint(1, 2)
        if choice == 1:
            event_log = messages.data['slime_king_prepare_crash'].replace('%boss_name%', self.name)
            self.preparing_crash = True
            return event_log
        else:
            event_log = messages.data['slime_king_tackle'].replace('%boss_name%', self.name) + '\n\n'
            # Attack all players
            for player in players:
                damage = random.randint(1, 4) + self.atk
                if not player.evaded_roll():
                    player.damage(damage)
                    hp_left = str(player.get_info()['hp'])
                    if player.extra_hp > 0:
                        hp_left += ' [+ {}]'.format(player.extra_hp)

                    event_log += '**{}** took **{}** damage (**{}** HP left).\n'.format(player.get_name(),
                                                                                      damage, hp_left)
                else:
                    event_log += '**{}** dodged the attack!\n'.format(player.get_name())

            return event_log

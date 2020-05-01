from enum import Enum
import random

from raids import raid_manager


class BossTier(Enum):
    COMMON = "Common"
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"
    MYTHICAL = "Mythical"


class RaidBoss:
    def __init__(self, name, hp, atk, eva, tier, level, raid_time, rewards, url, server_id):
        self.rewards = rewards
        self.server_id = server_id
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.atk = atk
        self.eva = eva
        self.tier = tier
        self.level = level
        self.raid_time = raid_time
        self.url = url
        self.alive = True
        self.is_minion = False

    def get_name(self):
        return self.name

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.max_hp

    def get_atk(self):
        return self.atk

    def get_eva(self):
        return self.eva

    def get_tier(self):
        return self.tier

    def get_level(self):
        return self.level

    def get_raid_time(self):
        return self.raid_time

    def damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            if not self.is_minion:
                self.alive = False

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    # Will return updated event_log
    def damage_player(self, player, damage, event_log):
        player.damage(damage)
        hp_left = str(player.get_info()['hp'])
        if player.extra_hp > 0:
            hp_left += ' [+ {}]'.format(player.extra_hp)

        event_log += '**{}** took **{}** damage (**{}** HP left).\n'.format(player.get_name(),
                                                                            damage, hp_left)
        # Check if player is dead, reset and remove if so
        if player.is_dead():
            player.db.reset_player(player.id)
            raid = raid_manager.get_raid(self.server_id)
            raid.players.remove(player)
            event_log += ':skull: **{}** died...\n'.format(player.get_name())

        return event_log

    def is_alive(self):
        return self.alive

    def get_url(self):
        return self.url
    
    def handle_turn(self, players):
        pass

    def set_minion(self, minion):
        self.is_minion = minion

    # Calculate dodge rng outcome
    def evaded_roll(self):
        roll = random.randint(1, 100)

        if roll > self.eva:
            return False

        return True

    def get_rewards(self):
        return self.rewards

    def get_reward_gold(self, player_level):
        tier_multiplier = {
            BossTier.COMMON: 1,
            BossTier.RARE: 1.5,
            BossTier.EPIC: 2,
            BossTier.MYTHICAL: 3,
            BossTier.LEGENDARY: 5
        }
        return int(15 + tier_multiplier[self.tier] * 25 + random.randint(1, player_level) + self.level)

    def get_reward_xp(self):
        tier_multiplier = {
            BossTier.COMMON: 1,
            BossTier.RARE: 1.2,
            BossTier.EPIC: 1.5,
            BossTier.MYTHICAL: 3,
            BossTier.LEGENDARY: 5
        }
        return int(10 + tier_multiplier[self.tier] * 20 + random.randint(self.level, self.level * 2))


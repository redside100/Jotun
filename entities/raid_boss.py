from enum import Enum
import random

class BossTier(Enum):
    COMMON = "Common"
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"
    MYTHICAL = "Mythical"


class RaidBoss:
    def __init__(self, name, hp, atk, eva, xp_reward, gold_reward, tier, level, raid_time, url):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.atk = atk
        self.eva = eva
        self.xp_reward = xp_reward
        self.gold_reward = gold_reward
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

    def get_xp_reward(self):
        return self.xp_reward

    def get_gold_reward(self):
        return self.gold_reward

    def get_tier(self):
        return self.tier

    def get_level(self):
        return self.level

    def get_raid_time(self):
        return self.raid_time

    def damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
            if not self.is_minion:
                self.alive = False

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

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


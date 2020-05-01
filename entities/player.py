import random
import math


class Player:
    def __init__(self, id, name, db):
        self.id = id
        self.name = name
        self.db = db
        self.extra_eva = 0
        self.extra_def = 0
        self.extra_hp = 0
        self.extra_mp = 0
        self.extra_atk = 0
        self.weak = 0
        self.stun_turn = 0
        self.poison_turn = 0
        self.poison_dmg = 0
        self.status_effects = []
        self.fled = False

    def get_info(self):
        return self.db.get_player_info(self.id)

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def damage(self, damage):
        # check for health buffs
        if self.extra_hp >= damage:
            self.extra_hp -= damage
            return
        # Damage them
        damage -= self.extra_hp
        self.extra_hp = 0
        info = self.get_info()
        info['hp'] -= damage
        # Update db
        self.db.set_player_info(self.id, info)

    def heal(self, amount):
        info = self.get_info()
        info['hp'] += amount
        if info['hp'] > info['max_hp']:
            info['hp'] = info['max_hp']

        self.db.set_player_info(self.id, info)

    def poison(self, turns, damage):
        self.poison_dmg = damage
        self.poison_turn = turns

    def cleanse(self):
        self.status_effects = []

    def add_extra_eva(self, amount):
        if self.get_info()['eva'] + self.extra_eva + amount > 50:
            self.extra_eva += 50 - self.get_info()['eva'] - self.extra_eva
        else:
            self.extra_eva += amount

    def is_dead(self):
        return self.get_info()['hp'] + self.extra_hp <= 0

    # Calculate dodge rng outcome
    def evaded_roll(self):
        total_evade = self.get_info()['eva'] + self.extra_eva
        roll = random.randint(1, 100)

        if roll > total_evade:
            return False

        return True

    # Returns a tuple, containing levels to be added, left over xp, and xp to next
    # f(x) = 50 * 1.1^(x - 1)
    # Inverse: f(x) = ln(x/50)/ln(1.1) + 1
    def calculate_raw_xp_to_levels(self, raw_xp):
        curr_level = self.get_info()['level']
        curr_xp = self.get_info()['xp']

        def level_to_xp(level):
            return int(50 * pow(1.1, level - 1))

        levels = 0
        while raw_xp > 0:
            if curr_xp + raw_xp >= level_to_xp(curr_level):
                levels += 1
                raw_xp -= level_to_xp(curr_level) - curr_xp
                curr_xp = 0
                curr_level += 1
            else:
                break

        return levels, raw_xp, level_to_xp(curr_level)


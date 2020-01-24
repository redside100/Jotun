from enum import Enum


class StatusEffect(Enum):
    POISON = "Poison"
    INVULNERABLE = "Invulnerable"
    HEALING = "Healing"
    STUNNED = "Stunned"
    WEAK = "Weak"


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

    def get_info(self):
        return self.db.get_player_info(self.id)

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

    def is_dead(self):
        return self.get_info()['hp'] + self.extra_hp <= 0


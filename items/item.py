from enum import Enum


class ItemType(Enum):
    WEAPON = "WEAPON"
    RING = "RING"
    ARMOR = "ARMOR"
    SPELL = "SPELL"
    CONSUMABLE = "CONSUMABLE"
    UNDEFINED = "UNDEFINED"


class Item:
    def __init__(self, name, item_type, emoji, gold_amount, value=0):
        self.name = name
        self.item_type = item_type
        self.emoji = emoji
        self.gold_amount = gold_amount
        self.value = value

    def get_name(self):
        return self.name

    def get_item_type(self):
        return self.item_type

    def get_emoji(self):
        return self.emoji

    def get_gold_amount(self):
        return self.gold_amount

    def get_value(self):
        return self.value

    async def use(self, message, db):
        pass

    async def equip(self, message, db):
        pass

    async def dequip(self, message, db):
        pass

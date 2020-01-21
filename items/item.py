from enum import Enum


class ItemType(Enum):
    WEAPON = "WEAPON"
    SPELL = "SPELL"
    CONSUMABLE = "CONSUMABLE"
    UNDEFINED = "UNDEFINED"


class Item:
    def __init__(self, name, item_type, emoji, gold_amount):
        self.name = name
        self.item_type = item_type
        self.emoji = emoji
        self.gold_amount = gold_amount;

    def get_name(self):
        return self.name

    def get_item_type(self):
        return self.item_type

    def get_emoji(self):
        return self.emoji

    def get_gold_amount(self):
        return self.gold_amount

    async def use(self, message, db):
        pass

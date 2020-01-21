from enum import Enum


class ItemType(Enum):
    WEAPON = "WEAPON"
    SPELL = "SPELL"
    CONSUMABLE = "CONSUMABLE"
    UNDEFINED = "UNDEFINED"


class Item:
    def __init__(self, name, item_type, emoji):
        self.name = name
        self.item_type = item_type
        self.emoji = emoji

    def get_name(self):
        return self.name

    def get_item_type(self):
        return self.item_type

    def get_emoji(self):
        return self.emoji

    async def use(self, message, db):
        pass

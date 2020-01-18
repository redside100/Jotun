import messages
import items.item as item


class HealthPotionItem(item.Item):
    def __init__(self):
        super(HealthPotionItem, self).__init__("Health Potion", item.ItemType.CONSUMABLE, messages.data['emoji_health_potion'])

    async def use(self):
        pass

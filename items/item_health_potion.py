import messages
import items.item as item


class HealthPotionItem(item.Item):
    def __init__(self):
        super(HealthPotionItem, self).__init__("Health Potion", item.ItemType.CONSUMABLE,
                                               messages.data['emoji_health_potion'], 100)

    async def use(self, message, db):
        info = db.init_info_check(message)
        percent_restore = 0.2
        if info['hp'] < info['max_hp']:
            amount = int(info['max_hp'] * percent_restore)
            # Add HP
            info['hp'] += amount

            # Check for overflow
            if info['hp'] > info['max_hp']:
                info['hp'] = info['max_hp']

            info['hp'] = int(info['hp'])
            # Consume item
            hp_item_id = info['items'].get('potion_hp', None)
            # This should always happen... but just in case
            if hp_item_id is not None:
                # Consume 1 of the item
                info['items']['potion_hp'] -= 1
                # If we run out, delete the thing
                if info['items']['potion_hp'] <= 0:
                    del info['items']['potion_hp']

            # Update db
            db.set_player_info(message.author.id, info)
            await message.channel.send(messages.data['use_health_potion']
                                       .replace('%name%', message.author.name).replace('%amount%', str(int(amount))))
        else:
            await message.channel.send(messages.data['health_already_full'].replace('%name%', message.author.name))

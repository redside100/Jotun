import messages
import items.item as item


class ManaPotionItem(item.Item):
    def __init__(self):
        super(ManaPotionItem, self).__init__("Mana Potion", item.ItemType.CONSUMABLE,
                                               messages.data['emoji_mana_potion'], 150)

    async def use(self, message, db):
        info = db.init_info_check(message)
        percent_restore = 0.2
        if info['mp'] < info['max_mp']:
            amount = int(info['max_mp'] * percent_restore)
            # Add MP
            info['mp'] += amount

            # Check for overflow
            if info['mp'] > info['max_mp']:
                info['mp'] = info['max_mp']

            info['mp'] = int(info['mp'])
            # Consume item
            mp_item_id = info['items'].get('potion_mp', None)
            # This should always happen... but just in case
            if mp_item_id is not None:
                # Consume 1 of the item
                info['items']['potion_mp'] -= 1
                # If we run out, delete the thing
                if info['items']['potion_mp'] <= 0:
                    del info['items']['potion_mp']

            # Update db
            db.set_player_info(message.author.id, info)
            await message.channel.send(messages.data['use_mana_potion']
                                       .replace('%name%', message.author.name).replace('%amount%', str(int(amount))))
        else:
            await message.channel.send(messages.data['mana_already_full'].replace('%name%', message.author.name))

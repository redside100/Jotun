import messages
import items.item as item
from items import item_map


class HealthRingItem(item.Item):
    def __init__(self):
        super(HealthRingItem, self).__init__("Ring of Health", item.ItemType.RING,
                                               messages.data['emoji_hp_ring'], 600, value=25)

    async def equip(self, message, db):
        info = db.init_info_check(message)
        has_ring = False
        for item_id in info['equips']:
            equipped_item = item_map.item_map[item_id]()
            if equipped_item.get_item_type() == item.ItemType.RING:

                await equipped_item.dequip(message, db, announce=False)
                # refresh db after dequipping
                info = db.init_info_check(message)
                # add to equips
                info['equips'].append("ring_hp")
                info['max_hp'] += self.get_value()
                has_ring = True
                break

        if not has_ring:
            info['equips'].append("ring_hp")
            info['max_hp'] += self.get_value()

        # Consume 1 of the item
        info['items']['ring_hp'] -= 1
        # If we run out, delete the thing
        if info['items']['ring_hp'] <= 0:
            del info['items']['ring_hp']

        db.set_player_info(message.author.id, info)
        await message.channel.send(messages.data['equip_successful'].replace('%item_name%', "Ring of Health")
                                   .replace('%name%', message.author.name))

    async def dequip(self, message, db, announce=True):
        info = db.init_info_check(message)
        info['max_hp'] -= self.get_value()
        if info['hp'] > info['max_hp']:
            info['hp'] = info['max_hp']

        # refund item
        if 'ring_hp' in info['items']:
            info['items']['ring_hp'] += 1
        else:
            info['items']['ring_hp'] = 1

        info['equips'].remove('ring_hp')

        db.set_player_info(message.author.id, info)
        if announce:
            await message.channel.send(messages.data['dequip_successful'].replace('%item_name%', "Ring of Health")
                                       .replace('%name%', message.author.name))


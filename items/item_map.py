from items.item_health_potion import HealthPotionItem
from items.item_health_ring import HealthRingItem
from items.item_mana_potion import ManaPotionItem

item_map = {
    "potion_hp": HealthPotionItem,
    "potion_mp": ManaPotionItem,
    "ring_hp": HealthRingItem
}
item_shop_map = {
    "potion_hp": HealthPotionItem,
    "potion_mp": ManaPotionItem,
    "ring_hp": HealthRingItem
}

# Keep everything lower case
item_name_to_id = {
    "health potion": "potion_hp",
    "mana potion": "potion_mp",
    "ring of health": "ring_hp"
}

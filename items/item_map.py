from items.item_health_potion import HealthPotionItem
from items.item_health_ring import HealthRingItem

item_map = {
    "potion_hp": HealthPotionItem,
    "ring_hp": HealthRingItem
}
item_shop_map = {
    "potion_hp": HealthPotionItem,
    "ring_hp": HealthRingItem
}

# Keep everything lower case
item_name_to_id = {
    "health potion": "potion_hp",
    "ring of health": "ring_hp"
}

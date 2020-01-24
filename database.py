from pymongo import MongoClient

import logging
import time

"""
Player collection format:

id: Discord ID (snowflake)
hp: Player HP
max_hp: Player max HP
mp: Player MP
max_mp: Player max MP
xp: Player current XP
xp_to_next: XP needed to next level
level: Player current level
class: Player chosen class
skills: List of player skills (by ID and/or enum)
items: List of player's inventory items (by ID and/or enum)
equips: List of player's current equips (by ID and/or enum)
"""

logging.basicConfig(filename='files/app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


class Database:

    def __init__(self):
        # Create new client connection, db, and player collection (if not already existing)
        self.client = MongoClient()  # Default localhost:27017
        self.db = self.client['jotun_db']
        self.player_collection = self.db['players']
        self.player_cd_collection = self.db['player_cd']

    def get_player_info(self, id):
        return self.player_collection.find_one({'id': str(id)})

    def get_player_cds(self, id):
        return self.player_cd_collection.find_one({'id': str(id)})

    def set_player_info(self, id, info):
        return self.player_collection.update_one({'id': str(id)}, {'$set': info})

    def set_player_cds(self, id, cd_info):
        return self.player_cd_collection.update_one({'id': str(id)}, {'$set': cd_info})

    def add_new_player(self, id):
        default_info = {
            'id': str(id),
            'hp': 100,
            'max_hp': 100,
            'mp': 0,
            'max_mp': 0,
            'atk': 0,
            'eva': 0,
            'xp': 0,
            'xp_to_next': 50,
            'level': 1,
            'class': 'None',
            'gold': 0,
            'skills': [],
            'items': {},
            'equips': []
        }
        return self.player_collection.insert_one(default_info)

    def init_player_cds(self, id):
        default_cds = {
            'id': str(id),
            'heal': int(time.time()),
            'search': int(time.time())
        }
        return self.player_cd_collection.insert_one(default_cds)

    def reset_player(self, id):
        default_info = {
            'id': str(id),
            'hp': 100,
            'max_hp': 100,
            'mp': 0,
            'max_mp': 0,
            'atk': 0,
            'eva': 0,
            'xp': 0,
            'xp_to_next': 50,
            'level': 1,
            'class': 'None',
            'gold': 0,
            'skills': [],
            'items': {},
            'equips': []
        }
        return self.player_collection.update_one({'id': str(id)}, {'$set': default_info})

    def attempt_reconnect(self, id):
        try:
            self.client.close()
        except Exception:
            pass

        self.client = MongoClient()
        self.db = self.client['jotun_db']
        self.player_collection = self.db['players']

    def init_info_check(self, message):
        id = message.author.id
        info = self.get_player_info(id)

        if info is None:
            self.add_new_player(id)
            info = self.get_player_info(id)

        return info

    def init_cd_check(self, message):
        id = message.author.id
        player_cds = self.get_player_cds(id)

        if player_cds is None:
            self.init_player_cds(id)
            player_cds = self.get_player_cds(id)

        return player_cds

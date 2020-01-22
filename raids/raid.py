from enum import Enum
from entities.raid_boss import BossTier


class RaidState(Enum):
    LOBBY = "Waiting for players..."
    PLAYER_TURN = "Player Turn"
    RAID_BOSS_TURN = "Raid Boss Turn"
    REWARD = "Reward"
    FAILED = "Failed"


class Raid:
    def __init__(self, server_id, raid_boss):
        self.server_id = server_id
        self.raid_boss = raid_boss
        self.raid_state = RaidState.LOBBY
        self.players = {}

    def start_raid(self):
        pass

    def get_raid_boss(self):
        return self.raid_boss

    def get_raid_state(self):
        return self.raid_state

    def get_server_id(self):
        return self.server_id

    # Returns true if successful, false if not
    def add_player(self, id, name):
        if len(self.players) < 20:
            self.players[id] = name
            return True
        return False

    def get_players(self):
        return self.players

    def has_player(self, id):
        return id in self.players

import messages
import raids.raid_manager as raid_manager
from enum import Enum
from timers.timer import Timer


class RaidState(Enum):
    LOBBY = "Waiting for players..."
    PLAYER_TURN = "Player Turn"
    RAID_BOSS_TURN = "Raid Boss Turn"
    REWARD = "Reward"
    FAILED = "Failed"


class Raid:
    def __init__(self, server_id, raid_boss, default_channel, event_loop):
        self.server_id = server_id
        self.raid_boss = raid_boss
        self.raid_state = RaidState.LOBBY
        self.default_channel = default_channel
        self.players = {}
        self.timer = Timer(30, event_loop, self.start_raid, default_channel)
        self.timer.set_event(10, self.announce_time_left, default_channel)
        self.timer.start()

    async def start_raid(self, channel):

        force = False

        # Check if it was called by the timer class, it passes tuples
        if type(channel) == tuple:
            channel = channel[0]
            force = True

        if len(self.players) == 0:
            await channel.send(messages.data['raid_not_enough_players'])
            raid_manager.end_raid(self.server_id)
            return

        if force:
            await channel.send(messages.data['force_raid_start'])

        # End raid for now lmao
        raid_manager.end_raid(self.server_id)

    async def announce_time_left(self, args):

        if type(args) == tuple:
            channel = args[0]

        await channel.send(messages.data['ten_seconds_left'])

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

    def get_timer(self):
        return self.timer

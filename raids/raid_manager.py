from raids.raid import Raid

raids = {}


def add_raid(server_id, raid_boss, default_channel, event_loop):
    raids[server_id] = Raid(server_id, raid_boss, default_channel, event_loop)


def end_raid(server_id):
    if server_id in raids:
        del raids[server_id]


def has_raid(server_id):
    return server_id in raids


def get_raid(server_id):
    if server_id in raids:
        return raids[server_id]



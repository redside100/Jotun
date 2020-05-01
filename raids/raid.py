import random

import messages
import raids.raid_manager as raid_manager
from enum import Enum

from entities.player import Player
from entities.status_effect import StatusEffect
from items import item_map
from timers.timer import Timer
import command_handlers.command_raid_info as command_raid_info
import discord
import asyncio


class RaidState(Enum):
    LOBBY = "Waiting for players..."
    PLAYER_TURN = "Player Turn"
    RAID_BOSS_TURN = "Raid Boss Turn"
    REWARD = "Reward"
    FAILED = "Failed"


# Any functions to be called by the timer should have a force kwarg
class Raid:
    def __init__(self, server_id, raid_boss, default_channel, event_loop):
        self.server_id = server_id
        self.raid_boss = raid_boss
        self.raid_time = raid_boss.get_raid_time()
        self.raid_state = RaidState.LOBBY
        self.default_channel = default_channel
        self.event_loop = event_loop
        self.players = []
        self.current_player = None
        self.current_player_index = -1
        self.timer = Timer(15, event_loop, self.start_raid, default_channel, force=True)
        self.timer.set_event(10, self.announce_time_left, default_channel)
        self.timer.start()

    async def start_raid(self, channel, force=False):

        if len(self.players) == 0:
            await channel.send(messages.data['raid_not_enough_players'])
            raid_manager.end_raid(self.server_id)
            return

        if force:
            await channel.send(messages.data['force_raid_start'])

        # Go to player turn
        self.raid_state = RaidState.PLAYER_TURN
        self.timer = Timer(self.raid_time, self.event_loop, self.end_raid, self.default_channel, force=True)
        self.timer.start()

        # Show raid info
        await command_raid_info.show_info(channel)

        await self.next_player(channel)

    async def next_player(self, channel, flee=False):
        # Flee marks if the caller of next_player has fled the battle (removed from player list)
        if not flee:
            self.current_player_index += 1

        # Set to none so people can't do anything during the wait
        self.current_player = None

        await asyncio.sleep(1)

        # Check if all players gone (no players left)
        if len(self.get_players()) == 0:
            await self.end_raid(channel)
            await channel.send(messages.data['raid_failed'])
            return

        # If we're still not done with players
        if self.current_player_index < len(self.get_players()):

            temp_player = self.get_players()[self.current_player_index]

            turn_msg = messages.data['raid_player_move'].replace('%name%', '<@{}>'.format(temp_player.get_id()))

            # Stun check
            if StatusEffect.STUNNED in temp_player.status_effects:
                breakout = random.randint(1, 2)
                if breakout == 1:
                    turn_msg = messages.data['raid_player_breakout_stun'].replace('%name%', '<@{}>'
                                                                                  .format(temp_player.get_id()))
                    self.get_players()[self.current_player_index].status_effects.remove(StatusEffect.STUNNED)
                else:
                    await channel.send(messages.data['raid_player_stunned'].replace('%name%', temp_player.get_name()))
                    await self.next_player(channel)
                    return

            # Set current player after stun check
            self.current_player = self.get_players()[self.current_player_index]
            await channel.send(turn_msg)
        else:
            # Reset index counter, go to boss turn
            self.current_player_index = -1
            self.current_player = None
            self.raid_state = RaidState.RAID_BOSS_TURN
            await self.handle_boss_turn(channel)

    async def handle_boss_turn(self, channel):
        event_log = self.raid_boss.handle_turn(self.players)
        embed = discord.Embed(title="Boss Event Log", color=0xFFFFFF)
        embed.set_thumbnail(url=self.raid_boss.get_url())
        embed.add_field(name='\u200B', value=event_log)
        await channel.send(embed=embed)
        self.raid_state = RaidState.PLAYER_TURN
        await self.next_player(channel)

    async def announce_time_left(self, channel, force=False):
        await channel.send(messages.data['ten_seconds_left'])

    async def end_raid(self, channel, force=False):
        if force:
            raid_manager.end_raid(self.server_id)
            await channel.send(messages.data['raid_out_of_time'])
            return

        # cancel timer
        self.timer.cancel()
        del self.timer

        await channel.send(messages.data['raid_defeated'].replace('%boss_name%', self.get_raid_boss().get_name()))
        self.current_player = None
        self.raid_state = RaidState.REWARD

        await asyncio.sleep(1)
        rewards = self.get_raid_boss().get_rewards()

        reward_xp = self.get_raid_boss().get_reward_xp()
        reward_log = "All raiders gained **{}** XP.\n\n".format(reward_xp)

        for player in self.players:

            info = player.get_info()

            # Gold drop
            gold = self.get_raid_boss().get_reward_gold(info['level'])
            reward_log += "**{}** found **{}** {}.\n".format(player.get_name(), gold, messages.data['emoji_gold'])
            info['gold'] += gold

            # Exp drop
            xp_info = player.calculate_raw_xp_to_levels(reward_xp)

            info['level'] += xp_info[0]

            if xp_info[0] > 0:
                info['xp'] = xp_info[1]
            else:
                info['xp'] += xp_info[1]

            info['xp_to_next'] = xp_info[2]

            info['max_hp'] += xp_info[0] * 5
            info['max_mp'] += xp_info[0] * 5
            info['atk'] += xp_info[0]

            # Item drops
            reward = random.choice(rewards)
            if reward is not None:
                item_id = reward[0]
                if item_id in info['items']:
                    info['items'][item_id] += reward[1]
                else:
                    info['items'][item_id] = reward[1]
                player.db.set_player_info(player.id, info)

                item_obj = item_map.item_map[item_id]()
                item_name = item_obj.get_name()
                item_emoji = item_obj.get_emoji()
                reward_log += "**{}** found: {} {} (x{})\n".format(player.get_name(), item_emoji, item_name, reward[1])

            player.db.set_player_info(player.id, info)

        embed = discord.Embed(title="Reward Log", color=0xF8C300)
        embed.set_thumbnail(url=self.raid_boss.get_url())
        embed.add_field(name='\u200B', value=reward_log)
        await channel.send(embed=embed)

        raid_manager.end_raid(self.server_id)

    def get_raid_boss(self):
        return self.raid_boss

    def get_raid_state(self):
        return self.raid_state

    def get_server_id(self):
        return self.server_id

    # Returns true if successful, false if not
    def add_player(self, id, name, db):
        if len(self.players) < 20:
            self.players.append(Player(id, name, db))
            return True
        return False

    def get_players(self):
        return self.players

    def get_current_player(self):
        return self.current_player

    def has_player(self, id):
        for player in self.players:
            if player.id == id:
                return True
        return False

    def get_timer(self):
        return self.timer

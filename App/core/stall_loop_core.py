# usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from App.dekomori import client
from App.utils.startup import globalLogger
from App.utils.constants import VERSION


import asyncio
from datetime import datetime
from App.utils import logger as logger
from App.core import guilds_db_core as gdb
from App.core import log_channel_sender_core as lcsend
from App.utils import actions as actions
from DataStructures.watchlist import watchlist as wl
from App.core import dming_core as dms

def initialize_stall_loop():
    """
    Initializes the stall loop.
    """
    client.loop.create_task(stall_loop())

async def stall_loop():
    """
    The stall loop checks for users stalled in onboarding. It runs every 60 seconds.
    """
    while True:
        wlGuilds = gdb.get_guilds_with_populated_watchlists()
        for guildentry in wlGuilds:
            guildId = int(guildentry["guild_id"])
            guildLogger = logger.get_guild_logger(guildId)
            guild = discord.utils.get(client.guilds, id=guildId)
            guildLogger.debug(f"Stall Loop - Checking guild {guild.name} ({guildId})")
            watchlist = gdb.get_value(guildId, "watchlist")
            guildTimeout = gdb.get_value(guildId, "stall_timeout")
            trueWatchlist = wl.purge_userpairs(watchlist, guild)
            for userpair in trueWatchlist:
                userpairId = wl.get_userpair_id(userpair)
                timeElapsed = datetime.datetime.now() - wl.get_userpair_time(userpair)
                if timeElapsed >= datetime.timedelta(seconds=guildTimeout):
                    member = discord.utils.get(guild.members, id=userpairId)
                    guildLogger.info(f"Stall Loop - User {member.name} ({str(userpairId)}) has reached the timeout limit.")
                    if is_kos_active(guildId):
                        actions.kick_member(member, "KOS")
                        dms.kick_on_stall_dm(member, guildId)
                    else:
                        lcsend.stall_no_kos(guild, member)
                    # TODO rejoinchecker
                    wl.remove_userpair(userpair)
                    guildLogger.debug(f"Stall Loop - Removed userpair {userpairId} from watchlist.")
        await asyncio.sleep(60)

def is_kos_active(guildId):
    """
    Checks if the kick on stall feature is active for the guild.

    Parameters
    ----------
    guildId : int
        The ID of the guild.

    Returns
    -------
    bool
        True if KOS is active, False otherwise.
    """
    return gdb.get_value(guildId, "kick_on_stall") == True
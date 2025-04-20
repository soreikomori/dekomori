# usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import discord
from App.dekomori import client
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
        for guild in wlGuilds:
            guildId = int(guild["guild_id"])
            guildLogger = logger.get_guild_logger(guildId)
            guildObj = discord.utils.get(client.guilds, id=guildId)
            guildLogger.debug(f"Stall Loop - Checking guild {guildObj.name} ({guildId})")
            watchlist = gdb.get_value(guildId, "watchlist")
            guildTimeout = gdb.get_value(guildId, "stall_timeout")
            trueWatchlist = wl.purge_userpairs(watchlist, guildObj)
            for userpair in trueWatchlist:
                userpairId = wl.get_userpair_id(userpair)
                timeElapsed = datetime.datetime.now() - wl.get_userpair_time(userpair)
                if timeElapsed >= datetime.timedelta(seconds=guildTimeout):
                    memberObj = discord.utils.get(guildObj.members, id=userpairId)
                    guildLogger.info(f"Stall Loop - User {memberObj.name} ({str(userpairId)}) has reached the timeout limit.")
                    if is_kos_active(guildId):
                        actions.kick_member(memberObj, "KOS")
                        dms.kick_on_stall_dm(memberObj, guildId)
                    else:
                        lcsend.stall_no_kos(guildObj, memberObj)
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
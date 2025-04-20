# usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import discord
from datetime import datetime
from App.utils import logger as logger
from App.core import guilds_db_core as gdb
from App.core import log_channel_sender_core as lcsender
from App.utils import actions as actions
from DataStructures.List import wu_list as wul

def initialize_stall_loop(client):
    """
    Initializes the stall loop.

    Parameters
    ----------
    client : discord.Client
        The Discord client instance.
    """
    client.loop.create_task(stall_loop(client))

async def stall_loop(client):
    """
    The stall loop checks for users stalled in onboarding. It runs every 60 seconds.

    Parameters
    ----------
    client : discord.Client
        The Discord client instance.
    """
    while True:
        wuGuilds = gdb.get_guilds_with_watched_users()
        for guild in wuGuilds:
            guildId = int(guild["id"])
            guildLogger = logger.get_guild_logger(guildId)
            guildObj = discord.utils.get(client.guilds, id=guildId)
            guildLogger.debug(f"Stall Loop - Checking guild {guildObj.name} ({guildId})")
            watchedUsers = guild["watched_users"] # List of WuLists
            guildTimeout = guild["timeout"]
            validUsers = purge_watched_users(guildObj, watchedUsers)
            for wu in validUsers:
                wuId = wul.get_wuser_id(wu)
                timeElapsed = datetime.datetime.now() - wul.get_wuser_time(wu)
                if timeElapsed >= datetime.timedelta(seconds=guildTimeout):
                    memberObj = discord.utils.get(guildObj.members, id=wuId)
                    guildLogger.info(f"Stall Loop - User {memberObj.name} ({str(wuId)}) has reached the timeout limit.")
                    if isKOSActive(guildId):
                        exec_kickonstall(client, guildObj, memberObj)
                    else:
                        lcsender.send_nokos_stall(client, guildId, memberObj)
                    # TODO rejoinchecker
        await asyncio.sleep(60)

def purge_watched_users(guildObj, watchedUsers):
    """
    Purges the watched users list by removing users that are no longer in the guild.

    Parameters
    ----------
    guildObj : discord.Guild
        The guild object to check against.
    watchedUsers : wu_list
        The list of watched users to purge.

    Returns
    -------
    list of WuList
        The list of watched users that are still in the guild.
    """
    for wuList in watchedUsers:
        if not wul.wuser_is_valid(wuList, guildObj):
            watchedUsers.remove(wuList)
    return watchedUsers

def exec_kickonstall(client, memberObj):
    """
    Executes the kick on stall action.

    Parameters
    ----------
    client : discord.Client
        The Discord client instance.
    memberObj : discord.Member
        The member object to kick.
    """
    actions.kick_member(client, memberObj, "KOS")

def isKOSActive(guildId):
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
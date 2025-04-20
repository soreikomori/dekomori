# usr/bin/env python3
# -*- coding: utf-8 -*-
import discord
import asyncio

from App.utils import logger as logger
from App.utils import counters as counters

async def kick_user(guildObj, memberObj, type):
    """
    Kicks a user from the guild.

    Parameters
    ----------
    guildObj : discord.Guild
        The guild object from which to kick the user.
    memberObj : discord.Member
        The member object representing the user to be kicked.
    type : Literal["KOS", "Bait"]
        The type of kick. "KOS" for kick on stall, "Bait" for bait kick.
    """
    guildLogger = logger.get_guild_logger(guildObj.id)
    reason = get_kick_reason(type)
    while not kicked:
        try:
            await memberObj.kick(reason=reason)
            kicked = True
            counters.increment_kick_counter(guildObj.id)
            guildLogger.info(f"Kicked {memberObj.name} ({memberObj.id}).")
        except discord.HTTPException as e:
            guildLogger.error(f"Got an HTTPException while trying to kick {memberObj.name}. Retrying...")
            guildLogger.debug(f"HTTPException: {e}")
            await asyncio.sleep(5)

def get_kick_reason(type):
    """
    Gets the kick reason based on the type of kick. This reason will be logged in the guild's audit log.

    Parameters
    ----------
    type : Literal["KOS", "Bait"]
        The type of kick. "KOS" for kick on stall, "Bait" for bait kick.

    Returns
    -------
    str
        The reason for the kick.
    """
    if type == "KOS":
        return "User didn't complete onboarding in time."
    elif type == "Bait":
        return # TODO implement bait kick reason
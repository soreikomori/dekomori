# usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from App.dekomori import client
from App.utils.startup import globalLogger
from App.utils.constants import VERSION

import asyncio

from App.utils import logger as logger
from App.utils import counters as counters
from App.utils import checks as checks

@checks.requires_permission("kick_members")
async def kick_user(guild, member, type):
    """
    Kicks a user from the guild.

    Parameters
    ----------
    guild : discord.Guild
        The guild object from which to kick the user.
    member : discord.Member
        The member object representing the user to be kicked.
    type : Literal["KOS", "Bait"]
        The type of kick. "KOS" for kick on stall, "Bait" for bait kick.
    """
    guildLogger = logger.get_guild_logger(guild.id)
    guildLogger.debug(f"Attempting to kick {member.name} ({member.id}).")
    reason = get_kick_reason(type)
    kicked = False
    while not kicked:
        try:
            await member.kick(reason=reason)
            kicked = True
            counters.increment_kick_counter(guild.id)
            guildLogger.info(f"Kicked {member.name} ({member.id}).")
        except discord.HTTPException as e:
            guildLogger.error(f"Got an HTTPException while trying to kick {member.name}. Retrying...")
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
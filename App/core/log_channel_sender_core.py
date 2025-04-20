# usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from App.dekomori import client
from App.utils.startup import globalLogger
from App.utils.constants import VERSION

from App.utils import logger as logger
from App.core import guilds_db_core as gdb
from App.core import messages_core as msgs
from App.core import checks as checks

def get_log_channel(guild):
    """
    Gets the log channel for the guild.
    TODO check

    Parameters
    ----------
    guild : discord.Guild
        The guild object.

    Returns
    -------
    discord.TextChannel or None
        The log channel object or None if not found.
    """
    guildId = str(guild.id)
    guildLogger = logger.get_guild_logger(guildId)
    logChannelId = gdb.get_value(guildId, "log_channel_id")
    if logChannelId == 0:
        guildLogger.warning("Log channel ID is 0. No log channel set.")
        return None
    logChannel = discord.utils.get(guild.text_channels, id=logChannelId)
    if logChannel is None:
        guildLogger.warning(f"Log channel with ID {logChannelId} not found in guild {guild.name}.")
    return logChannel

@checks.can_message_log_channel()
async def stall_no_kos(guild, member):
    """
    Sends a message to the log channel indicating that a user has reached the timeout limit, but has not been kicked.
    This happens when the kick on stall feature is not enabled.

    Parameters
    ----------
    guild : discord.Guild
        The guild object.
    member : discord.Member
        The member object representing the user who reached the timeout limit.
    """
    logChannel = get_log_channel(guild)
    message = msgs.nokos_stall(member.mention, member.name, parsedDuration)
    await logChannel.send(message)
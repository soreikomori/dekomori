# usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from App.dekomori import client
from App.utils.startup import globalLogger
from App.utils.constants import VERSION

from App.utils import logger as logger
from App.core import guilds_db_core as gdb
from App.core import messages_core as msgs

def get_log_channel(guildObj):
    """
    Gets the log channel for the guild.

    Parameters
    ----------
    guildObj : discord.Guild
        The guild object.

    Returns
    -------
    discord.TextChannel or None
        The log channel object or None if not found.
    """
    guildId = str(guildObj.id)
    guildLogger = logger.get_guild_logger(guildId)
    logChannelId = gdb.get_value(guildId, "log_channel_id")
    if logChannelId == 0:
        guildLogger.warning("Log channel ID is 0. No log channel set.")
        return None
    logChannel = discord.utils.get(guildObj.text_channels, id=logChannelId)
    if logChannel is None:
        guildLogger.warning(f"Log channel with ID {logChannelId} not found in guild {guildObj.name}.")
    return logChannel

async def send_nokos_stall(client, guildId, memberObj):
    """
    Sends a message to the log channel indicating that a user has reached the timeout limit, but has not been kicked.
    This happens when the kick on stall feature is not enabled.

    Parameters
    ----------
    client : discord.Client
        The Discord client instance.
    guildId : str
        The ID of the guild.
    memberObj : discord.Member
        The member object representing the user who reached the timeout limit.
    """
    guildObj = discord.utils.get(client.guilds, id=int(guildId))
    logChannel = get_log_channel(guildObj)
    if logChannel is None:
        return
    message = msgs.nokos_stall(memberMention, memberName, parsedDuration)
    await logChannel.send(message)
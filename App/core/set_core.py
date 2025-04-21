# usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from App.dekomori import client
from App.utils.startup import globalLogger
from App.utils.constants import VERSION
from App.utils import exceptions as ex
from App.utils import checks as checks

from App.core import guilds_db_core as gdb


@checks.can_message_channel()
def set_log_channel(guild: discord.Guild, channel: discord.TextChannel):
    """Set the log channel for a given guild.

    Parameters
    ----------
    guild : discord.Guild
        The guild where the log channel will be set.
    channel : discord.TextChannel
        The channel to be set as the log channel.

    Raises
    ------
    PermissionError
        If the bot does not have permission to send messages in the specified channel.
    """
    gdb.set_log_channel(guild.id, channel.id)

def set_stall_timeout(guild: discord.Guild, timeout: int):
    """Set the stall timeout for a given guild.

    Parameters
    ----------
    guild : discord.Guild
        The guild where the stall timeout will be set.
    timeout : int
        The timeout duration in seconds.
    """
    # TODO check
    gdb.set_stall_timeout(guild, timeout)
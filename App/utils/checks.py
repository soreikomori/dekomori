# usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from App.dekomori import client
from App.utils.startup import globalLogger
from App.utils.constants import VERSION

from functools import wraps

from App.utils import logger as logger
from App.core import log_channel_sender_core as lcsend

def requires_permission(permission: str):
    """
    Decorator to check if the bot has the required permission in a guild.
    It assumes that the first argument is the guild.

    Parameters
    ----------
    permission : str
        The permission to check for.

    Returns
    -------
    function
        The decorator function.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            guild = args[0]
            if not getattr(guild.me.guild_permissions, permission, False):
                guildLogger = logger.get_guild_logger(guild.id)
                guildLogger.critical(f"Dekomori lacks '{permission}' permission.")
                # TODO Pause deko
                await lcsend.send_permission_error(guild.id, permission)
                raise PermissionError(f"Dekomori lacks '{permission}' permission.")
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def can_message_log_channel(guild):
    """
    Checks if the bot can send messages to the designated log channel.
    It assumes that the first argument is the guild object.

    Parameters
    ----------
    guild : discord.Guild
        The guild object.

    Returns
    -------
    function
        The decorator function.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            guild = args[0]
            logChannelObj = lcsend.get_log_channel(guild)
            if not logChannelObj.permissions_for(guild.me).send_messages:
                guildLogger = logger.get_guild_logger(guild.id)
                guildLogger.critical("Dekomori cannot send messages to the log channel.")
                raise PermissionError("Log channel is not available.")
            return await func(*args, **kwargs)
        return wrapper
    return decorator
# usr/bin/env python3
# -*- coding: utf-8 -*-
import discord
from functools import wraps

from App.utils import logger as logger
from App.core import log_channel_sender_core as lcsender

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
                await lcsender.send_permission_error(guild.id, permission)
                raise PermissionError(f"Dekomori lacks '{permission}' permission.")
            return await func(*args, **kwargs)
        return wrapper
    return decorator
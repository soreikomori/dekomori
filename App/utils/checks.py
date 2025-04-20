# usr/bin/env python3
# -*- coding: utf-8 -*-
import discord
from functools import wraps

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
                raise PermissionError(f"Dekomori lacks '{permission}' permission.")
            return await func(*args, **kwargs)
        return wrapper
    return decorator
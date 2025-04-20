# usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from App.dekomori import client
from App.utils.startup import globalLogger
from App.utils.constants import VERSION

from functools import wraps

from App.utils import logger as logger
from App.core import log_channel_sender_core as lcsend
from App.core import guilds_db_core as gdb

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
                await lcsend.permission_error(guild.id, permission)
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

def can_delete_welcome_messages(guild):
    """
    Checks if the bot can delete the welcome messages in the system channel.
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
            channel = guild.system_channel
            if not channel.permissions_for(guild.me).manage_messages:
                guildLogger = logger.get_guild_logger(guild.id)
                guildLogger.error(f"Dekomori cannot delete messages in the {channel.name} channel.")
                await lcsend.welcome_message_error(guild.id, "manage_messages")
                raise PermissionError("Dekomori lacks 'manage_messages' permission in the channel.")
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def member_join_fullcheck(guild, member):
    """
    Performs the full check for member join events.
    It assumes that the first two arguments are the guild and member objects.
    
    Parameters
    ----------
    guild : discord.Guild
        The guild object.
    member : discord.Member
        The member object.
        
    Returns
    -------
    function
        The decorator function.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            guild = args[0]
            member = args[1]

            await not_paused(guild)
            await can_message_log_channel(guild)
            await bait_roles_exist(guild)
            await not_genuine_bot(member)
            await onboarding_enabled(guild, member)

            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Fullcheck Checks

def not_paused(guild):
    """
    Checks if Dekomori is paused in the guild.
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
            if gdb.is_paused(guild):
                raise Exception("Dekomori is paused in this guild.")
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def bait_roles_exist(guild):
    """
    Checks if the guild has bait roles set and if Dekomori can add them to the user.
    It assumes that the first argument is the guild object.
    
    Parameters
    ----------
    guild : discord.Guild
        The guild object.
    member : discord.Member
        The member object.
        
    Returns
    -------
    function
        The decorator function.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            guild = args[0]
            guildLogger = logger.get_guild_logger(guild.id)
            bait_roles = gdb.get_value(guild.id, "bait_roles")
            if len(bait_roles) == 0:
                guildLogger.error("No bait roles set in the guild.")
                lcsend.bait_roles_missing(guild)
                raise Exception("No bait roles set in the guild.")
        return wrapper
    return decorator

def not_genuine_bot(member):
    """
    Checks if the user is a genuine bot.
    It assumes that the first argument is the member object.
    
    Parameters
    ----------
    member : discord.Member
        The member object.
        
    Returns
    -------
    function
        The decorator function.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            member = args[1]
            if member.bot:
                raise Exception("User is a genuine bot.")
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def onboarding_enabled(guild, member):
    """
    Checks if onboarding is enabled in the guild.
    It assumes that the first argument is the member object.
    
    Parameters
    ----------
    guild : discord.Guild
        The guild object.
    member : discord.Member
        The member object.
        
    Returns
    -------
    function
        The decorator function.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            guild = args[0]
            member = args[1]
            guildLogger = logger.get_guild_logger(guild.id)
            if not member.flags.started_onboarding: # Can assume that if the user did not start onboarding, it is not enabled
                lcsend.onboarding_not_enabled(guild, member)
                raise Exception("Onboarding is not enabled in this guild.")
            return await func(*args, **kwargs)
        return wrapper
    return decorator
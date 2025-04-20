# usr/bin/env python3
# -*- coding: utf-8 -*-
import App.core.guilds_db_core as gdb

def increment_kick_count(guildId):
    """
    Increments the kick count for a specific guild.

    Parameters
    ----------
    guildId : int
        The ID of the guild.
    """
    gdb.update_value(guildId, "kick_count", gdb.get_value(guildId, "kick_count") + 1)

def increment_ban_count(guildId):
    """
    Increments the ban count for a specific guild.

    Parameters
    ----------
    guildId : int
        The ID of the guild.
    """
    gdb.update_value(guildId, "ban_count", gdb.get_value(guildId, "ban_count") + 1)

def get_kick_count(guildId):
    """
    Retrieves the kick count for a specific guild.

    Parameters
    ----------
    guildId : int
        The ID of the guild.

    Returns
    -------
    int
        The kick count for the specified guild.
    """
    return gdb.get_value(guildId, "kick_count")

def get_ban_count(guildId):
    """
    Retrieves the ban count for a specific guild.

    Parameters
    ----------
    guildId : int
        The ID of the guild.

    Returns
    -------
    int
        The ban count for the specified guild.
    """
    return gdb.get_value(guildId, "ban_count")
# usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from App.utils.startup import globalLogger

from tinydb import TinyDB, Query
from DataStructures.watchlist import watchlist as wl
from DataStructures.guildentry import guildentry as ge

DB_PATH = "env/guilds_db.json"
db = TinyDB(DB_PATH)
Guild = Query()

def add_guild(guildId: int, guild_name: str):
    """
    Adds a new guild to the database if it doesn't already exist.
    
    Parameters
    ----------
    guildId : int
        The ID of the guild.
    guild_name : str
        The name of the guild.
    """
    guildId = str(guildId)
    if not db.contains(Guild.id == guildId):
        db.insert(ge.new_guildentry(guildId, guild_name))
        globalLogger.info(f"Added new guild to database: {guildId} - {guild_name}")
    else:
        globalLogger.warning(f"Guild with ID {guildId} already exists in the database. Skipping addition.")
        raise ValueError(f"Guild with ID {guildId} already exists in the database.")

def remove_guild(guildId: int):
    """
    Removes a guild from the database.

    Parameters
    ----------
    guildId : int
        The ID of the guild.
    """
    guildId = str(guildId)
    db.remove(Guild.id == guildId)
    globalLogger.info(f"Removed guild from database: {guildId}")

def get_guild_config(guildId: int):
    """
    Retrieves the configuration for a specific guild.

    Parameters
    ----------
    guildId : int
        The ID of the guild.

    Returns
    -------
    dict or None
        The configuration dictionary for the guild, or None if not found.
    """
    guildId = str(guildId)
    return db.get(Guild.id == guildId)

def update_value(guildId: int, key: str, value):
    """
    Updates a nested field in the guild configuration.

    Parameters
    ----------
    guildId : int
        The ID of the guild.
    key : str
        The key of the field to update in the guild configuration.
    value : any
        The new value to set for the specified field.
    """
    guildId = str(guildId)
    config = get_guild_config(guildId)
    if config:
        config[key] = value
        db.update({key: value}, Guild.id == guildId)
    else:
        raise ValueError(f"Guild with ID {guildId} not found.")

def get_value(guildId: int, key: str):
    """
    Retrieves a value from the guild configuration.

    Parameters
    ----------
    guildId : int
        The ID of the guild.
    key : str
        The key of the field to retrieve from the guild configuration.

    Returns
    -------
    any or None
        The value of the specified field, or None if not found.
    """
    guildId = str(guildId)
    config = get_guild_config(guildId)
    if config:
        return config.get(key, None)
    return None

def get_total_guilds():
    """
    Retrieves the total number of guilds in the database.

    Returns
    -------
    int
        The total number of guilds.
    """
    return len(db.all())

def get_all_guilds():
    """
    Retrieves all guild configurations from the database.

    Returns
    -------
    list of dict
        A list of dictionaries containing the configurations for all guilds.
    """
    return db.all()

# region # Watchlist Related

def get_guilds_with_populated_watchlists():
    """
    Retrieves all guilds with populated watchlists, which means they have users that have not gone through onboarding.
    This function is used in the stall loop to check for users who might be stalled in onboarding.

    Returns
    -------
    list of dict
        A list of dictionaries containing the configurations for guilds with watched users.
    """
    allGuilds = db.all()
    wlGuilds = [guild for guild in allGuilds if not wl.is_empty(guild["watchlist"])]
    return wlGuilds

def is_user_in_watchlist(guild: discord.Guild, member: discord.Member):
    """
    Checks if a user is in the watchlist of a guild.

    Parameters
    ----------
    guild : discord.Guild
        The guild object to check against.
    member : discord.Member
        The member object representing the user to check.
    
    Returns
    -------
    bool
        True if the user is in the watchlist, False otherwise.
    """
    guildId = str(guild.id)
    watchlist = get_value(guildId, "watchlist")
    return wl.is_present(member.id, watchlist)

def remove_user_from_watchlist(guild: discord.Guild, member: discord.Member):
    """
    Removes a user from the watchlist of a guild.

    Parameters
    ----------
    guild : discord.Guild
        The guild object to remove the user from.
    userId : int
        The ID of the user to remove from the watchlist.
    """
    guildId = str(guild.id)
    watchlist = get_value(guildId, "watchlist")
    if wl.is_present(member, watchlist):
        watchlist = wl.remove_user(member.id, watchlist)
        update_value(guildId, "watchlist", watchlist)
        globalLogger.info(f"Removed user {member.name} from watchlist in guild {guild.name} ({guildId}).")

# endregion # Watchlist Related
# region # DM Related

def dm_on_kick(guildId: int):
    """
    Checks if DM on kick is enabled for the specified guild.

    Parameters
    ----------
    guildId : int
        The ID of the guild.

    Returns
    -------
    bool
        True if DM on kick is enabled, False otherwise.
    """
    guildId = str(guildId)
    return get_value(guildId, "dm_on_kick") == True

def dm_on_ban(guildId: int):
    """
    Checks if DM on ban is enabled for the specified guild.

    Parameters
    ----------
    guildId : int
        The ID of the guild.

    Returns
    -------
    bool
        True if DM on ban is enabled, False otherwise.
    """
    guildId = str(guildId)
    return get_value(guildId, "dm_on_ban") == True

def dm_on_kos(guildId: int):
    """
    Checks if DM on kick on stall is enabled for the specified guild.

    Parameters
    ----------
    guildId : int
        The ID of the guild.

    Returns
    -------
    bool
        True if DM on kick on stall is enabled, False otherwise.
    """
    return get_value(guildId, "dm_on_kos") == True

# endregion # DM Related
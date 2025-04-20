# usr/bin/env python3
# -*- coding: utf-8 -*-
from tinydb import TinyDB, Query
from DataStructures.watchlist import watchlist as wl
from DataStructures.guildentry import guildentry as ge

DB_PATH = "env/guilds_db.json"
db = TinyDB(DB_PATH)
Guild = Query()

def add_guild(guild_id: str, guild_name: str):
    """
    Adds a new guild to the database if it doesn't already exist.
    
    Parameters
    ----------
    guild_id : str
        The ID of the guild.
    guild_name : str
        The name of the guild.
    """
    if not db.contains(Guild.id == guild_id):
        db.insert(ge.new_guildentry(guild_id, guild_name))
    else:
        raise ValueError(f"Guild with ID {guild_id} already exists in the database.")

def get_guild_config(guild_id: str):
    """
    Retrieves the configuration for a specific guild.

    Parameters
    ----------
    guild_id : str
        The ID of the guild.

    Returns
    -------
    dict or None
        The configuration dictionary for the guild, or None if not found.
    """
    return db.get(Guild.id == guild_id)

def update_value(guild_id: str, key: str, value):
    """
    Updates a nested field in the guild configuration.

    Parameters
    ----------
    guild_id : str
        The ID of the guild.
    key : str
        The key of the field to update in the guild configuration.
    value : any
        The new value to set for the specified field.
    """
    config = get_guild_config(guild_id)
    if config:
        config[key] = value
        db.update({key: value}, Guild.id == guild_id)
        db.save()
    else:
        raise ValueError(f"Guild with ID {guild_id} not found.")

def get_value(guild_id: str, key: str):
    """
    Retrieves a value from the guild configuration.

    Parameters
    ----------
    guild_id : str
        The ID of the guild.
    key : str
        The key of the field to retrieve from the guild configuration.

    Returns
    -------
    any or None
        The value of the specified field, or None if not found.
    """
    config = get_guild_config(guild_id)
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

# endregion # Watchlist Related
# region # DM Related

def dm_on_kick(guildId: str):
    """
    Checks if DM on kick is enabled for the specified guild.

    Parameters
    ----------
    guildId : str
        The ID of the guild.

    Returns
    -------
    bool
        True if DM on kick is enabled, False otherwise.
    """
    return get_value(guildId, "dm_on_kick") == True

def dm_on_ban(guildId: str):
    """
    Checks if DM on ban is enabled for the specified guild.

    Parameters
    ----------
    guildId : str
        The ID of the guild.

    Returns
    -------
    bool
        True if DM on ban is enabled, False otherwise.
    """
    return get_value(guildId, "dm_on_ban") == True

def dm_on_kos(guildId: str):
    """
    Checks if DM on kick on stall is enabled for the specified guild.

    Parameters
    ----------
    guildId : str
        The ID of the guild.

    Returns
    -------
    bool
        True if DM on kick on stall is enabled, False otherwise.
    """
    return get_value(guildId, "dm_on_kos") == True

# endregion # DM Related
# usr/bin/env python3
# -*- coding: utf-8 -*-
from tinydb import TinyDB, Query

DB_PATH = "env/guilds_db.json"
db = TinyDB(DB_PATH)
Guild = Query()

def default_guild_config(guild_id: str, guild_name: str):
    """
    Creates a default configuration for a new guild.
    
    Parameters
    ----------
    guild_id : str
        The ID of the guild.
    guild_name : str
        The name of the guild.
        
    Returns
    -------
    dict
        A dictionary containing the default configuration for the guild."""
    return {
        "id": guild_id,
        "paused": True,
        "bait_roles": [],
        "watched_users": [],
        "dm_on_kick": False,
        "dm_on_ban": False,
        "dm_on_stallkick": False,
        "spammer_check": False,
        "rejoin_checker": {
            "enabled": False,
            "userId": 0,
            "joinCount": 0,
            "maxJoinCount": 0,
            "pingRoleId": 0,
            "kickuser": True
        },
        "ban": False,
        "log_channel_id": 0,
        "kick_on_stall": False,
        "stall_timeout": 300,
        "kick_dm_message": f"You have been kicked from {guild_name} for suspicious activity.",
        "ban_dm_message": f"You have been banned from {guild_name} for suspicious activity.",
        "stall_dm_message": f"You have been kicked from {guild_name} because you didn't complete onboarding in a while. If you join back, please complete onboarding.",
        "ban_counter": 0,
        "kick_counter": 0,
        "delete_welcome_message": False,
        "welcome_channel_id": 0,
        "debug_logging": False
    }

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
        db.insert(default_guild_config(guild_id, guild_name))
        db.save()
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

def get_guilds_with_watched_users():
    """
    Retrieves all guilds with watched users. Watched users are those in each guild's currenteval list.
    This function is used in the stall loop to check for users who might be stalled in onboarding.

    Returns
    -------
    list of dict
        A list of dictionaries containing the configurations for guilds with watched users.
    """
    all_guilds = db.all()
    watched_guilds = [guild for guild in all_guilds if guild["currenteval"]]
    return watched_guilds
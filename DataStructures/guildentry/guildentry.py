# usr/bin/env python3
# -*- coding: utf-8 -*-
# The guildentry is a data structure that contains information about a guild.

from DataStructures.watchlist import watchlist as wl

def new_guildentry(guildId, guildName):
    """
    Creates a default configuration for a new guild. It requires the guild ID and name at the very least, then the rest of the parameters are set to default values.
    
    Parameters
    ----------
    guildId : int
        The ID of the guild.
    guildName : str
        The name of the guild.
        
    Returns
    -------
    guildentry
        A new guildentry object with default values.
    """
    if not isinstance(guildId, int):
        try:
            guildId = int(guildId)
        except ValueError:
            raise ValueError("guildId must be an integer or a string that can be converted to an integer.")
    return {
        "id": guildId,
        "paused": True,
        "bait_roles": [],
        "watchlist": wl.new_watchlist(),
        "dm_on_kick": False,
        "dm_on_ban": False,
        "dm_on_kos": False,
        "kick_spamflagged": False,
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
        "kick_dm_message": f"You have been kicked from {guildName} for suspicious activity.",
        "ban_dm_message": f"You have been banned from {guildName} for suspicious activity.",
        "kos_dm_message": f"You have been kicked from {guildName} because you didn't complete onboarding in a while. If you join back, please complete onboarding.",
        "ban_counter": 0,
        "kick_counter": 0,
        "delete_welcome_message": False,
        "welcome_channel_id": 0,
        "debug_logging": False
    }

def get(guildentry, key):
    """
    Gets a value from the guildentry.
    
    Parameters
    ----------
    guildentry : guildentry
        The guildentry to get the value from.
    key : str
        The key of the value to get.
        
    Returns
    -------
    any
        The value of the specified key in the guildentry.
    """
    return guildentry.get(key, None)

def reset(guildId, guildName):
    """
    Resets a guild entry to its default values.
    
    Parameters
    ----------
    guildId : int
        The ID of the guild.
    guildName : str
        The name of the guild.
        
    Returns
    -------
    guildentry
        The reset guildentry.
    """
    return new_guildentry(guildId, guildName)
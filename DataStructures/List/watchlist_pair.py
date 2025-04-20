# usr/bin/env python3
# -*- coding: utf-8 -*-
# The watchlist pair is a dictionary with the user ID and a timestamp.
# It's the main structure used to keep track of users in a watchlist.

import datetime
import discord

def new_wlpair(userId, time=datetime.datetime.now()):
    """
    Creates a new watchlist pair.
    
    Parameters
    ----------
    userId : int
        The ID of the user.
    time : datetime.datetime
        The time when the user was added to the watchlist. Defaults to the current time.
        
    Returns
    -------
    wl_pair
        A watchlist pair containing the user ID and time.
    """
    return {
        "userId": userId,
        "time": time
    }

def user_exists(wl_pair, guildObj):
    """
    Checks if a user in the watchlist pair exists in the guild.
    
    Parameters
    ----------
    wl_pair : wl_pair
        The watchlist pair to check.
    guildObj : discord.Guild
        The guild object to check against.
        
    Returns
    -------
    bool
        True if the watchlist pair is valid, False otherwise.
    """
    return discord.utils.get(guildObj.members, id=wl_pair["userId"]) is not None

def get_user_id(wl_pair):
    """
    Gets the user ID from the watchlist pair.
    
    Parameters
    ----------
    wl_pair : wl_pair
        The watchlist pair to get the user ID from.
        
    Returns
    -------
    int
        The user ID from the watchlist pair.
    """
    return wl_pair["userId"]

def get_user_time(wl_pair):
    """
    Gets the time when a user was added to the watchlist.
    
    Parameters
    ----------
    wl_pair : wl_pair
        The watchlist pair to get the time from.
        
    Returns
    -------
    datetime.datetime
        The time when the user was added to the watchlist.
    """
    return wl_pair["time"]
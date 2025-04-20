# usr/bin/env python3
# -*- coding: utf-8 -*-
# The watchlist userpair is a dictionary with the user ID and a timestamp.
# It's the main structure used to keep track of users in a watchlist.

import datetime
import discord

def new_userpair(userId, time=datetime.datetime.now()):
    """
    Creates a new watchlist userpair.
    
    Parameters
    ----------
    userId : int
        The ID of the user.
    time : datetime.datetime
        The time when the user was added to the watchlist. Defaults to the current time.
        
    Returns
    -------
    wl_userpair
        A watchlist userpair containing the user ID and time.
    """
    return {
        "id": userId,
        "time": time
    }

def user_exists(wl_userpair, guildObj):
    """
    Checks if a user in the watchlist userpair exists in the guild.
    
    Parameters
    ----------
    wl_userpair : wl_userpair
        The watchlist userpair to check.
    guildObj : discord.Guild
        The guild object to check against.
        
    Returns
    -------
    bool
        True if the watchlist userpair is valid, False otherwise.
    """
    return discord.utils.get(guildObj.members, id=wl_userpair["id"]) is not None

def get_user_id(wl_userpair):
    """
    Gets the user ID from the watchlist userpair.
    
    Parameters
    ----------
    wl_userpair : wl_userpair
        The watchlist userpair to get the user ID from.
        
    Returns
    -------
    int
        The user ID from the watchlist userpair.
    """
    return wl_userpair["id"]

def get_user_time(wl_userpair):
    """
    Gets the time when a user was added to the watchlist.
    
    Parameters
    ----------
    wl_userpair : wl_userpair
        The watchlist userpair to get the time from.
        
    Returns
    -------
    datetime.datetime
        The time when the user was added to the watchlist.
    """
    return wl_userpair["time"]
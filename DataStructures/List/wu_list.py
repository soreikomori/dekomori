# usr/bin/env python3
# -*- coding: utf-8 -*-
# WuList - Watched Users List

import datetime
import discord

def new_wu(userId, time=datetime.datetime.now()):
    """
    Creates a new watched user entry.
    
    Parameters
    ----------
    userId : int
        The ID of the user.
    time : datetime.datetime
        The time when the user was added to the watched list. Defaults to the current time.
        
    Returns
    -------
    wu_list
        A WuList containing the user ID and time.
    """
    return {
        "userId": userId,
        "time": time
    }

def wuser_is_valid(wu_list, guildObj):
    """
    Checks if a watched user entry is valid.
    
    Parameters
    ----------
    wu_list : wu_list
        The watched user entry to check.
    guildObj : discord.Guild
        The guild object to check against.
        
    Returns
    -------
    bool
        True if the watched user entry is valid, False otherwise.
    """
    if wu_list is None:
        return False
    else:
        userObj = discord.utils.get(guildObj.members, id=wu_list["userId"])
        if userObj is None:
            return False
        else:
            return True
        
def get_wuser_time(wu_list):
    """
    Gets the time when a watched user was added to the list.
    
    Parameters
    ----------
    wu_list : wu_list
        The watched user entry.
        
    Returns
    -------
    datetime.datetime
        The time when the user was added to the watched list.
    """
    return wu_list["time"]

def get_wuser_id(wu_list):
    """
    Gets the user ID of a watched user.
    
    Parameters
    ----------
    wu_list : wu_list
        The watched user entry.
        
    Returns
    -------
    int
        The user ID of the watched user.
    """
    return wu_list["userId"]
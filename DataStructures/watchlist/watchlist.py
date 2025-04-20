# usr/bin/env python3
# -*- coding: utf-8 -*-
# The watchlist is a data structure similar to a queue list.
# It is used to keep track of users that are being watched in a guild.

import datetime
import discord
from DataStructures.watchlist import watchlist_userpair as wlup

def new_watchlist():
    """
    Creates a new watchlist.

    Returns
    -------
    watchlist
        A new watchlist.
    """
    return []

def add(watchlist, userpair):
    """
    Adds a new userpair to the watchlist.

    Parameters
    ----------
    watchlist : watchlist
        The watchlist to add the userpair to.
    userpair : watchlist_useruserpair
        The userpair to add to the watchlist.

    Returns
    -------
    list
        The updated watchlist.
    """
    watchlist.append(userpair)
    return watchlist

def pop(watchlist):
    """
    Pops the first userpair from the watchlist.

    Parameters
    ----------
    watchlist : watchlist
        The watchlist to pop the userpair from.

    Returns
    -------
    watchlist_useruserpair
        The popped userpair.
    """
    return watchlist.pop(0) if watchlist else None

def peek(watchlist):
    """
    Peeks at the first userpair in the watchlist.

    Parameters
    ----------
    watchlist : watchlist
        The watchlist to peek at.

    Returns
    -------
    watchlist_useruserpair
        The first userpair in the watchlist.
    """
    return watchlist[0] if watchlist else None

def is_empty(watchlist):
    """
    Checks if the watchlist is empty.

    Parameters
    ----------
    watchlist : watchlist
        The watchlist to check.

    Returns
    -------
    bool
        True if the watchlist is empty, False otherwise.
    """
    return len(watchlist) == 0

def size(watchlist):
    """
    Gets the size of the watchlist.

    Parameters
    ----------
    watchlist : watchlist
        The watchlist to get the size of.

    Returns
    -------
    int
        The size of the watchlist.
    """
    return len(watchlist)

# Utility Functions

def purge_userpairs(watchlist, guild):
    """
    Purges all userpairs from the watchlist that are not valid in the guild.
    "Not valid" means that the user is not in the guild.

    Parameters
    ----------
    watchlist : watchlist
        The watchlist to purge.
    guild : discord.Guild
        The guild object to check against.

    Returns
    -------
    watchlist
        The purged watchlist.
    """
    wlPurged = [userpair for userpair in watchlist if wlup.user_exists(userpair, guild)]
    return wlPurged

def get_userpair_id(userpair):
    """
    Gets the user ID from the watchlist userpair.

    Parameters
    ----------
    userpair : watchlist_useruserpair
        The watchlist userpair to get the user ID from.

    Returns
    -------
    int
        The user ID from the watchlist userpair.
    """
    return wlup.get_user_id(userpair)

def get_userpair_time(userpair):
    """
    Gets the time when a user was added to the watchlist.

    Parameters
    ----------
    userpair : watchlist_useruserpair
        The watchlist userpair to get the time from.

    Returns
    -------
    datetime.datetime
        The time when the user was added to the watchlist.
    """
    return wlup.get_user_time(userpair)

def remove_userpair(userpair):
    """
    Removes a userpair from the watchlist.

    Parameters
    ----------
    userpair : watchlist_useruserpair
        The watchlist userpair to remove.
    """
    del userpair
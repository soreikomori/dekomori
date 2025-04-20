# usr/bin/env python3
# -*- coding: utf-8 -*-
# The watchlist is a data structure similar to a queue list.
# It is used to keep track of users that are being watched in a guild.

import datetime
import discord
from DataStructures.List import watchlist_pair as wlp

def new_watchlist():
    """
    Creates a new watchlist.

    Returns
    -------
    watchlist
        A new watchlist.
    """
    return []

def add(watchlist, pair):
    """
    Adds a new pair to the watchlist.

    Parameters
    ----------
    watchlist : watchlist
        The watchlist to add the pair to.
    pair : watchlist_pair
        The pair to add to the watchlist.

    Returns
    -------
    list
        The updated watchlist.
    """
    watchlist.append(pair)
    return watchlist

def pop(watchlist):
    """
    Pops the first pair from the watchlist.

    Parameters
    ----------
    watchlist : watchlist
        The watchlist to pop the pair from.

    Returns
    -------
    watchlist_pair
        The popped pair.
    """
    return watchlist.pop(0) if watchlist else None

def peek(watchlist):
    """
    Peeks at the first pair in the watchlist.

    Parameters
    ----------
    watchlist : watchlist
        The watchlist to peek at.

    Returns
    -------
    watchlist_pair
        The first pair in the watchlist.
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

def purge_pairs(watchlist, guildObj):
    """
    Purges all pairs from the watchlist that are not valid in the guild.
    "Not valid" means that the user is not in the guild.

    Parameters
    ----------
    watchlist : watchlist
        The watchlist to purge.
    guildObj : discord.Guild
        The guild object to check against.

    Returns
    -------
    watchlist
        The purged watchlist.
    """
    wlPurged = [pair for pair in watchlist if wlp.user_exists(pair, guildObj)]
    return wlPurged
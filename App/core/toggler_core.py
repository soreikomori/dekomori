# usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from App.dekomori import client
from App.utils.startup import globalLogger
from App.utils.constants import VERSION
from App.utils import exceptions as ex

from App.core import guilds_db_core as gdb

def toggle_dm(guild, action):
    """
    Toggle the DM action for a specific guild.

    Parameters
    ----------
    guild : int
        The ID of the guild.
    action : str
        The action to be performed. Can be either "kick", "ban", or "kos".
    """
    key = f"dm_on_{action}"
    return gdb.toggle(guild, key)

def toggle_delete_wm(guild):
    """
    Toggle the deletion of welcome messages for a specific guild.

    Parameters
    ----------
    guild : int
        The ID of the guild.
    """
    return gdb.toggle(guild, "delete_welcome_message")

def toggle_action(guild):
    """
    Toggle the action (kick or ban) for a specific guild.

    Parameters
    ----------
    guild : int
        The ID of the guild.

    Returns
    -------
    bool, bool
        A tuple containing the new state of the action and whether the rejoin checker was turned off.
    """
    newState = gdb.toggle(guild, "ban") # newState True = ban, False = kick
    rjcActive = gdb.rjc.is_enabled(guild)
    rjcTurnedOff = False
    if newState and rjcActive:
        gdb.rjc.disable(guild)
        rjcTurnedOff = True
    return newState, rjcTurnedOff

def toggle_kos(guild):
    """
    Toggle the kick on stall action for a specific guild.

    Parameters
    ----------
    guild : int
        The ID of the guild.
    """
    return gdb.toggle(guild, "kick_on_stall")
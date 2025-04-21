# usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from App.dekomori import client
from App.utils.startup import globalLogger
from App.utils.constants import VERSION
from App.utils import exceptions as ex
from App.utils import checks as checks

from App.core import guilds_db_core as gdb

def toggle_dm(guild, action):
    """
    Toggle the DM action for a specific guild.

    Parameters
    ----------
    guild : discord.Guild
        The guild object.
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
    guild : discord.Guild
        The guild object.
    """
    return gdb.toggle(guild, "delete_welcome_message")

def toggle_action(guild):
    """
    Toggle the action (kick or ban) for a specific guild.

    Parameters
    ----------
    guild : discord.Guild
        The guild object.

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
    guild : discord.Guild
        The guild object.
    """
    return gdb.toggle(guild, "kick_on_stall")

def toggle_spamflagged(guild):
    """
    Toggle the spam flagged action for a specific guild.

    Parameters
    ----------
    guild : discord.Guild
        The guild object.
    """
    return gdb.toggle(guild, "kick_spamflagged")

@checks.rejoin_checker.has_ping_roles()
@checks.rejoin_checker.has_max_join_count()
@checks.rejoin_checker.action_is_ban()
def toggle_rejoin_checker(guild):
    """
    Toggle the rejoin checker for a specific guild.

    Parameters
    ----------
    guild : discord.Guild
        The guild object.
    """
    return gdb.rjc.toggle(guild)

def toggle_rejoin_checker_kick(guild):
    """
    Toggle the rejoin checker kick action for a specific guild.

    Parameters
    ----------
    guild : discord.Guild
        The guild object.
    """
    return gdb.rjc.toggle_kick(guild)
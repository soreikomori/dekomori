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
        The action to be performed. Can be either "kick", "ban", or "stall".
    """
    action = "kos" if action == "stall" else action
    key = f"dm_on_{action}"
    gdb.toggle(guild, key)
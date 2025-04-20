# usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from App.dekomori import client
from App.utils.startup import globalLogger
from App.utils.constants import VERSION

from App.core import guilds_db_core as gdb

def has_bait_role(guild, member):
    """
    Check if a member has any bait role in the guild.

    Parameters
    ----------
    guild : discord.Guild
        The guild object representing the guild.
    member : discord.Member
        The member object representing the user.

    Returns
    -------
    bool
        True if the member has the bait role, False otherwise.
    """
    baitroleList = gdb.get_bait_roles(guild.id)
    return any(role.id in baitroleList for role in member.roles)


# usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from App.dekomori import client
from App.utils.startup import globalLogger
from App.utils.constants import VERSION

from App.core import guilds_db_core as gdb
from App.utils import logger as logger
from App.utils import actions as actions

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

def is_spammer_kickable(guild, member):
    """
    Check if a member is spamflagged and is kickable.
    A member is considered kickable if the guild chooses to kick spamflagged members.

    Parameters
    ----------
    guild : discord.Guild
        The guild object representing the guild.
    member : discord.Member
        The member object representing the user.

    Returns
    -------
    bool
        True if the member is kickable, False otherwise.
    """
    isSpammer = member.public_flags.spammer
    guildKicksSpamflagged = gdb.get_value(guild.id, "kick_spamflagged")
    return isSpammer and guildKicksSpamflagged

def get_preferred_action(guild):
    """
    Get the preferred action for the guild.

    Parameters
    ----------
    guild : discord.Guild
        The guild object representing the guild.

    Returns
    -------
    str
        The preferred action for the guild.
    """
    return "ban" if gdb.get_value(guild.id, "ban") else "kick"


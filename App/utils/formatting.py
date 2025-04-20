# usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from App.dekomori import client
from App.utils.startup import globalLogger
from App.utils.constants import VERSION

from App.core import guilds_db_core as gdb
from App.utils import logger as logger

def parse_roles(guild, rolestring):
    """
    Parse the role string into a list of role IDs.

    Parameters
    ----------
    guild : discord.Guild
        The guild object representing the guild.
    rolestring : str
        The role string to be parsed. The string can contain multiple roles separated by commas, or a single role.
        The roles can be mentions (e.g., <@&123456789012345678>) or IDs (e.g., 123456789012345678).
        The rolestring can also be "all" to indicate all roles.
        If "all" is provided, all roles in the guild will be returned.

    Returns
    -------
    list
        A list of role IDs.
    """
    guildLogger = logger.get_guild_logger(guild.id)
    if rolestring.lower() == "all": # All roles
        roleList = gdb.get_all_bait_roles(guild)
        guildLogger.debug(f"All roles requested: {roleList}")
        return roleList
    if "," in rolestring:
        roles = [role.strip() for role in rolestring.split(",")]
    else:
        roles = [rolestring.strip()]
    roleList = []
    for role in roles:
        try:
            if role.startswith("<@&") and role.endswith(">"): # Mention
                roleId = int(role[3:-1])
            else: # ID
                roleId = int(role)
            roleList.append(roleId)
        except ValueError: # Invalid
            guildLogger.error(f"Invalid role ID: {role}")
    if len(roleList) == 0:
        raise ValueError("No valid role IDs found.")
    return roleList
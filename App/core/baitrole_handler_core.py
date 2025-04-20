# usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from App.dekomori import client
from App.utils.startup import globalLogger
from App.utils.constants import VERSION
from App.utils import exceptions as ex

from App.core import guilds_db_core as gdb
from App.utils import formatting as fmt

def add_rolestring(guild, rolestring):
    """
    Adds a rolestring (a string of one or more role IDs or mentions) to the bait roles list for a guild.
    
    Parameters
    ----------
    guild : discord.Guild
        The guild object representing the guild.
    rolestring : str
        The rolestring to be added. It can contain multiple role IDs or mentions separated by commas.
    """
    guildLogger = globalLogger.get_guild_logger(guild.id)
    roleList = fmt.parse_rolestring(rolestring)
    if roleList == "all":
        guildLogger.error("Attempted to add all roles to the bait roles list.")
        raise ex.AddAllRolesError("You cannot add all roles to the bait roles list.")
    added = []
    already_in_list = []
    invalid = []
    for roleId in roleList:
        try:
            role = get_role(roleId)
            try:
                gdb.add_bait_role(guild, role.id)
                added.append(role.id)
            except ex.RoleAlreadyInListError:
                guildLogger.error(f"Role already in list: {role}")
                already_in_list.append(role)
        except ValueError:
            guildLogger.error(f"Invalid role: {role}")
            invalid.append(role)
    return {
        "added": added,
        "already": already_in_list,
        "invalid": invalid
    }


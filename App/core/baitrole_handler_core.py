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

    Returns
    -------
    dict
        A dictionary containing the results of the operation. It includes the roles that were added, already in the list, and invalid roles.
    """
    guildLogger = globalLogger.get_guild_logger(guild.id)
    roleList = fmt.parse_rolestring(rolestring)
    if roleList == "all":
        guildLogger.error("Attempted to add all roles to the bait roles list.")
        raise ex.AddAllRolesError("You cannot add all roles to the bait roles list.")

def get_results_dict(guild, roleList, action):
    """
    Takes a list of roles IDs and returns a dictionary of roles that were added, existing, or invalid.
    
    Parameters
    ----------
    guild : discord.Guild
        The guild object representing the guild.
    roleList : list
        A list of role IDs or mentions.
    action : str
        The action to be performed. Can be either "add" or "remove".

    Returns
    -------
    dict
        A dictionary containing the results of the operation. It includes the roles that were added, already in the list, and invalid.
    """
    guildLogger = globalLogger.get_guild_logger(guild.id)
    valid = []
    existing = []
    invalid = []
    for roleId in roleList:
        try:
            role = get_role(roleId)
            try:
                if action == "remove":
                    gdb.remove_bait_role(guild, role.id)
                else:
                    gdb.add_bait_role(guild, role.id)
                valid.append(role.id)
            except ex.RoleAlreadyInListError:
                guildLogger.error(f"Role already in list: {role}")
                existing.append(role)
        except ValueError:
            guildLogger.error(f"Invalid role: {role}")
            invalid.append(role)
    return {
        "valid": valid,
        "existing": existing,
        "invalid": invalid
    }

def get_role(guild, rawRole):
    """
    Retrieves a role object from a guild based on a raw role string.

    Parameters
    ----------
    guild : discord.Guild
        The guild object representing the guild.
    rawRole : str
        The role string to be parsed. It can be a mention (e.g., <@&123456789012345678>) or an ID (e.g., 123456789012345678).
    """
    try:
        if rawRole.startswith("<@&") and rawRole.endswith(">"):
            role_id = rawRole[3:-1]
        else:
            role_id = rawRole
        return guild.get_role(int(role_id))
    except Exception:
        raise ValueError(f"Invalid role: {rawRole}")

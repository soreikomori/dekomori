# usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from App.dekomori import client
from App.utils.startup import globalLogger
from App.utils.constants import VERSION

from discord import app_commands
from discord.ext import commands
from App.core import messages_core as msg
from App.core import baitrole_handler_core as bait
from App.utils import exceptions as ex
from App.utils import logger as logger

@client.hybrid_group(aliases=["br","baitroles"], brief="Add or remove bait roles.")
@app_commands.default_permissions(manage_roles = True)
@commands.has_permissions(manage_roles=True)
async def baitrole(ctx):
    """Add or remove a role from the bait roles list.
    You can also operate multiple roles by separating them with commas inside quotes, for example d!baitrole add "@role1, @role2". You can also remove all roles by typing d!baitrole remove all.

    Parameters
    ----------
    action : str
        The action to be performed. Can be either "add" or "remove".
    role : str
        The role to be added or removed. Can be a mention or an ID. For multiple roles, they must be separated by commas inside quotes.
    """
    guildLogger = logger.getLogger(str(ctx.guild.id))
    await ctx.send(msg.commands.baitrole["no_args"]())
    guildLogger.error(f"{ctx.author.name} didn't specify any arguments for baitrole.")

@baitrole.command(aliases=["a"], brief="Add a role to the bait roles list.")
@commands.has_permissions(manage_roles=True)
async def add(ctx, role):
    """Add a role to the bait roles list. You can also operate multiple roles by separating them with commas inside quotes, for example d!baitrole add "@role1, @role2".

    Parameters
    ----------
    role : str
        The role(s) to be added. Can be a mention or an ID.
    """
    guildLogger = logger.getLogger(str(ctx.guild.id))
    guildLogger.info(f"{ctx.author.name} requested to add baitroles.")
    guildLogger.info(f"Role(s): {role}")
    try:
        result = bait.add_rolestring(ctx.guild, rolestring=role)
    except ex.AddAllRolesError as e:
        await ctx.send(msg.commands.baitrole["add"]["tried_adding_all"]())
        guildLogger.error(f"{ctx.author.name} attempted to add all roles to the bait roles list.")
        return
    if result["added"]:
        await ctx.send(msg.commands.baitrole["add"]["added"](result["added"]))
        guildLogger.info(f"Added roles: {result['added']}")
    if result["existing"]:
        plural = "are" if len(result["existing"]) > 1 else "is"
        await ctx.send(msg.commands.baitrole["add"]["already_in_list"](result["existing"], plural))
        guildLogger.info(f"Roles already in list: {result['already']}")
    if result["invalid"]:
        plural = "are" if len(result["invalid"]) > 1 else "is"
        await ctx.send(msg.commands.baitrole["add"]["invalid"](result["invalid"]))
        guildLogger.info(f"Invalid roles: {result['invalid']}")
    guildLogger.info(f"Completed adding baitroles.")
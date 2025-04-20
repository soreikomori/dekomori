# usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from App.dekomori import client
from App.utils.startup import globalLogger
from App.utils.constants import VERSION

from discord import app_commands
from discord.ext import commands
from App.core import messages_core as msg
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
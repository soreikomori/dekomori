# usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from App.dekomori import client
from App.utils.startup import globalLogger
from App.utils.constants import VERSION
from App.utils import exceptions as ex

from typing import Literal
from discord import app_commands
from discord.ext import commands
from App.core import messages_core as msg
from App.utils import logger as logger

@client.hybrid_group(brief="Set various configurations for Dekomori.")
@app_commands.default_permissions(manage_roles = True)
@commands.has_permissions(manage_roles=True)
async def set(ctx):
    """Set various configurations for Dekomori. You can check their current configuration with d!config.
    """
    guildLogger = logger.getLogger(str(ctx.guild.id))
    await ctx.send(msg.commands.set["no_args"]())
    guildLogger.error(f"{ctx.author.name} didn't specify any arguments for set.")
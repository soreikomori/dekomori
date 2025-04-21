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
from App.core import toggler_core as tgl
from App.utils import logger as logger

@client.hybrid_group(brief="Toggle various settings for Dekomori.")
@app_commands.default_permissions(manage_roles = True)
@commands.has_permissions(manage_roles=True)
async def toggle(ctx):
    """Toggle various settings for Dekomori. You can check their status with d!config."""
    guildLogger = logger.getLogger(str(ctx.guild.id))
    await ctx.send(msg.commands.toggle["no_args"]())
    guildLogger.error(f"{ctx.author.name} didn't specify any arguments for toggle.")


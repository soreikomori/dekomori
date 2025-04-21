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
from App.core import set_core as sc
from App.utils import logger as logger
from App.utils import formatting as fmt

@client.hybrid_group(brief="Set various configurations for Dekomori.")
@app_commands.default_permissions(manage_roles = True)
@commands.has_permissions(manage_roles=True)
async def set(ctx):
    """Set various configurations for Dekomori. You can check their current configuration with d!config.
    """
    guildLogger = logger.getLogger(str(ctx.guild.id))
    await ctx.send(msg.commands.set["no_args"]())
    guildLogger.error(f"{ctx.author.name} didn't specify any arguments for set.")

@set.command(aliases=["logchan", "setlogchannel", "setlogchan"], brief="Set the log channel for Dekomori.")
@commands.has_permissions(manage_roles=True)
async def logchannel(ctx, channel: discord.TextChannel):
    """Set the channel where Dekomori will log the actions taken. You can check the current one with d!config.
    
    Parameters
    ----------
    channel : str
        The channel to be set as the log channel. Can be a mention or an ID.
    """
    guildLogger = logger.getLogger(str(ctx.guild.id))
    try:
        sc.set_log_channel(ctx.guild, channel)
    except PermissionError:
        await ctx.send(msg.commands.set["logchannel"]["no_perms"]())
        guildLogger.error(f"{ctx.author.name} tried to set the log channel to a channel Dekomori can't send messages in.")
    guildLogger.info(f"{ctx.author.name} set the log channel to {channel.mention}.")
    await ctx.send(msg.commands.set["logchannel"]["valid"](channel.mention))

@set.command(aliases=["st", "stalltimeout", "jointimer", "jointimeout"], brief="Set the stall timer for Dekomori.")
@commands.has_permissions(manage_roles=True)
async def stalltimer(ctx, time: int):
    """Set the stall timer for Dekomori. This is the time in seconds a user has to complete the onboarding process before being kicked.
    
    Parameters
    ----------
    time : int
        The time in seconds a user has to complete the onboarding process.
    """
    # TODO check
    if time < 60:
        await ctx.send(msg.commands.set["stalltimer"]["too_short"]())
        return
    elif time > 604800:
        await ctx.send(msg.commands.set["stalltimer"]["too_long"]())
        return
    guildLogger = logger.getLogger(str(ctx.guild.id))
    sc.set_stall_timeout(ctx.guild, time)
    parsedTime = fmt.parse_duration(time)
    guildLogger.info(f"{ctx.author.name} set the stall timer to {parsedTime} seconds.")
    await ctx.send(msg.commands.set["stalltimer"]["valid"](parsedTime))
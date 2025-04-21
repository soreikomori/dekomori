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

@toggle.command(aliases=["dmuser"], brief="Toggle DMs on detection of bait roles.")
@commands.has_permissions(manage_roles=True)
async def dm(ctx, action:Literal["kick", "ban", "stall"]):
    """Toggle DMs on detection of bait roles. If enabled, Dekomori will DM the user before taking action. You can check its status with d!config.

    Parameters
    ----------
    action : str
        The action to be performed. Can be either "kick", "ban", or "stall".
    """
    action = "kos" if action == "stall" else action
    guildLogger = logger.getLogger(str(ctx.guild.id))
    newValue = tgl.toggle_dm(ctx.guild.id, action)
    state = "on" if newValue else "off"
    guildLogger.info(f"{ctx.author.name} turned {state} DM on {action}.")
    await ctx.send(msg.commands.toggle["dm"][action][state]())

@toggle.command(aliases=["wm", "wmdel", "welcomemessage", "deletewelcomemessage"], brief="Toggle deletion of welcome messages.")
@commands.has_permissions(manage_guild=True)
async def delwm(ctx):
    """Toggle deletion of welcome messages. If enabled, Dekomori will delete the default welcome message for new users. You can check its status with d!config.
    """
    guildLogger = logger.getLogger(str(ctx.guild.id))
    newValue = tgl.toggle_delete_wm(ctx.guild.id)
    state = "on" if newValue else "off"
    guildLogger.info(f"{ctx.author.name} turned {state} deletion of welcome messages.")
    await ctx.send(msg.commands.toggle["delwm"][state]())

@toggle.command(aliases=["ban", "kick"], brief="Toggle between banning and kicking users with bait roles.")
@commands.has_permissions(manage_roles=True)
async def action(ctx):
    """Toggle between banning and kicking users with bait roles. By default, Dekomori will kick users with bait roles. You can check its status with d!config.
    """
    guildLogger = logger.getLogger(str(ctx.guild.id))
    newState, rjcTurnedOff = tgl.toggle_action(ctx.guild.id)
    guildLogger.info(f"{ctx.author.name} toggled action to {newState}.")
    await ctx.send(msg.commands.toggle["action"][newState]())
    if rjcTurnedOff:
        guildLogger.warning("As the action was changed to ban, the rejoin checker has been disabled.")
        await ctx.send(msg.commands.toggle["action"]["rjc_off"]())

@toggle.command(aliases=["kos", "stallkick"], brief="Toggle kicking on stall.")
@commands.has_permissions(manage_roles=True)
async def kickonstall(ctx):
    """Toggle kicking on stall. If enabled, Dekomori will kick users who stall in the onboarding process. You can check its status with d!config.
    """
    guildLogger = logger.getLogger(str(ctx.guild.id))
    newValue = tgl.toggle_kos(ctx.guild.id)
    state = "on" if newValue else "off"
    guildLogger.info(f"{ctx.author.name} turned {state} kick on stall.")
    await ctx.send(msg.commands.toggle["kos"][state]())
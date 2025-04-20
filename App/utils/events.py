# usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from App.dekomori import client
from App.utils.startup import globalLogger
from App.utils.constants import VERSION

from App.utils import startup as startup
from App.utils import logger as logger
from App.core import stall_loop_core as stall_loop
from App.core import guilds_db_core as gdb
from App.core import evaluation_core as evaluation

@client.event
async def on_ready():
    print(f"Dekomori Sanae, koko ni suisu!")
    print(f"Logged in succesfully as {client.user}.")
    startup.setup_rich_presence()
    startup.initialize_loggers()
    print("Ready!")
    stall_loop.initialize_stall_loop()

@client.event
async def on_guild_join(guild):
    """
    Event handler for when the bot joins a new guild.
    
    Parameters
    ----------
    guild : discord.Guild
        The guild object representing the guild the bot has joined.
    
    """
    globalLogger.info(f"Joined {guild.name} ({guild.id}).")
    gdb.add_guild(guild.id, guild.name) # Database addition
    guildLogger = startup.initialize_guild_logger(guild.id)
    # Log the event of joining the guild
    guildLogger.info(f" - - - Dekomori has joined {guild.name}! - - - ")
    guildLogger.info(f"First Setup - Dekomori {VERSION}")

@client.event
async def on_guild_remove(guild):
    """
    Event handler for when the bot is removed from a guild.
    
    Parameters
    ----------
    guild : discord.Guild
        The guild object representing the guild the bot has been removed from.
    
    """
    globalLogger.info(f"Left {guild.name} ({guild.id}).")
    guildLogger = logger.get_guild_logger(guild.id)
    guildLogger.info(f" - - - Dekomori has left {guild.name}. Goodbye! - - - ")
    gdb.remove_guild(guild.id)

@client.event
async def on_member_remove(member):
    """
    Event handler for when a member is removed from a guild.
    
    Parameters
    ----------
    member : discord.Member
        The member object representing the member who has been removed.
    
    """
    guild = member.guild
    guildLogger = logger.get_guild_logger(guild.id)
    guildLogger.debug(f"Member {member.name} ({member.id}) has left.")
    if gdb.is_user_in_watchlist(guild, member):
        gdb.remove_user_from_watchlist(guild, member)

@client.event
async def on_member_update(_, after):
    """
    Event handler for when a member is updated.
    This function is Dekomori's core.
    
    Parameters
    ----------
    after : discord.Member
        The member object representing the member after the update.
    
    """
    guild = after.guild
    guildLogger = logger.get_guild_logger(guild.id)
    member = after
    if not gdb.is_user_in_watchlist(guild, member) and after.flags.completed_onboarding: # Main checker for onboarding
        return # If the user is not in the watchlist or has not completed onboarding, does nothing
    guildLogger.debug(f"Member {member.name} ({member.id}) has completed onboarding.")
    evaluation.evaluate_member(guild, member)
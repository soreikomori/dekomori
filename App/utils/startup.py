import discord
import json
import os
import logging

from App.utils import config as config
from App.utils import logger as logger
from App.utils.constants import VERSION
from App.core import guilds_db_core as gdb

def initialize_global_logger():
    """
    Initializes the global logger for the bot.

    Returns
    -------
    logging.Logger
        The global logger instance.
    """
    global globalLogger
    globalLogger = logger.setup_logger("global", level=logging.INFO, filename="dekomori.log")
    return globalLogger

async def setup_rich_presence(client):
    """
    Sets up the Rich Presence for the Discord client.

    Parameters
    ----------
    client : discord.Client
        The Discord client instance.
    """
    rpMessage = config.get_config("rp_message")
    await client.change_presence(activity=discord.CustomActivity(name=rpMessage))

def initialize_all_guild_loggers(client_guilds):
    """
    Initializes the loggers for each guild.

    Parameters
    ----------
    client_guilds : list
        List of guilds the client is in.
    """
    for guild in client_guilds:
        initialize_guild_logger(str(guild.id))

def initialize_guild_logger(guildId):
    """
    Initializes the logger for a specific guild.

    Parameters
    ----------
    guildId : str
        The ID of the guild.
    """
    globalLogger.debug(f"Initializing logger for guild: {guildId}")
    guildLogLevel = gdb.get_value(guildId, "log_level")
    guildLogger = logger.setup_guild_logger(guildId, guildLogLevel)
    guildLogger.info(f" - - - Dekomori {VERSION} Reconnected! - - - ")
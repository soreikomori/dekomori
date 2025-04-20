import discord
import json
import os

from App.utils import config as config
from App.utils import logger as logger
from App.utils.constants import VERSION
from App.core import guilds_db_core as gdb

globalLogger = logger.get_global_logger()

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

def initialize_loggers(client_guilds):
    """
    Initializes the loggers for each guild.

    Parameters
    ----------
    client_guilds : list
        List of guilds the client is in.
    """
    for guild in client_guilds:
        globalLogger.debug(f"Initializing logger for guild: {guild.name} ({guild.id})")
        guildId = str(guild.id)
        guildLogLevel = gdb.get_value(guildId, "log_level")
        guildLogger = logger.setup_guild_logger(guildId, guildLogLevel)
        guildLogger.info(f" - - - Dekomori {VERSION} Reconnected! - - - ")
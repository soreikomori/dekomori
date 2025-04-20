# usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from App.dekomori import client
from App.utils.startup import globalLogger
from App.utils.constants import VERSION

from App.utils import logger as logger
from App.core import guilds_db_core as gdb

async def kick_on_stall_dm(member, guildId):
    """
    Checks if the guild has a kick on stall DM enabled and sends a DM to the user if it does.
    
    Parameters
    ----------
    member : discord.Member
        The member object representing the user to be kicked.
    guildId : int
        The ID of the guild.    
    """
    if gdb.dm_on_kos(guildId):
        message = gdb.get_value(guildId, "kos_dm_message")
        guildLogger = logger.get_guild_logger(guildId)
        dmChannel = await member.create_dm()
        try:
            await dmChannel.send(content=message)
            guildLogger.info(f"Sent kick on stall DM to {member.name} ({member.id}).")
        except discord.errors.Forbidden:
            guildLogger.warning(f"Could not send kick on stall DM to {member.name} ({member.id}).")

from App.core.guilds_db_core import add_guild
from App.dekomori import client
from App.utils import startup as startup
from App.core import stall_loop_core as stall_loop

@client.event
async def on_ready():
    print(f"Dekomori Sanae, koko ni suisu!")
    print(f"Logged in succesfully as {client.user}.")
    startup.setup_rich_presence(client)
    startup.initialize_loggers(client.guilds)
    stall_loop.initialize_stall_loop(client)



"""
@client.event
async def on_guild_join(guild):
    guildId = str(guild.id)
    globalLogger.info(f"Joined {guild.name} ({guildId}). Adding to TinyDB.")

    add_guild(guildId, guild.name)
    
    guildLogger = logging.getLogger(guildId)
    setup_logger(guildLogger, guild)
    
    guildLogger.info(f" - - - Dekomori has joined {guild.name}! - - - ")
    guildLogger.info(f"First Setup - Dekomori {version}")
"""
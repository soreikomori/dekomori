import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "env/logs"
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger(loggerName, level=logging.INFO, filename="dekomori.log"):
    """
    Sets up a logger object.

    Parameters
    ----------
    loggerName : str
        Logger name to be used.
    level : Literal[logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL], optional
        Logging level, by default logging.INFO.
    filename : str, optional
        Filename for the log file, by default "dekomori.log".
    """
    logger = logging.getLogger(loggerName)
    logger.setLevel(level)
    log_path = os.path.join(LOG_DIR, filename)
    handler = RotatingFileHandler(log_path, maxBytes=125_000, backupCount=1, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def setup_guild_logger(guildId, level):
    """
    Sets up a logger object for a specific guild.
    
    Parameters
    ----------
    guild_id : int
        Guild ID to be used.
    level : Literal[logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL], optional
        Logging level."""
    guildId = str(guildId)
    return setup_logger(guildId, level=level, filename=f"{guildId}.log")

def get_guild_logger(guild_id):
    """
    Gets a logger object for a specific guild.
    
    Parameters
    ----------
    guild_id : int
        Guild ID to be used.
    
    Returns
    -------
    logging.Logger
        Logger object for the specified guild.
    """
    return logging.getLogger(str(guild_id))

def get_global_logger():
    """
    Gets the global logger object.
    
    Returns
    -------
    logging.Logger
        Global logger object.
    """
    return logging.getLogger("global")
import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "env/logs"
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger(logger_name, level=logging.INFO, filename="dekomori.log"):
    """
    Sets up a logger object.

    Parameters
    ----------
    logger_name : str
        Logger name to be used.
    level : Literal[logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL], optional
        Logging level, by default logging.INFO.
    filename : str, optional
        Filename for the log file, by default "dekomori.log".
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    log_path = os.path.join(LOG_DIR, filename)
    handler = RotatingFileHandler(log_path, maxBytes=125_000, backupCount=1, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def setup_guild_logger(guild_id, level):
    """
    Sets up a logger object for a specific guild.
    
    Parameters
    ----------
    guild_id : int
        Guild ID to be used.
    level : Literal[logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL], optional
        Logging level."""
    return setup_logger(f"guild_{guild_id}", level=level, filename=f"{guild_id}.log")
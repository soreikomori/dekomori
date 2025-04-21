# usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from App.dekomori import client
from App.utils.startup import globalLogger
from App.utils.constants import VERSION

from App.core import guilds_db_core as gdb
from App.utils import logger as logger

def parse_rolestring(rolestring):
    """
    Parse the role string into a list of role IDs.

    Parameters
    ----------
    rolestring : str
        The role string to be parsed. The string can contain multiple roles separated by commas, or a single role.
        The roles can be mentions (e.g., <@&123456789012345678>) or IDs (e.g., 123456789012345678).
        The rolestring can also be "all" to indicate all roles.

    Returns
    -------
    list
        A list of role IDs.
    """
    return rolestring.split(",") if rolestring != "all" else "all"

def format_command_list(commands):
    """
    Formats a list of command names into a string that looks like:
    `command1`, `command2`, and `command3`.

    Parameters
    ----------
    commands : list
        The list of command names. Given by constants.get_commands_list(client).

    Returns
    -------
    str
        The formatted command string. For example, if the input is ["command1", "command2", "command3"],
        the output will be "`command1`, `command2`, and `command3`".
    """
    if not commands:
        raise ValueError("The commands list is empty.")
    if len(commands) > 1:
        return f"`{', '.join(commands[:-1])}` and `{commands[-1]}`"
    return f"`{commands[0]}`"

def parse_time(seconds):
    """
    Parse a duration in seconds into a human-readable format.

    Parameters
    ----------
    seconds : int
        The duration in seconds.

    Returns
    -------
    str
        The parsed duration in a human-readable format.
    """
    # TODO Check this
    if seconds < 60:
        return f"{seconds} second{'s' if seconds != 1 else ''}"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''}"
    elif seconds < 86400:
        hours = seconds // 3600
        return f"{hours} hour{'s' if hours != 1 else ''}"
    else:
        days = seconds // 86400
        return f"{days} day{'s' if days != 1 else ''}"
# usr/bin/env python3
# -*- coding: utf-8 -*-
from App.dekomori import client

VERSION = "Beta 2.0.0"

def get_commands_list(client):
    """
    Fetches the command names from all the cogs the bot is using.
    
    Parameters
    ----------
    client : discord.Client
        The Discord client instance.
    
    Returns
    -------
    dict
        A dictionary containing the command names as keys and their respective cog names as values.
    """
    commands = {}
    for cog_name, cog in client.cogs.items():
        for command in cog.get_commands():
            if command.name not in commands:
                commands[command.name] = [cog_name]
            else:
                commands[command.name].append(cog_name)
    return commands
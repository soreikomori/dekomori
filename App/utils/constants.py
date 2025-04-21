# usr/bin/env python3
# -*- coding: utf-8 -*-
from App.dekomori import client
import os
import discord
import json
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

cogIdsPath = '../../env/cog_ids.json'

async def update_cog_ids(client: discord.Client):
    """
    Fetches all application commands (cogs) and writes their names and IDs to cog_ids.json.

    Parameters
    ----------
    client : discord.Client
        The Discord client instance.
    """
    app_commands = await client.tree.fetch()
    command_ids = {}
    for command in app_commands:
        command_ids[command.name] = command.id
    with open(cogIdsPath, "w") as f:
        json.dump(command_ids, f, indent=4)

def get_cog_ids():
    """
    Reads cog IDs from cog_ids.json.

    Returns
    -------
    dict
        A dictionary containing command names and their respective IDs.
    """
    if not os.path.exists(cogIdsPath):
        raise FileNotFoundError(f"Command IDs file not found: {cogIdsPath}")
    with open(cogIdsPath, "r") as f:
        return json.load(f)

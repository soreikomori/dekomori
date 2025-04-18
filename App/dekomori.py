# usr/bin/env python3
# -*- coding: utf-8 -*-
# Dekomori by soreikomori
# Futsuwu ni nagareteku nichijou ni - muri shite najimaseta
# Shizunjimatta koseitachi wo kande nonde haite warau
import discord
from discord.ext import commands
import os
from App.help_command import InteractionHelpCommand
from App.scheduler.stall_loop import stall_loop

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix='d!', intents=intents, help_command=InteractionHelpCommand())

@client.event
async def on_ready():
    print(f"Dekomori Sanae, koko ni suisu!")
    print(f"Logged in succesfully as {client.user}.")
    client.loop.create_task(stall_loop(client))

# Automatically load all cogs in App/commands/
for filename in os.listdir("App/commands"):
    if filename.endswith(".py") and filename != "__init__.py":
        client.load_extension(f"App.commands.{filename[:-3]}")

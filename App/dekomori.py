# usr/bin/env python3
# -*- coding: utf-8 -*-
# Dekomori by soreikomori
# Futsuwu ni nagareteku nichijou ni - muri shite najimaseta
# Shizunjimatta koseitachi wo kande nonde haite warau
import discord
from discord.ext import commands
import os
from App.commands.help import InteractionHelpCommand
from App.core.stall_loop_core import stall_loop

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix='d!', intents=intents, help_command=InteractionHelpCommand())

for filename in os.listdir("App/commands"):
    if filename.endswith(".py") and filename != "__init__.py":
        client.load_extension(f"App.commands.{filename[:-3]}")
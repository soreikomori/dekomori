import os
from dotenv import load_dotenv
from App.dekomori import bot

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
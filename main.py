import os
from dotenv import load_dotenv
from App.utils import startup as startup
from App.dekomori import client

load_dotenv(dotenv_path="env/.env")
TOKEN = os.getenv("DISCORD_TOKEN")
startup.initialize_global_logger()
client.run(TOKEN)
import os
from dotenv import load_dotenv
from App.dekomori import client

load_dotenv(dotenv_path="env/.env")
TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
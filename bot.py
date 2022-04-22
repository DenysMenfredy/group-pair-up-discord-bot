import os
import discord
from dotenv import load_dotenv
from client import MyClient

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = MyClient(guild_name=GUILD)

# client.delete_all_channels()

client.run(TOKEN)

import os
import discord
from dotenv import load_dotenv
from client import MyClient

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


intents = discord.Intents().all()
client = MyClient(guild_name=GUILD, intents=intents)


client.run(TOKEN)

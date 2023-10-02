import discord
import pandas as pd
from discord.ext import commands

from apikeys import *

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
guild = discord.Guild

@client.event
async def on_ready():
    print("The bot is now ready for use")
    print("-----------------------------")

@client.event
async def on_message(message):
    print("Author of the msg",message.author)
    print("-----------------------------")
    if message.author == client.user:
        return 
    elif message.content.startswith('!bot'):
        print("Author: ",message.author," Content: ",message.content+" Channel: ",message.channel," Created: ",message.created_at)
        await message.channel.send("Hi from ScalerEvalBot")

client.run(DISCORD_BOT_TOKEN)



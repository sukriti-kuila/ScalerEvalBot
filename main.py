import discord
from discord.ext import commands

from apikeys import *

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@client.event
async def on_ready():
    print("The bot is now ready for use")
    print("-----------------------------")

@client.command()
async def hello(ctx):
    await ctx.send("Hello, I am Bot")

client.run(DISCORD_BOT_TOKEN)



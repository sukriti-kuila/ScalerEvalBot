import discord
from discord.ext import commands
from decouple import config

from utils import *

#token
discord_api_key = config('DISCORD_BOT_TOKEN')

# initialize bot
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# here, on_ready() tells that bot is ready to receive command
# This is for testing
@client.event
async def on_ready():
    print("The bot is now ready for use")
    print("-----------------------------")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # Reading participant data
    if message.content.lower().startswith("!evalbot new event"):
        if message.author.id == message.channel.guild.owner_id:
            response = await eventData(message)
            await message.channel.send(response)
    # Checking the desired Format
    elif message.content.lower().startswith("!evalbot"):
        response = await fomatting_check(message)
        await message.channel.send(response)

@client.event
async def on_message_edit(before, after):
    if after.author == client.user:
        return
    if after.content.lower().startswith("!evalbot new event"):
        if after.author.id == after.channel.guild.owner_id:
            response = await eventData(after)
            await after.channel.send(response)
    elif after.content.lower().startswith("!evalbot"):
        response = await fomatting_check(after)
        await after.channel.send (response)

# it tells the bot to run
client.run(discord_api_key)



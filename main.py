import discord
from discord.ext import commands
from decouple import config
import pandas as pd

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
            if response["success"]:
                embed = discord.Embed(title="Event Added!", description=response["message"], color=0x006600, timestamp = message.created_at)
            else:
                embed = discord.Embed(title="Failed to add event", description=response["message"], color=0xcc0000, timestamp = message.created_at) 
            await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(title="Permission Denied", description="Sorry, you're not authorized to perform this command", color=0xcc0000, timestamp = message.created_at) 
            await message.channel.send(embed=embed)

    # Delete event from database
    elif message.content.lower().startswith("!evalbot delete event"):
        if message.author.id == message.channel.guild.owner_id:
            response = await delete_event(message)
            print(response)
            if response["success"]:
                embed = discord.Embed(title="Event Deleted", description=response["message"], color=0x34eb71, timestamp = message.created_at)   
            else:
                embed = discord.Embed(title="Something went wrong", description=response["message"], color=0xe60000, timestamp = message.created_at)
            await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(title="Permission Denied", description="Sorry, you're not authorized to perform this command", color=0xcc0000, timestamp = message.created_at) 
            await message.channel.send(embed=embed)

    # Export Eligible Participants' list in csv format
    elif message.content.lower().startswith("!evalbot res event"):
        if message.author.id == message.channel.guild.owner_id:
            message_str = str(message.content).split("\n")
            if len(message_str) == 2:
                event_name = message_str[1]
                response = await exportResultCSV(event_name)
                if response["success"]:
                    owner = message.author
                    await owner.send(file=response["message"])
                    embed = discord.Embed(title="CSV file generated", description="File has been sent to your DM", color=0x34eb71, timestamp = message.created_at)
                    await message.channel.send(embed=embed)
                else:
                    embed = discord.Embed(title="Something went wrong", description=response["message"], color=0xe60000, timestamp = message.created_at)
                    await message.channel.send(embed=embed)
            else:
                embed = discord.Embed(title="Incorrect Format", description="Looks Like you forgot to mention **event name**", color=0xe60000, timestamp = message.created_at)
                await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(title="Permission Denied", description="Sorry, you're not authorized to perform this command", color=0xcc0000, timestamp = message.created_at) 
            await message.channel.send(embed=embed)
    
    # Checking the desired Format
    elif message.content.lower().startswith("!evalbot"):
        response = await fomatting_check(message)
        if response["success"]:
            response = f'**{message.author.display_name.upper()}**, {response["message"]}'
            embed = discord.Embed(title="Correct Format", description=response, color=0x4dff4d, timestamp = message.created_at)
        else:
            embed = discord.Embed(title="Incorrect Format", description=response["message"], color=0xe60000, timestamp = message.created_at)     
        await message.channel.send(embed=embed)


@client.event
async def on_message_edit(before, after):
    if after.author == client.user:
        return
    
    #New Event add
    if after.content.lower().startswith("!evalbot new event"):
        if after.author.id == after.channel.guild.owner_id:
            response = await eventData(after)
            if response["success"]:
                embed = discord.Embed(title="Event Added!", description=response["message"], color=0x006600, timestamp = after.created_at)
            else:
                embed = discord.Embed(title="Failed to add event", description=response["message"], color=0xcc0000, timestamp = after.created_at) 
            await after.channel.send(embed=embed)

    #fomatting check
    elif after.content.lower().startswith("!evalbot"):
        response = await fomatting_check(after)
        if response["success"]:
            response = f'**{after.author.name.upper()}**, {response["message"]}'
            embed = discord.Embed(title="Correct Format", description=response, color=0x4dff4d, timestamp = after.created_at)
        else:
            embed = discord.Embed(title="Incorrect Format", description=response["message"], color=0xe60000, timestamp = after.created_at)     
        await after.channel.send(embed=embed)

# it tells the bot to run
client.run(discord_api_key)
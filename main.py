import discord
from discord.ext import commands
from apikeys import *
import re
from datetime import datetime, timedelta

# initialize bot
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
guild = discord.Guild


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
    
    message_str = str(message.content).split("\n")
    print(message_str)

    if(len(message_str) < 2):
        await message.channel.send("Follow the format carefully")
        # break here

    first_line = message_str[0].split()
    bot_command = first_line[0].lower()
    completion_command = first_line[1 : len(first_line)]

    Second_line = message_str[1]
    post_pattern = r'^social media link : https://(www.linkedin.com|twitter.com)/+'

    start_date = datetime(2023, 2, 20)
    result_date = start_date + timedelta(days=30)
    day_diff = (result_date - start_date).days

    if len(first_line) == 3 and bot_command == "!bot" and completion_command[0].lower() == "completed" and completion_command[1][0:3].lower() == "day" and (0 < int(completion_command[1][3:len(completion_command[1])]) < day_diff):
        if re.match(post_pattern, Second_line.lower()):
            print("Author: ",message.author," Content: ",message.content+" Channel: ",message.channel," Created: ",message.created_at)
            await message.channel.send("You have successfully completed today's task")
        else:
            await message.channel.send("You have made a formating mistake in line 2 \n Use this format : social media link : <linkedin/twitter post> (not case-sensitive)")

    else:
        await message.channel.send("You have made a formating mistake in line 1 \n Use this format : !bot completed day<day no> (not case-sensitive)")


# it tells the bot to run
client.run(DISCORD_BOT_TOKEN)



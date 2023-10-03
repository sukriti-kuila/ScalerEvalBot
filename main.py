import discord
from discord.ext import commands
from apikeys import *
import re
from datetime import datetime, timedelta
import pytz


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


    start_time = datetime(2023, 10, 1) + timedelta(hours = 11, minutes = 00, seconds = 00)
    challenge_days = 30
    current_time = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")
    # convert String type to datetime object
    current_time = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")

    day_no = (current_time - start_time).days + 1

    
    if len(first_line) == 3 and bot_command == "!bot" and completion_command[0].lower() == "completed" and completion_command[1][0:3].lower() == "day" and (0 < int(completion_command[1][3:len(completion_command[1])]) <= challenge_days) and int(completion_command[1][3:len(completion_command[1])]) == day_no:
        if re.match(post_pattern, Second_line.lower()):
            print("Author: ",message.author," Content: ",message.content+" Channel: ",message.channel," Created: ",message.created_at)
            await message.channel.send("You have successfully completed today's task")
        else:
            await message.channel.send("You have made a formatting mistake in line 2 \n Use this format : social media link : <linkedin/twitter post> (not case-sensitive)")

    else:
        await message.channel.send("You have made a formatting mistake in line 1 \n Use this format : !bot completed day<day no> (not case-sensitive)")


# it tells the bot to run
client.run(DISCORD_BOT_TOKEN)



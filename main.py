from Utils.addNewEvent import *
from Utils.connection import *
from Utils.dayNumber import *
from Utils.deleteEvent import *
from Utils.eligibleList import *
from Utils.formatCheck import *
from Utils.setReminder import *
from Utils.updateToken import *
from Utils.slashCommands import *
from Utils.libraries import *

#token
discord_api_key = config('DISCORD_BOT_TOKEN')

# initialize bot
client = commands.Bot(command_prefix="!", intents=nextcord.Intents.all())

@tasks.loop()
async def main():
    current_time = datetime.now(pytz.timezone('Asia/Kolkata'))
    target_time = current_time.replace(hour=11, minute=0, second=0)
    if current_time > target_time:
        target_time += timedelta(days=1)

    initial_delay = (target_time - current_time).total_seconds()
    await asyncio.sleep(initial_delay)

    while True:
        response = await set_reminder()
        for ele in response:
            for key,value in ele.items():
                user = client.get_user(key)
                if user:
                    event_str = ""
                    for events in value:
                        event_str += events+"  "
                    await user.send(f"**REMINDER**\nYou haven't yet posted today's task post for the event(s) {event_str}")
                else:    
                    print("User not found")
        await asyncio.sleep(3600)

# here, on_ready() tells that bot is ready to receive command
# This is for testing
@client.event
async def on_ready():
    print("The bot is now ready for use")
    print("-----------------------------")
    main.start()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # Reading participant data
    if message.content.lower().startswith("!evalbot new event"):
        if message.author.id == message.channel.guild.owner_id:
            response = await eventData(message)
            if response["success"]:
                embed = nextcord.Embed(title="EVENT ADDED!", description=response["message"], color=0x006600, timestamp = message.created_at)
            else:
                embed = nextcord.Embed(title="Failed to add event", description=response["message"], color=0xcc0000, timestamp = message.created_at) 
            await message.channel.send(embed=embed)
        else:
            embed = nextcord.Embed(title="PERMISSION DENIED", description="Sorry, you're not authorized to perform this command", color=0xcc0000, timestamp = message.created_at) 
            await message.channel.send(embed=embed)

    # Delete event from database
    elif message.content.lower().startswith("!evalbot delete event"):
        if message.author.id == message.channel.guild.owner_id:
            response = await delete_event(message)
            print(response)
            if response["success"]:
                embed = nextcord.Embed(title="EVENT DELETED", description=response["message"], color=0x34eb71, timestamp = message.created_at)   
            else:
                embed = nextcord.Embed(title="Something went wrong", description=response["message"], color=0xe60000, timestamp = message.created_at)
            await message.channel.send(embed=embed)
        else:
            embed = nextcord.Embed(title="PERMISSION DENIED", description="Sorry, you're not authorized to perform this command", color=0xcc0000, timestamp = message.created_at) 
            await message.channel.send(embed=embed)

    # Export Eligible Participants' list in csv format
    elif message.content.lower().startswith("!evalbot res event"):
        if message.author.id == message.channel.guild.owner_id:
            response = await exportResultCSV(message)
            if response["success"]:
                owner = message.author
                await owner.send(file=response["message1"])
                await owner.send(file=response["message2"])
                embed = nextcord.Embed(title="CSV FILE GENERATED", description="Files have been sent to your DM", color=0x34eb71, timestamp = message.created_at)
                await message.channel.send(embed=embed)
            else:
                embed = nextcord.Embed(title="Something went wrong", description=response["message"], color=0xe60000, timestamp = message.created_at)
                await message.channel.send(embed=embed)
        else:
            embed = nextcord.Embed(title="PERMISSION DENIED", description="Sorry, you're not authorized to perform this command", color=0xcc0000, timestamp = message.created_at) 
            await message.channel.send(embed=embed)
    
    # Update tokens 
    elif message.content.lower().startswith("!evalbot update token"):
        if message.author.id == message.channel.guild.owner_id:
            response = await updateToken(message)
            if response["success"]:
                if len(response["updated"]):
                    await message.channel.send(f"**Following users tokens have been updated**")
                    for userid in response["updated"]:
                        await message.channel.send(f"<@{userid}>")

                if len(response["failed"]):
                    await message.channel.send(f"\n\n**Following users tokens can't be updated**")
                    for userid in response["failed"]:
                        await message.channel.send(f"<@{userid}>")

            else:
                embed = nextcord.Embed(title="TOKENS UPDATION FAILED", description=response["message"], color=0xe60000, timestamp = message.created_at)
                await message.channel.send(embed=embed)

        else:
            embed = nextcord.Embed(title="PERMISSION DENIED", description="Sorry, you're not authorized to perform this command", color=0xcc0000, timestamp = message.created_at) 
            await message.channel.send(embed=embed)


    # Checking the desired Format
    elif message.content.lower().startswith("!evalbot"):
        response = await fomatting_check(message)
        if response["success"]:
            response = f'**{message.author.display_name.upper()}**, {response["message"]}'
            embed = nextcord.Embed(title="CORRECT FORMAT", description=response, color=0x4dff4d, timestamp = message.created_at)
        else:
            embed = nextcord.Embed(title="INCORRECT FORMAT", description=response["message"], color=0xe60000, timestamp = message.created_at)     
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
                embed = nextcord.Embed(title="EVENT ADDED!", description=response["message"], color=0x006600, timestamp = after.created_at)
            else:
                embed = nextcord.Embed(title="Failed to add event", description=response["message"], color=0xcc0000, timestamp = after.created_at) 
            await after.channel.send(embed=embed)
        else:
            embed = nextcord.Embed(title="PERMISSION DENIED", description="Sorry, you're not authorized to perform this command", color=0xcc0000, timestamp = after.created_at) 
            await after.channel.send(embed=embed)

    # Delete event from database
    elif after.content.lower().startswith("!evalbot delete event"):
        if after.author.id == after.channel.guild.owner_id:
            response = await delete_event(after)
            if response["success"]:
                embed = nextcord.Embed(title="EVENT DELETED", description=response["message"], color=0x34eb71, timestamp = after.created_at)   
            else:
                embed = nextcord.Embed(title="Something went wrong", description=response["message"], color=0xe60000, timestamp = after.created_at)
            await after.channel.send(embed=embed)
        else:
            embed = nextcord.Embed(title="PERMISSION DENIED", description="Sorry, you're not authorized to perform this command", color=0xcc0000, timestamp = after.created_at) 
            await after.channel.send(embed=embed)

    # Export Eligible Participants' list in csv format
    elif after.content.lower().startswith("!evalbot res event"):
        if after.author.id == after.channel.guild.owner_id:
            response = await exportResultCSV(after)
            if response["success"]:
                owner = after.author
                await owner.send(file=response["message"])
                embed = nextcord.Embed(title="CSV FILE GENERATED", description="File has been sent to your DM", color=0x34eb71, timestamp = after.created_at)
                await after.channel.send(embed=embed)
            else:
                embed = nextcord.Embed(title="Something went wrong", description=response["message"], color=0xe60000, timestamp = after.created_at)
                await after.channel.send(embed=embed)
        else:
            embed = nextcord.Embed(title="PERMISSION DENIED", description="Sorry, you're not authorized to perform this command", color=0xcc0000, timestamp = after.created_at) 
            await after.channel.send(embed=embed)

    # Update tokens
    elif after.content.lower().startswith("!evalbot update token"):
        if after.author.id == after.channel.guild.owner_id:
            response = await updateToken(after)
            if response["success"]:
                if len(response["updated"]):
                    await after.channel.send(f"**Following users tokens have been updated**")
                    for userid in response["updated"]:
                        await after.channel.send(f"<@{userid}>")
                        if len(response["failed"]):
                            await after.channel.send(f"\n\n**Following users tokens can't be updated**")
                            for userid in response["failed"]:
                                await after.channel.send(f"<@{userid}>")
            else:
                embed = nextcord.Embed(title="TOKENS UPDATION FAILED", description=response["message"], color=0xe60000, timestamp = after.created_at)
                await after.channel.send(embed=embed)

        else:
            embed = nextcord.Embed(title="PERMISSION DENIED", description="Sorry, you're not authorized to perform this command", color=0xcc0000, timestamp = after.created_at) 
            await after.channel.send(embed=embed)
                
    #fomatting check
    elif after.content.lower().startswith("!evalbot"):
        response = await fomatting_check(after)
        if response["success"]:
            response = f'**{after.author.name.upper()}**, {response["message"]}'
            embed = nextcord.Embed(title="CORRECT FORMAT", description=response, color=0x4dff4d, timestamp = after.created_at)
        else:
            embed = nextcord.Embed(title="INCORRECT FORMAT", description=response["message"], color=0xe60000, timestamp = after.created_at)     
        await after.channel.send(embed=embed)

# Slash commands
testserverid = 1081631255700963409
@client.slash_command(name="help",description="List of all commands",guild_ids=[testserverid])
async def help (interaction: Interaction):
    embed = nextcord.Embed(title="**All Commands**",color=0x03f4fc)

    embed.add_field(name="🤖 DAILY POST FORMAT CHECK", value=await format_check_command(), inline=False)
    embed.add_field(name="🤖 ADD EVENT [OWNER ONLY]", value=await add_event_command(), inline=False)
    embed.add_field(name="🤖 DELETE EVENT [OWNER ONLY]", value=await delete_event_command(), inline=False)
    embed.add_field(name="🤖 RESULT OF EVENT [OWNER ONLY]", value=await result_event_command(), inline=False)
    embed.add_field(name="🤖 TOKEN UPDATE [OWNER ONLY]", value=await update_token_event_command(), inline=False)

    await interaction.response.send_message(embed=embed)



# it tells the bot to run
client.run(discord_api_key)

from Utils.connection import *
from Utils.libraries import *

async def findDayNumber(channel_name):
    # connect with mongodb
    cluster = await get_connection()

    db = cluster["Events"]
    collection = db[channel_name]
    #event info has been stored in the document with _id = 0
    filter = {"_id": 0}
    document = collection.find_one(filter)
    if document:
        start_date = (document.get("start_date")).split()
        if start_date:
            year = int(start_date[0].split("-")[2])
            month = int(start_date[0].split("-")[1])
            day = int(start_date[0].split("-")[0])

            hour = int(start_date[1].split(":")[0])
            minute = int(start_date[1].split(":")[1])
            second = int(start_date[1].split(":")[2])
            
            start_time = datetime(year, month, day) + timedelta(hours = hour, minutes = minute, seconds = second)
            current_time = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")
            # convert String type to datetime object
            current_time = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
            day_no = (current_time - start_time).days + 1
            return day_no
        else:
            print("Start Date field not found in the document.")
    else:
        print("Document not found in the collection.")

async def update_dayNumber(author_name, author_id, message, channel_name, current_day):
    # connect with mongodb
    cluster = await get_connection()

    db = cluster["Events"]
    collection = db[channel_name]
    # print(collection)
    all_records = collection.find()
    for record in all_records:
        if author_name in record.values() or author_id in record.values():
            # print(record)
            prev_day = record.get("day")
            # out of challenge
            if(current_day - prev_day > 1):
                return {"message": f"You didn't post on DAY **{prev_day + 1}**\n**YOU ARE OUT OF CHALLENGE**", "success": False}
            elif(current_day == prev_day):
                return {"message": f"You have already posted taday's (DAY - {current_day}) TASK", "success": True}
            else:
                post_day_no = f"day {current_day}"
                post_link_discord = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"
                
                # Define the update object to set "day" and push a new item to "post_link" array
                update = {
                    "$set": {"day": current_day},
                    "$push": {"post_link": {post_day_no: post_link_discord}}
                }
                collection.update_one(record, update)
                return {"message": f"YOU HAVE SUCCESSFULLY COMPLETED **DAY {current_day}** TASK :partying_face:", "success": True}
    return {"message": f"{author_name}, you have not registered for {channel_name}", "success": False}

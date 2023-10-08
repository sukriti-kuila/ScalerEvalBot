import re
from datetime import datetime, timedelta
import pytz
import csv
import pandas as pd
from connection import *

async def fomatting_check(message):
    message_str = str(message.content).split("\n")
    print(message_str)
    if(len(message_str) < 2):
        return {"message": "Follow the format carefully", "success": False}
    else:
        channel_name = str(message.channel)
        first_line = message_str[0].split()
        bot_command = first_line[0].lower()
        completion_command = first_line[1 : len(first_line)]
        Second_line = message_str[1]
        post_pattern = r'^social media link : https://(www.linkedin.com|x.com|twitter.com)/+'

        day_no = await findDayNumber(channel_name)
        print("day_no ", day_no)
        if day_no==None:
            return {"message": "The Event is not registered yet!\n Contact with moderators", "success": False}
        user_day_no = int(completion_command[1][3:len(completion_command[1])])

        if message.attachments:
            attachment = message.attachments[0]
            filename = attachment.filename.lower()
            if not filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp')):
                return {"message": "Please attach a screenshot of the task\n**Supported formats [jpg,jpeg,png,gif,webp,bmp]**", "success": False}
        else:
            return {"message": "Please attach a screenshot of the task\n**Supported formats [jpg,jpeg,png,gif,webp,bmp]**", "success": False}

        if len(first_line) == 3 and bot_command == "!evalbot" and completion_command[0].lower() == "completed" and completion_command[1][0:3].lower() == "day" and  user_day_no== day_no:
            if re.match(post_pattern, Second_line.lower()):
                # update day number in the database
                response = await update_dayNumber(str(message.author), message.author.id, channel_name, day_no)
                return response
            else:
                return {"message": "\nYou have made a formatting mistake in line 2\nEdit the previous message or send a new message using the following format for line2\n\nsocial media link : <linkedin/twitter post> (Case-Insensitive)\n", "success": False}
        else:
            if user_day_no != day_no:
                return {"message": "Looks like the day number is wrong\n**Edit the previous message or send a new message to rectify the mistake**", "success": False}
            return {"message": "\nYou have made a formatting mistake in line 1\nEdit the previous message or send a new message using the following format for line1\n\n!Evalbot completed day<day no> (Case-Insensitive)\n", "success": False}


async def eventData(message):
        message_str = str(message.content).split("\n")
        if len(message_str)==4:
            event_name = message_str[1]
            start_date = message_str[2]
            event_duration = message_str[3]
            print(start_date)
            
            if not is_valid_date(start_date):
                return {"message": "The date format is wrong follow this format\n DD-MM-YYYY H:M:S", "success": False}
            if not is_valid_duration(event_duration):
                return {"message": "Please Enter a numeric value for duration", "success": False}
            print (f"name {event_name} start {start_date} duration {event_duration}")
            
            if message.attachments:
                attachment = message.attachments[0]
                if attachment.filename.endswith('.csv'):
                    # Download the CSV file
                    filename = event_name+""+".csv"
                    await attachment.save(filename)
                    await db_connection(event_name, event_duration, start_date, filename)
                    return {"message": "Participants entries have been successfully recorded", "success": True}
                else:
                    return {"message": "Please attach a CSV file", "success": False}
            else:
                return {"message": "Please attach a CSV file", "success": False}
        else:
            return {"message": "Please attach a CSV file", "success": False}
        

async def delete_event(message):
    message_str = str(message.content).split("\n")
    if len(message_str) == 2:
        event_name = message_str[1]

        cluster = await get_connection()
        db = cluster["Events"]
        if event_name in db.list_collection_names():
            db.drop_collection(event_name)
            return f"Event - {event_name} successfully deleted"
        return f"{event_name} does not exit in database"
        
        
async def db_connection(event_name, event_duration, start_date, filename):
    # connect with mongodb
    cluster = await get_connection()
    
    db = cluster["Events"]
    collection = db[event_name]
    event_details = {"_id":0,"event_name":event_name,"start_date":start_date,"event_duration":event_duration}
    collection.insert_one(event_details)

    # using pandas
    df = pd.read_csv(filename)  # table format
    df["day"] = int(0)
    # convert to dictionary
    records_dictionary = df.to_dict(orient='records')
    collection.insert_many(records_dictionary)


def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%d-%m-%Y %H:%M:%S")
        return True
    except ValueError:
        print("Error")
        return False
    
def is_valid_duration(duration):
    try:
        int(duration)
        return True
    except ValueError:
        print("Error")
        return False    
    

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
            print(f"Stat Date: {start_date}")
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


async def update_dayNumber(author_name, author_id, channel_name, current_day):
    # connect with mongodb
    cluster = await get_connection()

    db = cluster["Events"]
    collection = db[channel_name]
    
    print(collection)
    all_records = collection.find()
    for record in all_records:
        if author_name in record.values() or author_id in record.values():
            print(record)
            prev_day = record.get("day")
            # out of challenge
            if(current_day - prev_day > 1):
                return {"message": f"You have not posted on DAY {prev_day + 1}\nYou are out of challenge", "success": False}
            else:
                collection.update_one(record, {"$set":{"day":current_day}})
                return {"message": f"YOU HAVE SUCCESSFULLY COMPLETED DAY {current_day} TASK :partying_face:", "success": True}
    return {"message": f"{author_name}, you have not registered for {channel_name}", "success": False}




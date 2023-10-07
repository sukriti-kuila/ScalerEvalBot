import re
from datetime import datetime, timedelta
import pytz
import csv
from connection import *

async def fomatting_check(message):
    message_str = str(message.content).split("\n")
    print(message_str)
    if(len(message_str) < 2):
        return "Follow the format carefully"
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
            return "The Event is not registered yet!\n Contact with moderators"
        user_day_no = int(completion_command[1][3:len(completion_command[1])])

        if message.attachments:
            attachment = message.attachments[0]
            filename = attachment.filename.lower()
            if not filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp')):
                return "Please attach a screenshot of the task\nSupported formats [jpg,jpeg,png,gif,webp,bmp]"
        else:
            return "Please attach a screenshot of the task\nSupported formats [jpg,jpeg,png,gif,webp,bmp]"

        if len(first_line) == 3 and bot_command == "!evalbot" and completion_command[0].lower() == "completed" and completion_command[1][0:3].lower() == "day" and  user_day_no== day_no:
            if re.match(post_pattern, Second_line.lower()):
                # update day number in the database
                response = await update_dayNumber(message.author.name, channel_name, day_no)
                return response
            else:
                return "------------------\nYou have made a formatting mistake in line 2\nEdit the previous message or send a new message using the following format for line2\n\nsocial media link : <linkedin/twitter post> (Case-Insensitive)\n------------------"
        else:
            if user_day_no != day_no:
                return "------------------\nYou have made a formatting mistake in line 1\nEither day number is wrong OR you've send the message in a wrong channel\nEdit the previous message or send a new message to rectify the mistake\n------------------"
            return "------------------\nYou have made a formatting mistake in line 1\nEdit the previous message or send a new message using the following format for line1\n\n!Evalbot completed day<day no> (Case-Insensitive)\n------------------"


async def eventData(message):
        message_str = str(message.content).split("\n")
        if len(message_str)==4:
            event_name = message_str[1]
            start_date = message_str[2]
            event_duration = message_str[3]
            print(start_date)
            
            if not is_valid_date(start_date):
                return "The date format is wrong follow this format\n DD-MM-YYYY"
            if not is_valid_duration(event_duration):
                return "Please Enter a numeric value for duration"
            print (f"name {event_name} start {start_date} duration {event_duration}")
            
            if message.attachments:
                attachment = message.attachments[0]
                if attachment.filename.endswith('.csv'):
                    # Download the CSV file
                    filename = event_name+""+".csv"
                    await attachment.save(filename)
                    await db_connection(event_name, event_duration, start_date, filename)
                    return "Participant entries have been successfully recorded"
                else:
                    return "Please attach a CSV file"
            else:
                return "Please attach a CSV file"
        else:
            return "Please follow the proper format to register data"
        
        
async def db_connection(event_name, event_duration, start_date, filename):
    # connect with mongodb
    cluster = await get_connection()
    
    db = cluster["Events"]
    collection = db[event_name]
    event_details = {"_id":0,"event_name":event_name,"start_date":start_date,"event_duration":event_duration}
    collection.insert_one(event_details)

    with open(filename, newline='') as f:
        # extracting first row(attributes)
        reader = csv.reader(f)
        header = next(reader)
        print(header)

        # inserting participant's details
        csvFile = open(filename, 'r')
        reader = csv.DictReader(csvFile)
        for each in reader:
            row = {}
            for field in header:
                if field in each:
                    row[field] = each[field]
                else:
                    row[field] = None
            row["day"] = int(0)
            collection.insert_one(row)


def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%d-%m-%Y')
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
        start_date = document.get("start_date")
        if start_date:
            print(f"Stat Date: {start_date}")
            year = int(start_date.split("-")[2])
            month = int(start_date.split("-")[1])
            day = int(start_date.split("-")[0])
            start_time = datetime(year, month, day) + timedelta(hours = 11, minutes = 00, seconds = 00)
            current_time = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")
            # convert String type to datetime object
            current_time = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
            day_no = (current_time - start_time).days + 1
            return day_no
        else:
            print("Start Date field not found in the document.")
    else:
        print("Document not found in the collection.")


async def update_dayNumber(author_name, channel_name, current_day):
    # connect with mongodb
    cluster = await get_connection()

    db = cluster["Events"]
    collection = db[channel_name]
    
    all_records = collection.find()
    for record in all_records:
        if author_name in record.values():
            prev_day = record.get("day")
            # out of challenge
            if(current_day - prev_day > 1):
                response = f"You have not posted on DAY {prev_day + 1}\nYou are out of challenge"
                return response
            else:
                collection.update_one(record, {"$set":{"day":current_day}})
                return "YOU HAVE SUCCESSFULLY COMPLETED TODAY'S TASK :partying_face: "



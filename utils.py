import re
from datetime import datetime, timedelta
import pytz

async def fomatting_check(message):
    message_str = str(message.content).split("\n")
    print(message_str)
    if(len(message_str) < 2):
        return "Follow the format carefully"
    else:
        first_line = message_str[0].split()
        bot_command = first_line[0].lower()
        completion_command = first_line[1 : len(first_line)]

        Second_line = message_str[1]
        post_pattern = r'^social media link : https://(www.linkedin.com|x.com|twitter.com)/+'


        start_time = datetime(2023, 10, 1) + timedelta(hours = 11, minutes = 00, seconds = 00)
        challenge_days = 30
        current_time = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")
        # convert String type to datetime object
        current_time = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")

        day_no = (current_time - start_time).days + 1

        user_day_no = int(completion_command[1][3:len(completion_command[1])])
        if message.attachments:
            attachment = message.attachments[0]
            filename = attachment.filename.lower()
            if not filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp')):
                return "Please attach a screenshot of the task\nSupported formats [jpg,jpeg,png,gif,webp,bmp]"
        else:
            return "Please attach a screenshot of the task\nSupported formats [jpg,jpeg,png,gif,webp,bmp]"


        if len(first_line) == 3 and bot_command == "!evalbot" and completion_command[0].lower() == "completed" and completion_command[1][0:3].lower() == "day" and (0 < int(completion_command[1][3:len(completion_command[1])]) <= challenge_days) and  user_day_no== day_no:
            if re.match(post_pattern, Second_line.lower()):
                return "YOU HAVE SUCCESSFULLY COMPLETED TODAY'S TASK :partying_face: "
            else:
                return "------------------\nYou have made a formatting mistake in line 2\nEdit the previous message or send a new message using the following format for line2\n\nsocial media link : <linkedin/twitter post> (Case-Insensitive)\n------------------"

        else:
            if user_day_no != day_no:
                return "------------------\nYou have made a formatting mistake in line 1\nLooks like the day number is wrong\nEdit the previous message or send a new message to rectify the mistake\n------------------"
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
                    return "Participant entries have been successfully recorded"
                else:
                    return "Please attach a CSV file"
            else:
                return "Please attach a CSV file"
        else:
            return "Please follow the proper format to register data"

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

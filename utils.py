import re
from datetime import datetime, timedelta
import pytz

async def fomatting_check(message_str):
    if(len(message_str) < 2):
        return "Follow the format carefully"
    else:
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

        user_day_no = int(completion_command[1][3:len(completion_command[1])])

        if len(first_line) == 3 and bot_command == "!bot" and completion_command[0].lower() == "completed" and completion_command[1][0:3].lower() == "day" and (0 < int(completion_command[1][3:len(completion_command[1])]) <= challenge_days) and  user_day_no== day_no:
            if re.match(post_pattern, Second_line.lower()):
                return "YOU HAVE SUCCESSFULLY COMPLETED TODAY'S TASK :partying_face: "
            else:
                return "------------------\nYou have made a formatting mistake in line 2\nEdit the previous message or send a new message using the following format for line2\nsocial media link : <linkedin/twitter post> (Case-Insensitive)\n------------------"

        else:
            if user_day_no != day_no:
                return "------------------\nYou have made a formatting mistake in line 1\nLooks like the day number is wrong\nEdit the previous message or send a new message to rectify the mistake\n------------------"
            return "------------------\nYou have made a formatting mistake in line 1\nEdit the previous message or send a new message using the following format for line1\n!bot completed day<day no> (Case-Insensitive)\n------------------"

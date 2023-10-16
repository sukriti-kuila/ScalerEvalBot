from Utils.connection import *
from Utils.libraries import *
from Utils.dayNumber import *

async def fomatting_check(message):
    message_str = str(message.content).split("\n")
    print(message_str)
    if(len(message_str) != 2):
        return {"message": "Follow the format carefully", "success": False}
    else:
        channel_name = str(message.channel)
        first_line = message_str[0].split()
        bot_command = first_line[0].lower()
        completion_command = first_line[1 : len(first_line)]
        Second_line = message_str[1]
        post_pattern = r'^social media link\s*:\s*https://(www.linkedin.com|x.com|twitter.com)/+'

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
                response = await update_dayNumber(str(message.author), message.author.id, message, channel_name, day_no)
                return response
            else:
                return {"message": "\nYou have made a formatting mistake in line 2\nEdit the previous message or send a new message using the following format for line2\n\nsocial media link : <linkedin/twitter post> (Case-Insensitive)\n", "success": False}
        else:
            if user_day_no != day_no:
                return {"message": "Looks like the **DAY NUMBER** is wrong\nEdit the previous message or send a new message to rectify the mistake", "success": False}
            return {"message": "\nYou have made a formatting mistake in line 1\nEdit the previous message or send a new message using the following format for line1\n\n!Evalbot completed day<day no> (Case-Insensitive)\n", "success": False}
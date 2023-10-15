from libraries import *
from connection import *

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
                return {"message": "Looks like the **day number** is wrong\nEdit the previous message or send a new message to rectify the mistake", "success": False}
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
                    return {"message": "Please attach a **CSV** file", "success": False}
            else:
                return {"message": "Please attach a **CSV** file", "success": False}
        else:
            return {"message": "Please attach a **CSV** file", "success": False}
        
async def db_connection(event_name, event_duration, start_date, filename):
    event_name = event_name.lower()

    # connect with mongodb
    cluster = await get_connection()
    
    db = cluster["Events"]
    collection = db[event_name]
    event_details = {"_id":0,"event_name":event_name,"start_date":start_date,"event_duration":int(event_duration)}
    collection.insert_one(event_details)

    # using pandas
    df = pd.read_csv(filename)  # table format
    print(df.shape[0])          # no. of rows of df
    df["day"] = int(0)
    df['post_link'] = [[]] * df.shape[0]
    # convert to dictionary
    records_dictionary = df.to_dict(orient='records')
    collection.insert_many(records_dictionary)

async def delete_event(message):
    message_str = str(message.content).split("\n")
    if len(message_str) == 2:
        event_name = message_str[1]

        cluster = await get_connection()
        db = cluster["Events"]
        if event_name in db.list_collection_names():
            db.drop_collection(event_name)
            return {"message":f"Event - {event_name} successfully deleted", "success":True}
        return {"message":f"{event_name} does not exit in database", "success":False}
    else:
        return {"message":"Looks Like you forgot to mention **event name**", "success":False}
    
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


async def update_dayNumber(author_name, author_id, message, channel_name, current_day):
    # connect with mongodb
    cluster = await get_connection()

    db = cluster["Events"]
    collection = db[channel_name]
    print(collection)
    all_records = collection.find()
    for record in all_records:
        if author_name in record.values() or author_id in record.values():
            # print(record)
            prev_day = record.get("day")
            # out of challenge
            if(current_day - prev_day > 1):
                return {"message": f"You have not posted on DAY {prev_day + 1}\nYou are out of challenge", "success": False}
            elif(current_day == prev_day):
                return {"message": f"You have already posted taday's (DAY - {current_day}) TASK", "success": True}
            else:
                print(type(record.get("post_link")))
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


async def exportResultCSV(message):
    cluster = await get_connection()
    db = cluster["Events"]
    
    try:
        message_str = str(message.content).split("\n")
        if len(message_str) == 2:
            event_name = message_str[1]
            collection = db[event_name]

            # Fetch the event_duration from DB
            document = collection.find_one({"_id": 0})
            if document:
                event_duration = document.get("event_duration")
                records = collection.find({"day": event_duration})
            
                # Count the number of records that match the event_duration filter
                record_count = collection.count_documents({"day": event_duration})
            
                if record_count > 0:
                    records = collection.find({"day": event_duration})
                    # Convert records to a list of dictionaries
                    records_list = list(records)

                    df = pd.DataFrame(records_list)

                    columns_to_exclude = ["_id", "day"]
                    df = df.drop(columns=columns_to_exclude)

                    for index, row in df.iterrows():
                        for day_link_dict in row["post_link"]:
                            for day, link in day_link_dict.items():
                                df.at[index, day] = link

                    df = df.drop(columns=["post_link"])

                    csv_filename = f"{event_name}_result.csv"
                    df.to_csv(csv_filename, index=False)
                    file = nextcord.File(csv_filename)
                else:
                    print("No Eligible participant")
                    return {"message": "There is no eligible participant who completed task", "success": False}
        
                cluster.close()
                return {"message": file, "success": True}
            else:
               return {"message": f"There is no such event as **\"{event_name}\"** in the database", "success": False} 
        else:
            return {"message": "Looks Like you forgot to mention **event name**", "success": False}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"message": "An error occurred", "success": False}

async def updateToken(message):
    message_str = str(message.content).split("\n")
    if len(message_str) == 2:
        amount =  int(message_str[1])
        guild_id = message.guild.id

        if message.attachments:
            attachment = message.attachments[0]
            if attachment.filename.endswith('.csv'):
                filename = attachment.filename
                await attachment.save(filename)
                response = await tatsuAPICall(guild_id, amount, filename)
                return response
            else:
                return {"message": "Please attach a **CSV** file", "success": False}
        else:
            return {"message": "Please attach a **CSV** file", "success": False}
    else:
        return {"message":"You forgot to mention **TOKEN_AMONUT**", "success": False}

async def tatsuAPICall(guild_id, amount, csv_filename):
    # check whether the event exists in the DB
    cluster = await get_connection()
    db = cluster["Events"]
    updated_user = []
    failed_user = []
    try:
        TATSU_API_TOKEN = config('TATSU_API_TOKEN')
        payload = {
            'action': 0,
            'amount': amount
        }
        headers = {'Authorization': TATSU_API_TOKEN}

        df = pd.read_csv(csv_filename)
        columns = [col for col in df.columns if 'discord id' in col.lower()]
        # Specify that the 'discord id' columns should be treated as strings to maintain precision
        column_dtype = {col: str for col in columns}

        df = pd.read_csv(csv_filename, dtype=column_dtype)

        columns = [col for col in df.columns if 'discord id' in col.lower()]
        df_columns = df[columns]

        for index, row in df_columns.iterrows():
            for col in columns:
                value = row[col]
                if not pd.isnull(value):
                    print(value)
                    endpoint_url = f'https://api.tatsu.gg/v1/guilds/{guild_id}/members/{value}/points'
                    response = requests.patch(endpoint_url, json=payload, headers=headers)

                    if response.status_code == 200:
                        modified_points_data = response.json()
                        updated_user.append(str(modified_points_data["user_id"]))
                        print(f'Successfully modified points: {modified_points_data}')

                    else:
                        failed_user.append(str(value))
                        print(f'Failed to modify points. Status code: {response.status_code}')
                        # print(response.text)

    except Exception as e:
        print(str(e))
        return {"message": "Something went wrong", "success": False}
    return {"message": "Tokens have been updated of eligible participants", "updated": updated_user, "failed": failed_user, "success": True}

# Slash commands
async def add_event_command():
    return (
            "```!evalbot new event\n"
            "<event name>\n"
            "<event start date[DD-MM-YYYY] [SPACE] start time[HH:MM:SS]>\n"
            "<event duration>\n"
            "<CSV File>\n```")

async def delete_event_command():
    return (
            "```!evalbot delete event\n"
            "<event name>```\n")        

async def result_event_command():
    return ("```!evalbot res event\n"
            "<event name>```\n"
           )

async def format_check_command():
    return ("```!evalbot Completed Day<day number>\n"
            "Social Media Link : <X (Twitter) or Linkedin Post Link>\n"
            "<Screenshot of the task>```\n"
            )

async def update_token_event_command():
    return ("```!evalbot update token\n"
            "<token amount>\n"
            "<CSV File>```\n"
            "[Click Here To Discover More](https://github.com/sukriti-kuila/ScalerEvalBot)\n"
            )

async def set_reminder():
    cluster = await get_connection()
    db = cluster["Events"]
    all_events = db.list_collection_names()
    print(all_events)

    reminder_user = []
    for event in all_events:
        collection = db[event]
        time_left = await get_time_left(event)
        print("time left", time_left)
        if time_left:
            day_no = await findDayNumber(event)
            filter = {"day": day_no - 1}
            document = collection.find(filter, {"_id":0, "day": 0, "post_link":0})

            for user in document:
                print("user is", user)
                for key in user.keys():
                    if "discord id" in key.lower():
                        if not pd.isnull(user.get(key)):
                            user_id = int(user.get(key))
                            check = True
                            for ele in reminder_user:
                                if user_id in ele.keys():
                                    ele[user_id].append(event)
                                    check = False
                            if(check == True):
                                reminder_user.append({user_id:[event]})
    return reminder_user           


async def get_time_left(channel_name):
    cluster = await get_connection()
    db = cluster["Events"]
    collection = db[channel_name]

    filter = {"_id": 0}
    document = collection.find_one(filter)
    start_date = (document.get("start_date")).split()
    if start_date:
        hour = int(start_date[1].split(":")[0])
        minute = int(start_date[1].split(":")[1])
        second = int(start_date[1].split(":")[2])
            
        start_time = timedelta(hours = hour, minutes = minute, seconds = second)

        current_time = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")
        hour = int(current_time.split(' ')[1].split(":")[0])
        minute = int(current_time.split(' ')[1].split(":")[1])
        second = int(current_time.split(' ')[1].split(":")[2])
        # convert String type to datetime object
        time_part = timedelta(hours = hour, minutes = minute, seconds = second)


        time00 = timedelta(hours = 0, minutes = 0, seconds = 0)
        time01 = timedelta(hours = 1, minutes = 0, seconds = 0)
        time_left = 0
        if(time00 <= start_time <= time01):
            time_left = (start_time + timedelta(hours = 24, minutes = 0, seconds = 0)) - time_part
        else:
            time_left = (start_time - time_part)
        print("time left ----------", time_left)
        time_left = int(time_left.total_seconds())
        print(time_left)
        if 0 <= time_left <= 3600:
            return True

        return False


        
        











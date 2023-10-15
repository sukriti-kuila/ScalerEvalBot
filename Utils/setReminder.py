from Utils.connection import *
from Utils.libraries import *

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
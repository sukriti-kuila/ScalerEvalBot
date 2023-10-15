from Utils.connection import *
from Utils.libraries import *


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
    
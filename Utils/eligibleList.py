from Utils.connection import *
from Utils.libraries import *

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
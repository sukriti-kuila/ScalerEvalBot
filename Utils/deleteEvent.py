from Utils.connection import *
from Utils.libraries import *

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
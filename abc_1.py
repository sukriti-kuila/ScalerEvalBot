import os
from dotenv import load_dotenv, find_dotenv
import json
from apikeys import *
from pymongo import MongoClient
import csv
# import pandas as pd
# from pymongo.collection import Collection
# from pymongo.database import Database


load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")
connection_string = f""
try:
    client = MongoClient(connection_string)
except Exception:
    print("error ", Exception)

# get all database list
print(client.list_database_names())


db = client["Scaler"]
event_name = "September-challenge"
collection = db[event_name]


channel_name = "abcd"
start_date = 21-2-2023
duration = 30
event_details = {"_id":1,
                 "channel_name":channel_name,
                 "start_date":start_date,
                 "duration":duration}
collection.insert_one(event_details)


with open('sheet.csv', newline='') as f:
  reader = csv.reader(f)
  header = next(reader)

print(header)
csvFile = open('sheet.csv', 'r')
reader = csv.DictReader(csvFile)

for each in reader:
    row = {}
    for field in header:
        if field in each:
            row[field] = each[field]
        else:
            # Handle missing columns here (e.g., provide a default value)
            row[field] = None
    print(row)
    collection.insert_one(row)



# set1 = collection.find_one({"discord id": "abhunia."})
# print(set1)
# for ele in set1:
#     print(ele)








# post = {"_id":1, "name":"an"}
# collection.insert_one(post)
from pymongo import MongoClient
from decouple import config

async def get_connection():
    try:
        DB_URI_STRING = config('DB_URI_STRING')
        cluster = MongoClient(DB_URI_STRING)
        return cluster
    except Exception:
        print("error ", Exception)

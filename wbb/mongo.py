import asyncio
import sys

from motor import motor_asyncio
from wbb import MONGO_DB_URI 
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError


MONGO_PORT = "27017"
MONGO_DB_URI = " mongodb+srv://atom:pyro@cluster0.coknb1u.mongodb.net/?retryWrites=true&w=majority"
MONGO_DB = "atom-pyro"


client = MongoClient()
client = MongoClient(MONGO_DB_URI, MONGO_PORT)[MONGO_DB]
motor = motor_asyncio.AsyncIOMotorClient(MONGO_DB_URI, MONGO_PORT)
db = motor[MONGO_DB]
db = client["atom-pyro"]
try:
    asyncio.get_event_loop().run_until_complete(motor.server_info())
except ServerSelectionTimeoutError:
    sys.exit(log.critical("Can't connect to mongodb! Exiting..."))
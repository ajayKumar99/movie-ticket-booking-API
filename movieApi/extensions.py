import pymongo
from os import environ

db = pymongo.MongoClient(environ.get('MONGO_URI'))
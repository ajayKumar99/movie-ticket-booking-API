import pymongo
from os import environ

db = pymongo.MongoClient('localhost', 27017)
# test_db = pymongo.MongoClient(environ.get('TEST_MONGO_URI'))
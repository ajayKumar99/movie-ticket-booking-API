import pymongo
from os import environ

db = pymongo.MongoClient(environ.get('MONGO_URI'))
test_db = pymongo.MongoClient(environ.get('TEST_MONGO_URI'))
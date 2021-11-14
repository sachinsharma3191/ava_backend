import configparser

from pymongo import MongoClient

config = configparser.ConfigParser()
config.read("app.ini")

host = config.get('database', 'MONGO_DB_HOST')
username = config.get('database', 'MONGO_DB_USER')
password = config.get('database', 'MONGO_DB_PASSWORD')

url = "mongodb+srv://" + username + ":" + password + "@" + host

client = MongoClient(url)
db = client["conversations"]
conversation = db.conversation


def get_conversation_collection():
    return conversation


def get_starred_collection():
    return db.starred

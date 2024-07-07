from pymongo import MongoClient
from dotenv import load_dotenv
from os import getenv

load_dotenv()
connection_string = getenv("DATABASE_CONN_STRING")
connection = MongoClient(connection_string)
user_collection = connection.UsersDB.users


# USER DATABASE
class Users:
    def register_user(self,document: dict, app:str):
        try:
            doc = { "application":app, "username":document["username"], "password":document["password"] }
            user_collection.insert_one(doc)
            return True
        
        except Exception as error:
            return error
        
    def find_user(self, username: str):
        try:
            user = user_collection.find_one({"username":username})
            return user
        
        except Exception as error:
            return error

    def is_user(self, username:str):
        try:
            isuser = user_collection.find_one({ "username":username })
            if isuser:
                return True
            else:
                return False
            
        except Exception as error:
            return error

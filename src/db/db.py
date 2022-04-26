import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_DB = os.getenv("MONGO_DB")

mongo_conn_uri = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@cluster0.tlmrq.mongodb.net/{MONGO_DB}?retryWrites=true&w=majority"

client = MongoClient(mongo_conn_uri)
db = client.get_database()

users_collection = db['users']

user = {
    "discord_id": "123456789",
    "name": "John",
}

user_id = users_collection.insert_one(user).inserted_id
print(user_id)


class DB:
    def __init__(self):
        self.client = MongoClient(mongo_conn_uri)
        self.db = self.client.get_database()

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def get_user(self, discord_id):
        return self.get_collection('users').find_one({"discord_id": discord_id})
    
    def get_user_by_id(self, user_id):
        return self.get_collection('users').find_one({"_id": user_id})

    def get_all_users(self):
        return self.get_collection('users').find()

    def add_user(self, user):
        return self.get_collection('users').insert_one(user).inserted_id

    def update_user(self, user):
        return self.get_collection('users').update_one({"_id": user["_id"]}, {"$set": user})

    def delete_user(self, user_id):
        return self.get_collection('users').delete_one({"_id": user_id})

    def get_admins_id(self):
        return self.get_collection('admins').find().distinct("discord_id")
    
    def create_group(self, group):
        admins_id = self.get_collection('admins').find().distinct('discord_id')
        print(admins_id)
        if not group["creator_id"] in admins_id and self.get_collection('groups').find_one({"creator_id": group["creator_id"]}):
            raise Exception(f"Usurário <@{group['creator_id']}> já possui um grupo")
        if self.get_collection('groups').find_one({"name": group["name"]}):
            raise Exception(f"Grupo **{group['name']}** já existe")
        self.get_collection('groups').insert_one(group)

    def get_group(self, group_id):
        return self.get_collection('groups').find_one({"_id": group_id})

    def get_all_groups(self):
        return self.get_collection('groups').find()

    def update_group(self, group):
        return self.get_collection('groups').update_one({"_id": group["_id"]}, {"$set": group})

    def delete_group(self, group_id):
        return self.get_collection('groups').delete_one({"_id": group_id})

    def add_user_to_group(self, user_id, group_id):
        return self.get_collection('groups').update_one({"_id": group_id}, {"$push": {"users": user_id}})
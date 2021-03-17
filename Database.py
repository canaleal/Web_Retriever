from pymongo import MongoClient
from Encrypt import *


class Database:
    def __init__(self):
        cluster = MongoClient(
            "mongodb+srv://canaleal:Partyboy117$@cluster0-ok7xr.mongodb.net/<dbname>?retryWrites=true&w=majority")
        db = cluster["reddit"]
        self.collection = db["reddit"]

        self.name = ''
        self.password = ''
        self.id = ''

    def get_id(self):
        return self.id

    def check_login(self, name, password):
        return self.collection.find_one({"name": name, "pass": password})

    def sign_up(self, name, password):
        if self.check_login(name, password) is None:
            num = self.collection.count()
            self.collection.insert_one({"_id": num, "name": name, "pass": encrypt_pass(password)})
        else:
            print("Couldn't create account.")

    def login(self, name, password):
        if self.check_login(name, encrypt_pass(password)) is not None:
            self.name = name
            self.password = encrypt_pass(password)
            self.id = self.collection.find_one({"name": self.name, "pass": self.password})["_id"]
            return True
        else:
            print("Doesn't Exist")
            return False

    def find_item(self, tag):
        return self.collection.find_one({"_id": self.id})[tag]

    def print_item(self, tag):
        try:
            print('{0} : {1}'.format(tag, self.find_item(tag)))
        except Exception as e:
            print("")

    def update_recent(self, recent):
        self.collection.update_many({"_id": self.id}, {"$set": {"recent": recent}})

    def update_category(self, category):
        self.collection.update_many({"_id": self.id}, {"$set": {"category": category}})

    def update_password(self, old_password, new_password):
        if self.password == encrypt_pass(old_password):
            self.collection.update_one({"_id": self.id}, {"$set": {"pass": encrypt_pass(new_password)}})
            print("Updated Password.")
        else:
            print("Wrong Password.")

    def delete_account(self, password):
        if self.password == encrypt_pass(password):
            self.collection.remove({"_id": self.id})
            print("Deleted Account.")
        else:
            print("Wrong Password.")

from pymongo import MongoClient
client = MongoClient('mongodb+srv://Hochan:<2992>@cluster0.tukuuwi.mongodb.net/?retryWrites=true&w=majority')
db = client.dbhochan

doc = {
    'name':'ghcks',
    'age':24
}
db.users.insert_one(doc)
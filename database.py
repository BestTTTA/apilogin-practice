from pymongo import MongoClient

# Connect to your MongoDB cluster:
client = MongoClient("mongodb+srv://promtgov:promtgov@cluster0.b1xky3c.mongodb.net/")

# Get the database:
db = client.pratice

# Access your collection:
users_collection = db.user

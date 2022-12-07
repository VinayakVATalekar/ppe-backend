from pymongo import MongoClient
client = MongoClient()
db = client['my_db']
db["camera"].drop()
db["alert"].drop()




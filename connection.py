import
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["MAYLA"]
mycol = mydb["users"]
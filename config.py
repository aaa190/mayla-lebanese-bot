import os


def checknewuser(id):
    import pymongo
    # myclient = pymongo.MongoClient('localhost:27017', username='root', password='root2022')
    myclient = pymongo.MongoClient(os.getenv("CONNECTION_STRING", "mongodb://aDXFitC:aDFit&gr3exiHXDA31vb@localhost:27017/"))
    mydb = myclient["MAYLA"]
    usercol = mydb["users"]
    res=usercol.find_one({"_id": id})
    myclient.close()
    return res==None

def saveuser(id,fullname,username,number):
    import pymongo,datetime
    # myclient = pymongo.MongoClient('localhost:27017', username='root', password='root2022')
    myclient = pymongo.MongoClient(os.getenv("CONNECTION_STRING", "mongodb://aDXFitC:aDFit&gr3exiHXDA31vb@localhost:27017/"))

    mydb = myclient["MAYLA"]
    usercol = mydb["users"]

    usercol.insert_one({"_id":id,"name":fullname,"username":username,"number":number,"stage":0,"nextmsg":datetime.datetime.now(),"startdate":datetime.datetime.now(),"enddate":datetime.datetime.utcfromtimestamp(0)})
    myclient.close()

def getstage(id):
    import pymongo
    # myclient = pymongo.MongoClient('localhost:27017', username='root', password='root2022')
    myclient = pymongo.MongoClient(os.getenv("CONNECTION_STRING", "mongodb://aDXFitC:aDFit&gr3exiHXDA31vb@localhost:27017/"))
    mydb = myclient["MAYLA"]
    usercol = mydb["users"]
    if(usercol.find_one({"_id":id})!=None):
        res=usercol.find_one({"_id":id})['stage']
        myclient.close()
        return res
    else:
        myclient.close()
        return -1

def incstage(id):
    from datetime import datetime,timedelta
    import pymongo
    next_date=datetime.today() + timedelta(days=3)
    # myclient = pymongo.MongoClient('localhost:27017', username='root', password='root2022')
    myclient = pymongo.MongoClient(os.getenv("CONNECTION_STRING", "mongodb://aDXFitC:aDFit&gr3exiHXDA31vb@localhost:27017/"))
    mydb = myclient["MAYLA"]
    usercol = mydb["users"]
    usercol.find_one_and_update({"_id": id},{'$set':{'stage':(getstage(id)+1),'nextmsg':next_date}})
    myclient.close()

def getenddate(id):
    import pymongo
    # myclient = pymongo.MongoClient('localhost:27017', username='root', password='root2022')
    myclient = pymongo.MongoClient(os.getenv("CONNECTION_STRING", "mongodb://aDXFitC:aDFit&gr3exiHXDA31vb@localhost:27017/"))
    mydb = myclient["MAYLA"]
    usercol = mydb["users"]
    if(usercol.find_one({"_id":id})!=None):
        res=usercol.find_one({"_id":id})['enddate']
        myclient.close()
        return res
    else:
        myclient.close()
        return -1

def removeuser(id):
    from datetime import datetime
    import pymongo
    # myclient = pymongo.MongoClient('localhost:27017', username='root', password='root2022')
    myclient = pymongo.MongoClient(os.getenv("CONNECTION_STRING", "mongodb://aDXFitC:aDFit&gr3exiHXDA31vb@localhost:27017/"))
    mydb = myclient["MAYLA"]
    usercol = mydb["users"]
    usercol.find_one_and_update({"_id": id},{'$set':{'enddate':datetime.now()}})
    myclient.close()

def reactivateuser(id):
    import datetime
    import pymongo
    # myclient = pymongo.MongoClient('localhost:27017', username='root', password='root2022')
    myclient = pymongo.MongoClient(os.getenv("CONNECTION_STRING", "mongodb://aDXFitC:aDFit&gr3exiHXDA31vb@localhost:27017/"))
    mydb = myclient["MAYLA"]
    usercol = mydb["users"]
    usercol.find_one_and_update({"_id": id},{'$set':{'enddate':datetime.datetime.utcfromtimestamp(0)}})
    myclient.close()

def broadcast(msg):
    import pymongo
    from telegram.ext import Updater
    # myclient = pymongo.MongoClient('localhost:27017', username='root', password='root2022')
    myclient = pymongo.MongoClient(os.getenv("CONNECTION_STRING", "mongodb://aDXFitC:aDFit&gr3exiHXDA31vb@localhost:27017/"))
    mydb = myclient["MAYLA"]
    usercol = mydb["users"]
    # updater = Updater("2043435289:AAFOc0Q1mSCacbmJBZw6cYx7ys93kQscWbY") # prod
    updater = Updater(os.getenv("BOT_ID", "5594308493:AAGFf_dXgMjdo3nz2JjyVhSe1JZ4vP-treM"))
    for user in usercol.find():
        updater.bot.sendMessage(user['_id'],msg)
    myclient.close()

def send_audio(ID,audio):
    from telegram.ext import Updater
    # updater = Updater("2043435289:AAFOc0Q1mSCacbmJBZw6cYx7ys93kQscWbY") # prod
    updater = Updater(os.getenv("BOT_ID", "5594308493:AAGFf_dXgMjdo3nz2JjyVhSe1JZ4vP-treM"))
    updater.bot.send_voice(ID,open(audio,'rb').read())

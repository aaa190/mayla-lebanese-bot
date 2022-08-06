import json
from telegram.ext import Updater
import config
from datetime import datetime
import pymongo
import time
from config import send_audio
import logging

#Creating and Configuring Logger
Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(handlers=[logging.FileHandler("intervention.log",mode='a'),
                              logging.StreamHandler()
                              ],
                    format = Log_Format,
                    level = logging.INFO)

logger = logging.getLogger(__name__)
##ADD CHECKUP MESSAGES

def UpdateUsers():
    logger.info(f"Intervention Script Running")
    date = datetime.today()
    messages=json.load(open("Messages.json","r"))
    # Create the Updater and pass it your bot's token.
    # updater = Updater("2043435289:AAFOc0Q1mSCacbmJBZw6cYx7ys93kQscWbY") # prod
    updater = Updater("5594308493:AAGFf_dXgMjdo3nz2JjyVhSe1JZ4vP-treM")
    myclient = pymongo.MongoClient('localhost:27017', username='root', password='root2022')
    mydb = myclient["MAYLA"]
    usercol = mydb["users"]
    while (True):
        if(datetime.now().hour==13 and datetime.now().minute==00):
            logger.info(f"Scheduled Time Started")
            for user in usercol.find():
                key=user['_id']
                stage=str(config.getstage(key))
                if((usercol.find_one({'_id':key})['nextmsg']-date).days<=0):
                    updater.bot.sendMessage(key,messages["msg"+stage])
                    send_audio(key,f"./audio/msg{stage}.mp3")
                    config.incstage(key)
                    logger.info(f"User {key} Received stage: {stage} Message")
            logger.info(f"Users All Updated")
            myclient.close()
        time.sleep(30)

UpdateUsers()
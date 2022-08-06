from time import sleep

import telegram
from telegram import Update, ForceReply, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
import config
import logging

#DEVELOPER INFO: CHRISTOPHER FARAH CHRISTFARAH99@GMAIL.COM

#Creating and Configuring Logger
Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(handlers=[logging.FileHandler("logfile.log",mode='a'),
                              logging.StreamHandler()
                              ],
                    format = Log_Format,
                    level = logging.INFO)

logger = logging.getLogger(__name__)

NEWUSER_REPLY, CANCEL, IDENTITY_REQUEST, MSG= range(4)

# Starting Command /start, Inital Bot Conversation
def start_command(update: Update, context: CallbackContext):
    if (config.checknewuser(update.effective_user.id)):
        """Send a message when the command /start is issued."""
        reply_keyboard = [['نعم'], ['كلا']]
        user = update.effective_user.mention_markdown_v2()
        update.message.reply_markdown_v2(
            (fr'مرحبا %s,هل ترغب في مشاركتك في التوعية عن التنظيم الاسرة؟')%user,
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        )

        logger.info(f"User {update.effective_user.id} Reached for Registration")

        return NEWUSER_REPLY
    else:
        return echo(update,context)

#New User Successfully Registered to Database
def newuser(update: Update, context: CallbackContext,number):
    if(update.effective_user.username==None):
        username=''
    else:
        username=update.effective_user.username

    config.saveuser(update.effective_user.id, update.effective_user.full_name, username,number)
    update.message.reply_text(
        'شكرا لأنضمامك، تم تسجيلك في التوعية بنجاح', reply_markup=ReplyKeyboardRemove()
    )

    update.message.reply_text(
        'ستصلك رسالتك الاولى قريبا...', reply_markup=ReplyKeyboardRemove()
    )

    logger.info(f"User {update.effective_user.id} Successfuly Registered")

    return ConversationHandler.END

#Intervention Registration Canceling Request
def cancel_request(update: Update, context: CallbackContext)-> int:
    reply_keyboard = [['نعم'], ['كلا']]
    update.message.reply_markdown_v2(
        'هل انت متاكد بعدم مشاركة في التوعية؟ ',  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return cancel_request

#Intervention Cancelation Confirmed, end_date in database updated
def cancel_confirm(update: Update, context: CallbackContext):
    if ((not config.checknewuser(update.effective_user.id)) and config.getenddate(update.effective_user.id) == ""):
        from datetime import datetime

        date = datetime.now()

        config.removeuser(update.effective_user.id,
                          (str(date.day) + "-" + str(date.month) + "-" + str(date.day) + " " + str(
                              date.hour) + ":" + str(date.minute)))
    update.message.reply_text(
        'تم حذفك من التوعية، نشكرك على التواصل', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

#Auto-reply for registered user messages
def echo(update: Update, context: CallbackContext):
    update.message.reply_text(
        'شكرا لتواصلك، نرجو منك الانتظار رسالتك ستصل في الوقت المناسب...', reply_markup=ReplyKeyboardRemove()
    )

    logger.info(f"User {update.effective_user.id} Tried to contact \"{update.message.text}\"")
    return ConversationHandler.END

#Requesting Phone Number for Registering Users
def phone_request(update: Update, context: CallbackContext):
    reply_keyboard=ReplyKeyboardMarkup([[telegram.KeyboardButton('تسجيل الهاتف', request_contact=True)]])
    update.message.reply_text(
        'يرجى تسجيل رقم هاتفك بك لتحفيظ بياناتك' , reply_markup=reply_keyboard
    )
#ِADD GIF for button clicking

    logger.info(f"User {update.effective_user.id} Phone Requested")

    return IDENTITY_REQUEST

#Check if Phone Number Country Code is valid
def check_compatibility(update: Update, context: CallbackContext):
    number=update.message.contact['phone_number']
    number=number.replace("+","")
    if(number[:3]=='961'):
        logger.info(f"User {update.effective_user.id} Shared Valid Phone Number {number}")
        return newuser(update,context,int(number))
    else:
        update.message.reply_text(
            "شكرا لرغبتك بالمشاركة لكن للأسف المبادرة هي فقط للمقيمين في لبنان"
        )

        logger.error(f"User {update.effective_user.id} Shared invalid Phone Number {number}")

        return ConversationHandler.END


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # updater = Updater("2043435289:AAFOc0Q1mSCacbmJBZw6cYx7ys93kQscWbY") # prod
    updater = Updater("5594308493:AAGFf_dXgMjdo3nz2JjyVhSe1JZ4vP-treM")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_command),
                      MessageHandler(Filters.text & ~Filters.command, start_command)],
        states={
            NEWUSER_REPLY:[MessageHandler(Filters.regex('نعم'), phone_request),
                           MessageHandler(Filters.regex('كلا'), cancel_request),
                           MessageHandler(Filters.text & ~Filters.command, start_command)],
            IDENTITY_REQUEST: [MessageHandler(Filters.contact, check_compatibility),
                               MessageHandler(Filters.text & ~Filters.command, phone_request)],
            MSG:[MessageHandler(Filters.text & ~Filters.command, echo)
                 ],

            cancel_request: [MessageHandler(Filters.regex('نعم'), cancel_confirm),
                           MessageHandler(Filters.regex('كلا'), phone_request),
                             ]

        },

        fallbacks=[CommandHandler('cancel', cancel_request)],
    )


    dispatcher.add_handler(conv_handler)
    while True:
        try:
            updater.start_polling()
        except Exception as E:
            sleep(1)
            logger.error(E)
    

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
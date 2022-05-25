from dotenv import load_dotenv
import os
from time import sleep

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters


def button(update: Update, context: CallbackContext) -> None :
    global user_status
    username = update.effective_user.username
    query = update.callback_query
    if username in user_status :
        search_result = user_status[username]
        user_choose = search_result[int(query.data)]
        # showing the result that user choose by edit previous msg
        query.edit_message_text(text=user_choose)
        update.callback_query.message.reply_text('send other text')
    # Once things done, clear the user status
    user_status[username] = None

def msg(update: Update, context: CallbackContext) :
    global user_status
    username = update.effective_user.username
    msg = update.message.text
    if username in user_status :
        if user_status[username] == 'search' : # just an example
            # Do something...
            search_result = search(msg)
            # put the result into user_status for later process
            # but still, this is just an example
            user_status[username] = search_result
            reply_keyboard = []
            for i in range(len(search_result)) :
                reply_keyboard.append(
                    [InlineKeyboardButton(text=str(i + 1)+'. ' + search_result[i], callback_data=i)] # the callback data has to be an int
                )
            update.message.reply_text('Search Results', reply_markup=InlineKeyboardMarkup(reply_keyboard))
        elif user_status[username] == 'something else' :
            # Do something...
            user_status[username] = None


def start(update: Update, context: CallbackContext) -> None :
    # The first command
    # It is convenient that put the commands as keyboard button
    # But this is not necessary
    keyboard = [
        [KeyboardButton(text='/start'), KeyboardButton(text='/search')],
        [KeyboardButton(text='/help')],
    ]
    update.message.reply_text('Welcome message', reply_markup=ReplyKeyboardMarkup(keyboard=keyboard))

### global variables ###
# This variabl is for keeping users' status
# Once if your bot commands has continuity
# then you'll need this
user_status = dict()

if __name__ == "__main__" :
    # use the dotenv to protect secret values
    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    updater = Updater(TOKEN)
    # set handlers
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(MessageHandler(~Filters.command, msg))
    # start the bot
    updater.start_polling()
    print('bot start listening...')
    updater.idle()
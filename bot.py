"""
Calendar UN
"""

import logging
import os
import PyPDF2
from telegram import Update
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import urllib.request

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

MODE = "test"  # stable to deploy in heroku or test to deploy locally

if(MODE == "stable"):
    # TOKEN for stable version
    TOKEN = ""
    PORT = int(os.environ.get('PORT', 5000))
    ADDRESS = "https://.herokuapp.com/"
elif(MODE == "test"):
    # TOKEN for test version
    TOKEN = "1534450445:AAGDQ-ClfsEgdVpKfIDxIK9Vp_z8kaLhvfc"
else:
    print("Please select mode")
    exit()

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_html('Hello!')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_html('help')


def doc(update: Update, context: CallbackContext) -> None:
    update.message.reply_html(update.message.document.file_name)
    update.message.reply_document(update.message.document)
    url = update.message.document.get_file().file_path
    print(url)
    response = urllib.request.urlopen(url)
    file = open("calendar.pdf", 'wb')
    file.write(response.read())


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.document, doc))

    if(MODE == "stable"):
        # Start the Bot for stable version
        updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
        updater.bot.setWebhook(ADDRESS + TOKEN)
    elif(MODE == "test"):
        # Start the Bot for test version
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    main()

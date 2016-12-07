"""A bot to send news."""
import logging

from telegram import Emoji
from telegram.ext import Updater

# Enable logging

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Start the conversation."""
    text='Hi! {}'.format(Emoji.GRINNING_FACE_WITH_SMILING_EYES))

    bot.sendMessage(update.message.chat_id, text=text)


def help(bot, update):
    """Help user.

    Reminds the commands
    """
    bot.sendMessage(update.message.chat_id, text='Help!')


def get_new(bot, update):
    """Send a new link to the user."""
    pass


def summary(bot, update):
    """Update the summary for an url.

    Default is the last url sent
    """
    pass


def note(bot, update):
    """Update the note for an url.

    Default is the last url sent
    """
    pass


def tweet(bot, update):
    """Tweet an url.

    Default is the last url sent
    """
    pass


def error(bot, update, error):
    """Log all errors."""
    logger.error("An error (%s) occurred: %s"
                 % (type(error), error.message))


def main():
    """Main function."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("214692586:AAGvj-6EkhlgLlvyXeRwEr1FxU-wLU6tllg")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("help", help)

    # log all errors
    dp.addErrorHandler(error)

    # Start the Bot and store the update Queue, so we can insert updates
    update_queue = updater.start_polling(poll_interval=1, timeout=5)
    # Start CLI-Loop
    while True:
        text = input()

        # Gracefully stop the event handler
        if text == 'stop':
            updater.stop()
            break

        # else, put the text into the update queue
        elif len(text) > 0:
            update_queue.put(text)  # Put command into queue


if __name__ == '__main__':
    main()

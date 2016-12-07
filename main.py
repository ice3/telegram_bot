"""A bot to send news."""
import logging
from datetime import datetime
from datetime import timedelta

from telegram import Emoji
from telegram.ext import Updater

import db
import utils
import twitter

# Enable logging

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Start the conversation."""
    text = 'Hi! {}'.format(Emoji.GRINNING_FACE_WITH_SMILING_EYES)

    bot.sendMessage(update.message.chat_id, text=text)


def help(bot, update):
    """Help user.

    Reminds the commands
    """
    bot.sendMessage(update.message.chat_id, text='Help!')


def get_new(bot, update):
    """Send a new link to the user."""
    u = db.get_url_to_show()
    text = "Fresh news : {}".format(u)
    bot.sendMessage(update.message.chat_id, text=text)
    db.show(u)


def news_displayed_today(bot, update):
    """Send a new link to the user."""
    u = db.url_showed_today()
    text = "Woah, {} news send today".format(u)
    bot.sendMessage(update.message.chat_id, text=text)


def summary(bot, update):
    """Update the summary for an url.

    Default is the last url sent
    """
    command, t = update.message["text"].lstrip().split("/summary")
    if t:
        current_url = db.last_sent.link
        db.add_description(current_url, t)

        text = "Updated summary for : [[{}]]".format(current_url)
    else:
        text = "No summary text"
    bot.sendMessage(update.message.chat_id, text=text)


def new_url(bot, update, args):
    """User add a new url."""
    command, t = update.message["text"].lstrip().split("/new")
    if t:
        urls = utils.extract_urls_from_text(t)
        db.add_urls(urls)

        text = "Added {} to the database".format(len(urls))
    else:
        text = "No URLs given"
    bot.sendMessage(update.message.chat_id, text=text)


def note(bot, update):
    """Update the note for an url.

    Default is the last url sent
    """
    command, note = update.message["text"].lstrip().split("/note")
    if note:
        current_url = db.last_sent.link
        db.change_notation(current_url, note)

        text = "Updated notation for : [[{}]]".format(current_url)
    else:
        text = "No note"
    bot.sendMessage(update.message.chat_id, text=text)


def tweet(bot, update):
    """Tweet an url using buffer or normal tweet.

    Default is with buffer
    Default is the last url sent
    """
    command, method = update.message["text"].lstrip().split("/tweet")
    method = method or "buffer"
    current_url = db.last_sent.link
    desc = db.last_sent.twitter_description

    if method == "buffer":
        text = "Buffered : [[{}]]".format(current_url)
        twitter.buffer(current_url, desc)
    else:
        text = "Tweeted {}".format(current_url)
        twitter.tweet_now(current_url, desc)

    db.change_notation(current_url, note)
    bot.sendMessage(update.message.chat_id, text=text)


def error(bot, update, error):
    """Log all errors."""
    logger.error("An error (%s) occurred: %s"
                 % (type(error), error.message))


def auto_push_news(bot, update, args):
    """Sends news automatically at given time."""
    chat_id = update.message.chat_id

    def f(bot, update, args):
        auto_push_news(bot, update, args)
        get_new(bot, update)

    try:
        # args[0] should contain the time for the timer in seconds
        due = int(args[0])
        if due < 0:
            bot.sendMessage(chat_id, text='Sorry we can not go back to future!')

        # Add job to queue
        auto_push_news.q.put(lambda bot: f(bot, update, args), due, repeat=False)
        bot.sendMessage(chat_id, text='Auto push set!')

    except IndexError:
        bot.sendMessage(chat_id, text='Usage: /set <hours> or stop')
    except ValueError:
        bot.sendMessage(chat_id, text='AUto push stopped!')


def main():
    """Main function."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("214692586:AAGvj-6EkhlgLlvyXeRwEr1FxU-wLU6tllg")
    job_queue = updater.job_queue
    auto_push_news.q = job_queue
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("help", help)
    dp.addTelegramCommandHandler("fresh", get_new)
    dp.addTelegramCommandHandler("summary", summary)
    dp.addTelegramCommandHandler("note", note)
    dp.addTelegramCommandHandler("auto", auto_push_news)
    dp.addTelegramCommandHandler("new", new_url)
    dp.addTelegramCommandHandler("tweet", tweet)
    dp.addTelegramCommandHandler("stats", news_displayed_today)

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

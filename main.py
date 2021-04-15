import telebot

from consts import *
from db_worker import DBWorker
from models import *

bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None, threaded=False)
db_worker = DBWorker(db)


def publish_post(msg):
    sended_message = bot.send_message(CHANNEL_ID, msg.text, disable_web_page_preview=True)
    return sended_message.message_id


@bot.message_handler(commands=['start', 'help'])
def handle_support(msg):
    bot.reply_to(msg, WELCOME_MESSAGE)


@bot.message_handler(content_types=['text'])
def handle_message(msg):
    if msg.text.startswith('/'):
        bot.reply_to(msg, HELP_REQUEST)
        return
    sender = db_worker.get_user(msg)
    if sender and sender.blocked:
        bot.send_message(msg.chat.id, BLOCKED_USER)
        return
    if not sender:
        sender = db_worker.create_user(msg)
        sender.save()
    else:
        if db_worker.too_often(sender):
            bot.reply_to(msg, TOO_OFTEN)
            return
        old_message_id = db_worker.make_users_previous_post_archived(sender)
        try:
            bot.delete_message(CHANNEL_ID, old_message_id)
        except Exception:  # For now...
            pass

    post = db_worker.create_post(sender, msg)
    published_message_id = publish_post(msg)
    db_worker.update_post_msg_id(post, published_message_id)
    bot.reply_to(msg, SUCCESS_PUBLISH)


def main():
    bot.delete_webhook(drop_pending_updates=True)
    db.create_tables([Post, User])
    bot.polling(timeout=6, long_polling_timeout=15)


if __name__ == '__main__':
    main()

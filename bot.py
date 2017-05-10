import config
import telebot
import random
import time
import logging

logger = logging.getLogger('TEST')

bot = telebot.TeleBot(config.token)

# Базовые функции брента


def kukarek():  # брент говорить
    f = open('brent', encoding='utf-8').read().splitlines()
    return random.choice(f)

# Обработчик команд '/start' и '/help'.


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, 'Welcome to Brent bot')
    if message.text == '/help':
        bot.send_message(message.chat.id, 'Here we have only two commands: \n/start - Displays welcome message\n/help - Displays this info')


# Обработчки сообщений

@bot.message_handler(func=lambda msg: msg.from_user.id == config.userid)
def collecting_messages(message):
    s = message.text.lower()
    if s.find('тян') != -1:
        f = open('brent', 'a',  encoding='utf-8')
        f.write(message.text+'\n')
        f.close()


# Обработчик реплаев


@bot.message_handler(func=lambda msg: msg.reply_to_message is not None and msg.reply_to_message.from_user.id == config.bot_id)
def say_reply(message):
    bot.reply_to(message, kukarek())


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    f = open('userids', 'a',  encoding='utf-8')
    f.write(message.from_user.id.__str__()+' | ' + message.from_user.username + ' | ' + message.from_user.first_name +
            ' | ' + message.text + ' | ' + message.reply_to_message.__str__()+ '\n')
    f.close()
    s = message.text.lower()
    if (s.find('брент') != -1 or s.find('тян') != -1) and random.randint(1, 25) > 15:
        bot.send_message(message.chat.id, kukarek())


@bot.message_handler(content_types=["sticker"])
def stiker(message):
    pass


if __name__ == '__main__':
    # bot.polling(none_stop=True)
    while True:

        try:

            bot.polling(none_stop=True)

        # ConnectionError and ReadTimeout because of possible timout of the requests library

        # TypeError for moviepy errors

        # maybe there are others, therefore Exception

        except Exception as e:

            logger.error(e)

            time.sleep(15)

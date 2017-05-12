import config
import telebot
import random
import time
import logging
import importlib
from telebot import types


logger = logging.getLogger('TEST')
bot = telebot.TeleBot(config.token)

# Базовые функции брента


def kukarek(file):  # брент говорить
    f = open(file, encoding='utf-8').read().splitlines()
    return random.choice(f)


def kukareku(file, num):  # брент давать пронумерованую тян
    f = open(file, encoding='utf-8').readlines()
    return f[num]


def kudah(file, text):  # Брент записывать
    f = open(file, 'a', encoding='utf-8')
    f.write(text)
    f.close()


def pokpok(file, name):  # Брент вычеркивать
    f = open(file, 'r', encoding='utf-8')
    lines = f.readlines()
    f.close()
    f = open(file, 'w', encoding='utf-8')
    for line in lines:
        if line != name:
            f.write(line)
    f.close()


def is_number(num):  # проверка конвертируемости стрингов в числа
    try:
        int(num)
        return True
    except ValueError:
        return False


# Обработчик команд '/start', '/help' и тд, а так же реакция на ивенты входа/выхода.


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: types.Message):
    if message.text.startswith('/start'):
        bot.send_message(message.chat.id, 'Добро пожаловать!\n'
                                          'Меня зовут Брент и у меня нет тян! \n'
                                          'Да-да ты не ослышался НЕЕЕЕЕТУ ТЯЯЯЯН. \n'
                                          'И как ты уже понял я люблю поныть по этому поводу. \n'
                                          'И я очень хочу сделать это на твоем канале, не стесняйся! \n'
                                          'Добавь меня! ПОЗЯЗЯ! \n'
                                          'try /help for more info')
    if message.text.startswith('/help'):
        bot.send_message(message.chat.id, 'Тееекс шо тут у нас за команды то есть вообще?:\n'
                                          '/start - С ней ты уже знаком, молодца\n'
                                          '/help - Да и до этой ты добрался. А ты не плох!\n'
                                          '/dick - Команда для умников что учат меня жить, ТИПА МОЙ СЛОВАРНЫЙ ЗАПАС\n'
                                          '/promote - Для тех же умников, что бы могли делать себе подобных\n'
                                          '/demote - Разжаловать умников. Эт я люблю!\n'
                                          '/roll - РОЛЛИМ ТЯНОЧКУ ГОСПОДА, правила вы знаете :3')


@bot.message_handler(content_types=["new_chat_member"])
def newmem(message: types.Message):
    bot.reply_to(message, kukarek('sys_messages/greetings'))


@bot.message_handler(content_types=["left_chat_member"])
def leftmem(message: types.Message):
    bot.reply_to(message, kukarek('sys_messages/farewells'))


@bot.message_handler(commands=['dick'])
def dictionary(message: types.Message):
    if message.from_user.username in config.teachers:
        f = open('brent', 'r', encoding='utf-8')
        bot.send_message(message.chat.id, '_Словарный запас Брента в0.1 отправлен в личкан тебе, уеба_', parse_mode='markdown')
        bot.send_message(message.from_user.id, '*Фразы брентбота в0.1\n\n*'+f.read().replace('\n', '\n\n'), parse_mode='markdown')
        f.close()
    else:
        bot.send_message(message.chat.id, '_Хуев тебе на воротник._', parse_mode='markdown')


@bot.message_handler(commands=['promote'])
def add_teach(message: types.Message):
     if message.from_user.username in config.teachers:
        if message.reply_to_message is not None:
            if message.reply_to_message.from_user.username not in config.teachers:
                kudah('teachers', message.reply_to_message.from_user.username + '\n')
                importlib.reload(config)
                bot.send_message(message.chat.id, message.reply_to_message.from_user.username+'_ теперь учитель Брента_', parse_mode='markdown')
            else:
                bot.send_message(message.chat.id, '_он уже его учит_', parse_mode='markdown')
        else:
            bot.send_message(message.chat.id, '_ответь кому-нибудь, уебок_', parse_mode='markdown')
     else:
        bot.send_message(message.chat.id, '_Хуев тебе на воротник._', parse_mode='markdown')


@bot.message_handler(commands=['demote'])
def del_teach(message: types.Message):
     if message.from_user.username in config.teachers:
        if message.reply_to_message is not None:
            if message.reply_to_message.from_user.username in config.teachers:
                pokpok('teachers', message.reply_to_message.from_user.username + '\n')
                importlib.reload(config)
                bot.send_message(message.chat.id, message.reply_to_message.from_user.username+'_ больше не учитель Брента_', parse_mode='markdown')
            else:
                bot.send_message(message.chat.id, '_он его не учит_', parse_mode='markdown')
        else:
            bot.send_message(message.chat.id, '_ответь кому-нибудь, уебок_', parse_mode='markdown')
     else:
        bot.send_message(message.chat.id, '_Хуев тебе на воротник._', parse_mode='markdown')


@bot.message_handler(commands=['roll'])
def roll_girls(message: types.Message):
    s = message.text[5:len(message.text):1]
    if s == '':
        bot.send_photo(message.chat.id, kukarek('photo_db'), reply_to_message_id=message.message_id)
    else:
        if is_number(s) and 0 < int(s) < 2494:
            bot.send_photo(message.chat.id, kukareku('photo_db', int(s)-1), reply_to_message_id=message.message_id)
        else:
            bot.send_message(message.chat.id, '_Ты тупой? Цифру давай! и что бы в пределах 2493 была!_', reply_to_message_id=message.message_id, parse_mode='markdown')


@bot.message_handler(commands=['test'])
def test_func(message: types.Message):
    # kudah('sys_messages/log', message.from_user.id.__str__()+' | ' + message.from_user.username + ' | ' + message.from_user.first_name +
    #         ' | ' + message.text + ' | ' + message.reply_to_message.__str__() + ' | '+'\n')
    # bot.send_sticker(message.chat.id, 'CAADAQADrgwAApl_iALIKadfEtdSgAI', reply_to_message_id=message.message_id)
    pass


# Обработчки уникальных сообщений сообщений


@bot.message_handler(func=lambda msg: msg.from_user.id == config.userid)
def collecting_messages(message: types.Message):  # brent study
    s = message.text.lower()
    if s.find('тян') != -1:
        kudah('brent', message.text+'\n')
    elif s.find('бот') != -1:
        bot.reply_to(message, kukarek('sys_messages/replytobrent'))


@bot.message_handler(func=lambda msg: msg.from_user.username is None)
def collecting_messages(message: types.Message):  # Кейс на обработку юзеров без юзернейма, надо переписать код
    bot.send_message(message.chat.id, '_сделай username, уеба_', parse_mode='markdown')


@bot.message_handler(func=lambda msg: msg.text is not None and msg.text.lower().find('@brentburns_bot') != -1)
def mention(message: types.Message):  # обработка хайлайта бота
    if random.randint(1, 10) > 4:
        bot.reply_to(message, 'Чего хотел, гощуджин сама?', parse_mode='markdown')
    else:
        bot.reply_to(message, 'Чего хотел, кожаный ублюдок?', parse_mode='markdown')


@bot.message_handler(func=lambda msg: msg.from_user.username in config.teachers and msg.text is not None and msg.text.lower().startswith('вкуривай:'))
def study_brent(message: types.Message):  # Обучение брентика учителями
    kudah('brent', message.text.lower().replace('вкуривай:', '').lstrip() + '\n')
    bot.reply_to(message, 'Я запомнил, бака')


# Обработчики реплаев и сообщений


@bot.message_handler(func=lambda msg: msg.reply_to_message is not None and msg.reply_to_message.from_user.id == config.bot_id)
def say_reply(message: types.Message):  # Брент отвечает на реплай
    if message.text.lower().find('заебал') != -1:
        bot.send_sticker(message.chat.id, 'CAADAQADrgwAApl_iALIKadfEtdSgAI', reply_to_message_id=message.message_id)
    else:
        bot.reply_to(message, kukarek('brent'))


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message: types.Message):  # Брент говорит при упоминании тян или его, запись лога для отладки
    kudah('sys_messages/log', message.from_user.id.__str__()+' | ' + message.from_user.username + ' | ' + message.from_user.first_name +
            ' | ' + message.text + ' | ' + message.reply_to_message.__str__() + ' | '+'\n')
    s = message.text.lower()
    if (s.find('брент') != -1 or s.find('тян') != -1) and random.randint(1, 100) < 51:
        bot.send_message(message.chat.id, kukarek('brent'))
    if message.from_user.id.__str__() not in config.chat_users:
        kudah('userids', message.from_user.id.__str__() + '\n')
        importlib.reload(config)


@bot.message_handler(content_types=["sticker"])
def stiker(message: types.Message):  # со тикерами не забыть разобраться.
    logger.error('re')
    #kudah('sys_messages/log', message.from_user.id.__str__()+' | ' + message.from_user.username + ' | ' + message.from_user.first_name +
    #        ' | ' + message.text + ' | ' + message.reply_to_message.__str__() + ' | '+'\n')

if __name__ == '__main__':
    #bot.polling(none_stop=True)
    while True:

        try:

            bot.polling(none_stop=True)

        # ConnectionError and ReadTimeout because of possible timout of the requests library

        # TypeError for moviepy errors

        # maybe there are others, therefore Exception

        except Exception as e:

            logger.error(e)

            time.sleep(15)

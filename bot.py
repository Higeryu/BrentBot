import config
import telebot
import random
import time
import datetime
import logging
import importlib
from telebot import types

import brent

logger = logging.getLogger('TEST')
bot = telebot.TeleBot(config.token)


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
    bot.reply_to(message, brent.kukarek('sys_messages/greetings'))


@bot.message_handler(content_types=["left_chat_member"])
def leftmem(message: types.Message):
    bot.reply_to(message, brent.kukarek('sys_messages/farewells'))


@bot.message_handler(commands=['dick'])
def dictionary(message: types.Message):
    if message.from_user.username in brent.file_to_list('teachers'):
        f = open('brent', 'r', encoding='utf-8')
        bot.send_message(message.chat.id, '_Словарный запас Брента в0.1 отправлен в личкан тебе, уеба_', parse_mode='markdown')
        bot.send_message(message.from_user.id, '*Фразы брентбота в0.1\n\n*'+f.read().replace('\n', '\n\n'), parse_mode='markdown')
        f.close()
    else:
        bot.send_message(message.chat.id, '_Хуев тебе на воротник._', parse_mode='markdown')


@bot.message_handler(commands=['promote'])
def add_teach(message: types.Message):
     if message.from_user.username in brent.file_to_list('teachers'):
        if message.reply_to_message is not None:
            if message.reply_to_message.from_user.username not in brent.file_to_list('teachers'):
                brent.kudah('teachers', message.reply_to_message.from_user.username + '\n')
                bot.send_message(message.chat.id, message.reply_to_message.from_user.username.replace('_', ' ')+'_ теперь учитель Брента_', parse_mode='markdown')
            else:
                bot.send_message(message.chat.id, '_он уже его учит_', parse_mode='markdown')
        else:
            bot.send_message(message.chat.id, '_ответь кому-нибудь, уебок_', parse_mode='markdown')
     else:
        bot.send_message(message.chat.id, '_Хуев тебе на воротник._', parse_mode='markdown')


@bot.message_handler(commands=['demote'])
def del_teach(message: types.Message):
     if message.from_user.username in brent.file_to_list('teachers'):
        if message.reply_to_message is not None:
            if message.reply_to_message.from_user.username in brent.file_to_list('teachers'):
                brent.pokpok('teachers', message.reply_to_message.from_user.username + '\n')
                bot.send_message(message.chat.id, message.reply_to_message.from_user.username.replace('_', ' ')+'_ больше не учитель Брента_', parse_mode='markdown')
            else:
                bot.send_message(message.chat.id, '_он его не учит_', parse_mode='markdown')
        else:
            bot.send_message(message.chat.id, '_ответь кому-нибудь, уебок_', parse_mode='markdown')
     else:
        bot.send_message(message.chat.id, '_Хуев тебе на воротник._', parse_mode='markdown')


@bot.message_handler(commands=['remove'])
def del_mess(message: types.Message):
     if message.from_user.username in brent.file_to_list('teachers'):
        if message.reply_to_message is not None:
                brent.pokpok('brent', message.reply_to_message.text + '\n')
                bot.send_message(message.chat.id, '_забыл_', parse_mode='markdown')
                brent.kudah('brent_removed', message.reply_to_message.text + '\n')
        else:
            bot.send_message(message.chat.id, '_ответь на сообщение которое надо удалить_', parse_mode='markdown')
     else:
        bot.send_message(message.chat.id, '_Хуев тебе на воротник._', parse_mode='markdown')


@bot.message_handler(commands=['roll'])
def roll_girls(message: types.Message):
    s = message.text[5:len(message.text):1]
    if s == '':
        bot.send_photo(message.chat.id, brent.kukarek('photo_db'), reply_to_message_id=message.message_id)
    else:
        if brent.is_number(s) and 0 < int(s) <= brent.file_len('photo_db'):
            if str(int(s)-1) not in brent.file_to_list('chats/rolled_pics' + message.chat.id.__str__()):
                bot.send_photo(message.chat.id, brent.kukareku('photo_db', int(s)-1), reply_to_message_id=message.message_id)
                brent.kudah('chats/rolled_pics' + message.chat.id.__str__(), str(int(s)-1)+'\n')
            else:
                bot.reply_to(message, 'Уже было, роллируй другую')
        else:
            bot.send_message(message.chat.id, '_Ты тупой? Число давай! и что бы в пределах '+brent.file_len('photo_db').__str__()+' была!_', reply_to_message_id=message.message_id, parse_mode='markdown')


@bot.message_handler(commands=['roulette'])
def roulette(message):
    if config.roulette:
        bot.reply_to(message, 'Сначала закрой рулетку командой /end')
    else:
        importlib.reload(config)
        #open('chats/roulette' + message.chat.id.__str__(), 'w').close()
        config.roulette_owner = message.from_user.id.__str__()
        config.roulette = True
        bot.send_message(message.chat.id, message.from_user.username.replace('_', ' ') + ' *запустил рулетку, если хотите принять участие + в чат*', parse_mode='markdown')
        #  bot.send_message(message.chat.id, config.roulette_owner.__str__() + config.roulette.__str__())


@bot.message_handler(commands=['get_gamblers'])
def get_gamblers(message):
    if not brent.file_to_list('chats/roulette'+ message.chat.id.__str__()):
        bot.reply_to(message, 'Список участников пуст')
    else:
        f = open('chats/roulette'+ message.chat.id.__str__(), 'r', encoding='utf-8')
        bot.send_message(message.chat.id, 'Участники: \n' + f.read())


@bot.message_handler(commands=['get_winner'])
def get_winner(message):
    if message.from_user.id.__str__() == config.roulette_owner:
        if config.roulette_close:
            bot.send_message(message.chat.id, 'AND THE WINNER IS: @' + brent.kukarek('chats/roulette' + message.chat.id.__str__()))
        else:
            bot.reply_to(message, 'Сначала закрой набор командой /close')
    else:
        bot.reply_to(message, 'Ты не запускал рулетку, иди отсюда')


@bot.message_handler(commands=['close'])
def close_roul(message):
    if message.from_user.id.__str__() == config.roulette_owner:
        config.roulette_close = True
        bot.send_message(message.chat.id, '*Набор участников закрыт*', parse_mode='markdown')
    else:
        bot.reply_to(message, 'Иди отсюда. Жди пока хозяин рулетки сам закончит набор')


@bot.message_handler(commands=['end'])
def close_roul(message):
    if config.roulette and message.from_user.id.__str__() == config.roulette_owner:
        importlib.reload(config)
        open('chats/roulette'+ message.chat.id.__str__(), 'w').close()
        bot.send_message(message.chat.id, '*Рулетка закрыта*', parse_mode='markdown')
    else:
        bot.send_message(message.chat.id, '*Закрывать нечего, рулетка не запущена или ты не ее владелец\nТекущий владелец*: '+ config.roulette_owner.__str__() , parse_mode='markdown')


# @bot.message_handler(commands=['pidor'])
# def pidor(message: types.Message):
#     bot.reply_to(message, datetime.datetime.now())
#     config.pidor_time = datetime.datetime.now()
#     time.sleep(20)
#     bot.reply_to(message, datetime.datetime.now() - config.pidor_time)
#     if datetime.datetime.now() > datetime.timedelta(hours=24) + config.pidor_time:
#         bot.reply_to(message, 'new pidor')
#     else:
#         bot.reply_to(message, 'not new pidor pidor')


#@bot.message_handler(commands=['test'])  # Ообработка инлайн кнопок, вернуться позже
#def test_func(message: types.Message):
#     # kudah('sys_messages/log'+message.chat.id.__str__(), message.from_user.id.__str__()+' | ' + message.from_user.username + ' | ' + message.from_user.first_name +
#     #         ' | ' + message.text + ' | ' + message.reply_to_message.__str__() + ' | '+'\n')
#     # bot.send_sticker(message.chat.id, 'CAADAQADrgwAApl_iALIKadfEtdSgAI', reply_to_message_id=message.message_id)
#     keyboard = types.InlineKeyboardMarkup()
#     callback_button = types.InlineKeyboardButton(text="Нажми меня", callback_data="test", switch_inline_query_current_chat='tes')
#     keyboard.add(callback_button)
#     bot.send_message(message.chat.id, "Я – сообщение из обычного режима", reply_markup=keyboard)
#
#
# @bot.callback_query_handler(func=lambda call: True)
# def callback_inline(call):
#     # Если сообщение из чата с ботом
#     if call.message:
#         if call.data == "test":
#             bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.message.text+ '\n' + call.from_user.username, )
#             test_func(call.message)
#     # Если сообщение из инлайн-режима
#     elif call.inline_message_id:
#         if call.data == "test":
#             bot.edit_message_text(inline_message_id=call.inline_message_id, text="Бдыщь")



# Обработчки уникальных сообщений сообщений

@bot.message_handler(func=lambda msg: msg.text is not None and config.roulette and msg.text.find('+') != -1 )
def roul_users(message):
    if config.roulette_close:
        bot.reply_to(message, 'Набор закрыт')
    elif message.from_user.username in brent.file_to_list('chats/roulette' + message.chat.id.__str__()):
        bot.reply_to(message, 'Ты уже в списке участников')
    else:
        brent.kudah('chats/roulette' + message.chat.id.__str__(), message.from_user.username + '\n')
        bot.reply_to(message, 'Добавлен')


@bot.message_handler(func=lambda msg: msg.from_user.id == config.userid)
def collecting_messages(message: types.Message):  # brent study
    s = message.text.lower()
    if s.find('тян') != -1:
        brent.kudah('brent', message.text+'\n')
    elif s.find('бот') != -1:
        bot.reply_to(message, brent.kukarek('sys_messages/replytobrent'))


@bot.message_handler(func=lambda msg: msg.from_user.username is None)
def collecting_messages(message: types.Message):  # Кейс на обработку юзеров без юзернейма, надо переписать код
    bot.send_message(message.chat.id, '_сделай username, уеба_', parse_mode='markdown')


@bot.message_handler(func=lambda msg: msg.text is not None and msg.text.lower().find('@brentburns_bot') != -1)
def mention(message: types.Message):  # обработка хайлайта бота
        bot.reply_to(message, brent.kukarek('sys_messages/hilight_reply'), parse_mode='markdown')


@bot.message_handler(func=lambda msg: msg.from_user.username in brent.file_to_list('teachers') and msg.text is not None and msg.text.lower().startswith('вкуривай:'))
def study_brent(message: types.Message):  # Обучение брентика учителями
    brent.kudah('brent', message.text.lower().replace('вкуривай:', '').lstrip() + '\n')
    bot.reply_to(message, 'Я запомнил, бака')


# Обработчики реплаев и сообщений


@bot.message_handler(func=lambda msg: msg.reply_to_message is not None and msg.reply_to_message.from_user.id == config.bot_id)
def say_reply(message: types.Message):  # Брент отвечает на реплай
    if brent.check_in(message.text.lower(), brent.file_to_list('sys_messages/bully')):
        bot.send_sticker(message.chat.id, 'CAADAgADegIAAs7Y6AuR3bJUKSMqIgI', reply_to_message_id=message.message_id)  # CAADAQADrgwAApl_iALIKadfEtdSgAI No bully
    else:
        bot.reply_to(message, brent.kukarek('brent'))


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message: types.Message):  # Брент говорит при упоминании тян или его, запись лога для отладки
    brent.kudah('chats/log'+message.chat.id.__str__(), message.from_user.id.__str__()+' | ' + message.from_user.username + ' | ' + message.from_user.first_name +
            ' | ' + message.text + ' | ' + message.reply_to_message.__str__() + ' | '+'\n')
    s = message.text.lower()
    if (s.find('брент') != -1 or s.find('тян') != -1) and random.randint(1, 100) < 51:
        bot.send_message(message.chat.id, brent.kukarek('brent'))
    if message.from_user.id.__str__() not in brent.file_to_list('chats/userids'+message.chat.id.__str__()) and message.chat.type != 'private':
        brent.kudah('chats/userids'+message.chat.id.__str__(), message.from_user.id.__str__() + '\n')


@bot.message_handler(content_types=["sticker"])
def stiker(message: types.Message):  # со тикерами не забыть разобраться.
    pass

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

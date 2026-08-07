import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('UR TOKEN')
user_owner = int('UR ID IN TG')
requests = {}

def main_menu ():
    markup = types.InlineKeyboardMarkup()
    vork = types.InlineKeyboardButton('Отправить ворк', style='primary', callback_data='otpravit_vork')
    statistic = types.InlineKeyboardButton('Статистика', callback_data='statistic')
    rating_system = types.InlineKeyboardButton('Критерии рейта', callback_data='rating_system')
    markup.row(vork)
    markup.row(rating_system, statistic)
    return markup


def menu_vubora ():
    markup = types.InlineKeyboardMarkup()
    for_reit = types.InlineKeyboardButton('Отправить ворк для рейта', style="primary", callback_data='reit')
    for_feedback = types.InlineKeyboardButton('Отправить ворк для фидбэка', style='primary', callback_data='feedback')
    nazad = types.InlineKeyboardButton('Назад', callback_data='nazad')
    markup.row(for_reit, for_feedback)
    markup.row(nazad)
    return markup


def statistic_menu ():
    markup = types.InlineKeyboardMarkup()
    nazad = types.InlineKeyboardButton('Назад', callback_data='nazad')
    markup.row(nazad)
    return markup


@bot.message_handler(commands=['start'])
def start (message):
    conn = sqlite3.connect('DATABASAREQS.sql')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, ban_status BOOLEAN DEFAULT FALSE, reqs int, good_Reqs int, bad_reqs int)')
    cur.execute('INSERT OR IGNORE INTO users (id, reqs, good_reqs, bad_reqs) VALUES (?, 0, 0, 0)',(message.chat.id,))
    conn.commit()
    cur.execute(f'SELECT ban_status FROM users WHERE id = {message.chat.id}')
    ban_status = cur.fetchone()

    if ban_status and ban_status[0] == False:
        bot.send_message(message.chat.id, f'<b>Привет {message.from_user.first_name}! <tg-emoji emoji-id="5461117441612462242">🙂</tg-emoji></b>\n\n'+
                         '<b>В этом боте вы сможете отправлять реквесты прямоком камню, либо на рейт, либо на фидбэк.</b>\n'+
                         '<b>Внизу меню.</b>',
                        parse_mode='html', reply_markup=main_menu())
    elif ban_status and ban_status [0] == True:
        bot.send_message(message.chat.id, f'<b>Привет {message.from_user.first_name}! Вас забанили <tg-emoji emoji-id="5461117441612462242">🙂</tg-emoji></b>\n',
                                parse_mode='html')

    cur.close()
    conn.close()

@bot.callback_query_handler(func=lambda callback: callback.data == 'statistic')
def statistic (callback):
    conn = sqlite3.connect('DATABASAREQS.sql')
    cur = conn.cursor()

    cur.execute(f'SELECT reqs FROM users WHERE id = {callback.message.chat.id}')
    reqs = cur.fetchone()
    cur.execute(f'SELECT bad_reqs FROM users WHERE id = {callback.message.chat.id}')
    bad_reqs = cur.fetchone()
    cur.execute(f'SELECT good_reqs FROM users WHERE id = {callback.message.chat.id}')
    good_reqs = cur.fetchone()

    bot.edit_message_text(f'<b>Вот ваша статистика.\n\n</b>'+
                        f'<b>За все время вы отправили {reqs[0]} реквестов</b>'+
                        f'<b>\n <tg-emoji emoji-id="5210952531676504517">❌</tg-emoji> За все время ваши реквесты отклонили {bad_reqs[0]} раз</b>'+
                        f'<b>\n <tg-emoji emoji-id="5206607081334906820">✔️</tg-emoji> За все время ваши реквесты приняли {good_reqs[0]} раз</b>',
                        callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=statistic_menu())

    cur.close()
    conn.close()


@bot.callback_query_handler(func=lambda callback: callback.data == 'nazad')
def perevod_v_main_menu (callback):
    conn = sqlite3.connect('DATABASAREQS.sql')
    cur = conn.cursor()

    cur.execute(f'SELECT ban_status FROM users WHERE id = {callback.message.chat.id}')
    ban_status = cur.fetchone()

    if ban_status and ban_status[0] == False:
        bot.edit_message_text(f'<b>Привет! <tg-emoji emoji-id="5461117441612462242">🙂</tg-emoji></b>\n\n'+
                         '<b>В этом боте вы сможете отправлять реквесты прямоком камню, либо на рейт, либо на фидбэк.</b>\n'+
                         '<b>Внизу меню.</b>',
                        callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=main_menu())
    elif ban_status and ban_status [0] == True:
        bot.edit_message_text(f'<b>Привет! Вас забанили <tg-emoji emoji-id="5461117441612462242">🙂</tg-emoji></b>\n',
                                callback.message.chat.id, callback.message.message_id, parse_mode='html')

    cur.close()
    conn.close()



@bot.callback_query_handler(func=lambda callback: callback.data == 'rating_system')
def reit_system_text (callback):
    bot.edit_message_text(f'<b>На данный момент, критериев рейтов нету.</b>',
                        callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=statistic_menu())



@bot.callback_query_handler(func=lambda callback: callback.data == 'otpravit_vork')
def vubor (callback):
    bot.edit_message_text(f'<b><tg-emoji emoji-id="5440660757194744323">‼️</tg-emoji>Пожалуйста, выберете что именно вы хотите отправить.</b>',
                    callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=menu_vubora())


@bot.callback_query_handler(func=lambda callback: callback.data in ['reit', 'feedback'])
def deistvii (callback):
    msg = bot.edit_message_text(f'<b><tg-emoji emoji-id="5210956306952758910">👀</tg-emoji> Отправьте айди своего уровня, и желательно шоукейс вашего уровня.</b>',
                            callback.message.chat.id, callback.message.message_id, parse_mode='html')
    requests[msg.message_id] = callback.message.chat.id
    if callback.data == 'reit':
        settings = 'Оценить уровень'
    elif callback.data == 'feedback':
        settings = 'Получить фидбэк'
    bot.register_next_step_handler(callback.message, send_message_to_owner, settings=settings)


def send_message_to_owner(message, settings):
    user_id = message.chat.id
    user_message = message.text
    conn = sqlite3.connect('DATABASAREQS.sql')
    cur = conn.cursor()

    cur.execute('UPDATE users SET reqs = reqs + 1 WHERE id = ?',(message.chat.id,))
    conn.commit()
    cur.close()
    conn.close()

    forwarded = bot.forward_message(user_owner, message.chat.id, message.message_id)
    requests[forwarded.message_id] = user_id

    markup = types.InlineKeyboardMarkup()
    prinyati = types.InlineKeyboardButton('Принять ✔️', 
                                    parse_mode='html', style='success', callback_data=f'Prinat {user_id}')
    nahui = types.InlineKeyboardButton('Послать нахуй ❌', 
                                    parse_mode='html', style='danger', callback_data=f'Nahui {user_id}')
    ban = types.InlineKeyboardButton('Забанить пользователя ⛔️',
                                    parse_mode='html', callback_data=f'Ban {user_id}')
    if settings == 'Оценить уровень':
        markup.row(prinyati, nahui)
    markup.row(ban)

    msg = bot.send_message(user_owner, f'<b>От: @{user_id}, ник: {message.from_user.first_name}</b>'+
                    f'<b>\nТип хочет: {settings}</b>',
                    parse_mode='html', reply_markup=markup)

    requests[msg.message_id] = user_id


@bot.message_handler(func=lambda m: m.chat.id == user_owner)
def owner_reply(message):
    if not message.reply_to_message:
        return
    request_message_id = message.reply_to_message.message_id
    if request_message_id not in requests:
        bot.send_message(user_owner, '<tg-emoji emoji-id="5210952531676504517">❌</tg-emoji> Не удалось определить ебаната.')
        return
    
    user_id = requests[request_message_id]
    bot.send_message(user_id, f'<b>Камень отправил вам фидбэк по поводу вашего реквеста.</b>\n\n{message.text}', parse_mode="html")

    
@bot.callback_query_handler(func=lambda callback: True)
def reqs (callback):
    conn = sqlite3.connect('DATABASAREQS.sql')
    cur = conn.cursor()
    hui = (callback.data).split(" ")
    calback = hui[0]
    user_id = int(hui[1])

    if calback == 'Ban':
        cur.execute('UPDATE users SET ban_status = ? WHERE id = ?', 
                           (True, user_id))
        conn.commit()
    elif calback == 'Nahui':
        cur.execute('UPDATE users SET bad_reqs = bad_reqs + 1 WHERE id = ?',(user_id,))
        conn.commit()
        bot.send_message(user_id, f'<b><tg-emoji emoji-id="5210952531676504517">❌</tg-emoji> К сожалению, ваш реквест камню не понравился, и поэтому он не получит рейт.</b>', parse_mode='html')
    elif calback == 'Prinat':
        cur.execute('UPDATE users SET good_reqs = good_reqs + 1 WHERE id = ?',(user_id,))
        conn.commit()
        bot.send_message(user_id, f'<b><tg-emoji emoji-id="5206607081334906820">✔️</tg-emoji> Поздравляем! Ваш реквест проверил камень, и оценил ваш уровень!</b>', parse_mode='html')
    cur.close()
    conn.close()

bot.polling(non_stop=True)
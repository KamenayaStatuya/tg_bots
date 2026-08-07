import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('8640766684:AAHvtwBv94iSYzoyHWE_k9f0-siAg1o269k')
user_owner = 6060100513
requests = {}

def main_menu (user):
    markup = types.InlineKeyboardMarkup()
    vork = types.InlineKeyboardButton('Отправить ворк', style='primary', callback_data='otpravit_vork')
    statistic = types.InlineKeyboardButton('Статистика', callback_data='statistic')
    rating_system = types.InlineKeyboardButton('Критерии рейта', callback_data='rating_system')
    admin_menu = types.InlineKeyboardButton('Админ панель', style='success', callback_data='admin_menu')
    if user == user_owner:
        markup.row(admin_menu)
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

def admin_menu ():
    markup = types.InlineKeyboardMarkup()
    unban = types.InlineKeyboardButton('Разбанить пользователя',style="success",  callback_data='unban_polz')
    ban = types.InlineKeyboardButton('Забанить пользователя', style="danger", callback_data='ban_polz')
    check = types.InlineKeyboardButton('Посмотреть статистику пользователя.', style="primary", callback_data='check_statistic')
    nazad = types.InlineKeyboardButton('Назад', callback_data='nazad')
    markup.row(unban,ban)
    markup.row(check)
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
                         '<b>В этом боте вы сможете отправлять реквесты прямоком камню, либо на рейт, либо на фидбэк.</b>\n\n'+
                         '<b>Исходный код бота, если вы хотите использовать код для своих нужд: https://github.com/KamenayaStatuya/tg_bots/blob/main/bot_for_reqs.py \n\nВнизу меню.</b>',
                        parse_mode='html', reply_markup=main_menu(message.chat.id))
    elif ban_status and ban_status [0] == True:
        bot.send_message(message.chat.id, f'<b>Привет {message.from_user.first_name}! Вас забанили <tg-emoji emoji-id="5461117441612462242">🙂</tg-emoji></b>\n',
                                parse_mode='html')

    cur.close()
    conn.close()



@bot.callback_query_handler(func=lambda callback: callback.data in ['admin_menu'])
def menu_admin_goida (callback):
    bot.edit_message_text(f'<b>Вы попали в админ меню</b>', 
                          callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=admin_menu())


@bot.callback_query_handler(func=lambda callback: callback.data in ['unban_polz','ban_polz','check_statistic'])
def start_unban_for_callback (callback):
    bot.answer_callback_query(callback.id)
    if callback.message.chat.id == user_owner:
        bot.send_message(callback.message.chat.id, f'<b>Напишите пользователя для манипуляций</b>',
                            parse_mode='html')
        if callback.data == 'unban_polz':
            bot.register_next_step_handler(callback.message, unban)
        elif callback.data == 'ban_polz':
            bot.register_next_step_handler(callback.message, ban)
        elif callback.data == 'check_statistic':
            bot.register_next_step_handler(callback.message, check_statistic)
    else:
        bot.send_message(callback.message.chat.id, f'<b>Извините, у вас нету должных прав.</b>',
                        parse_mode='html')

def unban (message):
    print('хуй')
    conn = sqlite3.connect('DATABASAREQS.sql')
    cur = conn.cursor()

    try:
        user = int(message.text)
        try:
            cur.execute('UPDATE users SET ban_status = ? WHERE id = ?', 
                        (False, user))
            conn.commit()
            bot.send_message(message.chat.id, f'Пользователь успешно был разбанен', 
                            parse_mode='html')
        except:
            bot.send_message(message.chat.id, f'Вы ввели не тот формат.', 
                parse_mode='html')
    except:
        bot.send_message(message.chat.id, f'Вы ввели не тот формат.', 
                        parse_mode='html')
    
    cur.close()
    conn.close()

def ban (message):
    conn = sqlite3.connect('DATABASAREQS.sql')
    cur = conn.cursor()

    try:
        user = int(message.text)
        try:
            cur.execute('UPDATE users SET ban_status = ? WHERE id = ?', 
                        (True, user))
            conn.commit()
            bot.send_message(message.chat.id, f'Пользователь успешно был забанен', 
                            parse_mode='html')
        except:
            bot.send_message(message.chat.id, f'Вы ввели не тот формат.', 
                parse_mode='html')
    except:
        bot.send_message(message.chat.id, f'Вы ввели не тот формат.', 
                        parse_mode='html')

def check_statistic (message):
    try:
        user = int(message.text)
    except:
        bot.send_message(message.chat.id, f'Вы ввели не тот формат.', 
                        parse_mode='html')
    conn = sqlite3.connect('DATABASAREQS.sql')
    cur = conn.cursor()
    cur.execute(f'SELECT reqs FROM users WHERE id = {user}')
    reqs = cur.fetchone()
    cur.execute(f'SELECT bad_reqs FROM users WHERE id = {user}')
    bad_reqs = cur.fetchone()
    cur.execute(f'SELECT good_reqs FROM users WHERE id = {user}')
    good_reqs = cur.fetchone()

    bot.send_message(message.chat.id,f'<b>Вот статистика.\n\n</b>'+
                        f'<b>За все время вы отправили {reqs[0]} реквестов</b>'+
                        f'<b>\n <tg-emoji emoji-id="5210952531676504517">❌</tg-emoji> За все время ваши реквесты отклонили {bad_reqs[0]} раз</b>'+
                        f'<b>\n <tg-emoji emoji-id="5206607081334906820">✔️</tg-emoji> За все время ваши реквесты приняли {good_reqs[0]} раз</b>',
                        parse_mode='html')

@bot.callback_query_handler(func=lambda callback: callback.data == 'statistic')
def statistic (callback):
    bot.answer_callback_query(callback.id)
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
    bot.answer_callback_query(callback.id)
    conn = sqlite3.connect('DATABASAREQS.sql')
    cur = conn.cursor()

    cur.execute(f'SELECT ban_status FROM users WHERE id = {callback.message.chat.id}')
    ban_status = cur.fetchone()

    if ban_status and ban_status[0] == False:
        bot.edit_message_text(f'<b>Привет! <tg-emoji emoji-id="5461117441612462242">🙂</tg-emoji></b>\n\n'+
                         '<b>В этом боте вы сможете отправлять реквесты прямоком камню, либо на рейт, либо на фидбэк.</b>\n'+
                         '<b>Внизу меню.</b>',
                        callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=main_menu(callback.message.chat.id))
    elif ban_status and ban_status [0] == True:
        bot.edit_message_text(f'<b>Привет! Вас забанили <tg-emoji emoji-id="5461117441612462242">🙂</tg-emoji></b>\n',
                                callback.message.chat.id, callback.message.message_id, parse_mode='html')

    cur.close()
    conn.close()



@bot.callback_query_handler(func=lambda callback: callback.data == 'rating_system')
def reit_system_text (callback):
    bot.answer_callback_query(callback.id)
    bot.edit_message_text(f'<b>На данный момент, критериев рейтов нету.</b>',
                        callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=statistic_menu())



@bot.callback_query_handler(func=lambda callback: callback.data == 'otpravit_vork')
def vubor (callback):
    bot.answer_callback_query(callback.id)
    bot.edit_message_text(f'<b><tg-emoji emoji-id="5440660757194744323">‼️</tg-emoji>Пожалуйста, выберете что именно вы хотите отправить.</b>',
                    callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=menu_vubora())


@bot.callback_query_handler(func=lambda callback: callback.data in ['reit', 'feedback'])
def deistvii (callback):
    bot.answer_callback_query(callback.id)
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
    bot.delete_message(message.chat.id, message.message_id)
    bot.edit_message_text(f'<tg-emoji emoji-id="5206607081334906820">✔️</tg-emoji>Вы успешно отправили реквест камню. \nОжидайте...',
                          message.chat.id, message.message_id-1,parse_mode='html')

    markup = types.InlineKeyboardMarkup()
    prinyati = types.InlineKeyboardButton('Принять ✔️', 
                                    parse_mode='html', style='success', callback_data=f'Prinat {user_id}')
    nahui = types.InlineKeyboardButton('Послать нахуй ❌', 
                                    parse_mode='html', style='danger', callback_data=f'Nahui {user_id}')
    ban = types.InlineKeyboardButton('Забанить пользователя ⛔️',
                                    parse_mode='html', callback_data=f'Ban {user_id}')
    uze_ocenen = types.InlineKeyboardButton('Сказать что лвл уже оценен',
                                    parse_mode='html', callback_data=f'Uze_ocenen {user_id}')
    if settings == 'Оценить уровень':
        markup.row(prinyati, nahui)
        markup.row(uze_ocenen)
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
    bot.send_message(user_id, f'<b><tg-emoji emoji-id="5440660757194744323">‼️</tg-emoji>Камень отправил вам фидбэк по поводу вашего реквеста.</b>\n\n{message.text}', parse_mode="html")

    
@bot.callback_query_handler(func=lambda callback: True)
def reqs (callback):
    bot.answer_callback_query(callback.id)
    bot.edit_message_text(f'<b><tg-emoji emoji-id="5440660757194744323">‼️</tg-emoji>Вы ответили на реквест, теперь взаимодействовать с ним нельзя.</b>', 
                        callback.message.chat.id, callback.message.message_id, parse_mode='html')

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
    elif calback == 'Uze_ocenen':
        bot.send_message(user_id, f'<b><tg-emoji emoji-id="5206607081334906820">✔️</tg-emoji> Поздравляем! Ваш реквест проверил камень!\n\n<tg-emoji emoji-id="5440660757194744323">‼️</tg-emoji>Но есть проблема, уровень уже оценен на гдпсе...</b>', parse_mode='html')
    cur.close()
    conn.close()

bot.polling(non_stop=True)
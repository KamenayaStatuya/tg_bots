# Внимание, этот бот использует эмодзи, которые доступны только для премиум пользователей. Если у вас нету премиум подписки, то настоятельно нерекомендую вам использовать конкретно этот скрипт.
# Please note: this bot uses emojis that are available only to Premium users. If you do not have a Premium subscription, I strongly advise against using this specific script.

import telebot
import time
from telebot import types
import sqlite3

bot = telebot.TeleBot('СТАВЬ СЮДА СВОЙ ТОКЕН БОТА')

def main_menu ():
    markup = types.InlineKeyboardMarkup()
    calculator = types.InlineKeyboardButton('Подсчитать', callback_data='calculator')
    settings = types.InlineKeyboardButton('Настройки', callback_data='settings')
    markup.row(calculator, settings)
    return markup

def settings_menu ():
    markup = types.InlineKeyboardMarkup()
    usd = types.InlineKeyboardButton('USD', callback_data='usd')
    rub = types.InlineKeyboardButton('RUB', callback_data='rub')
    eur = types.InlineKeyboardButton('EUR', callback_data='eur')
    nazad = types.InlineKeyboardButton('Назад', callback_data='nazad')
    markup.row(usd, rub, eur)
    markup.row(nazad)
    return markup

def REAL_final_calculate(accs, comps, valuta_settings):
    mnoziteli = 1
    one_drop_per_week = 0.65
    price_one_acc = 25
    price_one_comp = 1200
    start_message = ''
    prem_emoji = ''
    summa_rashodov = (round((round(((price_one_comp)*int(comps)),2) + round((price_one_acc*int(accs)),2)),2)) * mnoziteli

    if "usd" == valuta_settings[0]:
        mnoziteli = 1
        start_message = '<b>Вы ранее в настройках выбрали валюту USD<tg-emoji emoji-id="5409048419211682843">💵</tg-emoji>, Поэтому все расчеты будут происходить в этой валюте</b>'
        prem_emoji = '<tg-emoji emoji-id="5409048419211682843">💵</tg-emoji>'
    if "eur" == valuta_settings[0]:
        mnoziteli = 0.87
        start_message = '<b>Вы ранее в настройках выбрали валюту RUB<tg-emoji emoji-id="5233326571099534068">💸</tg-emoji>, Поэтому все расчеты будут происходить в этой валюте</b>'
        prem_emoji = '<tg-emoji emoji-id="5233326571099534068">💸</tg-emoji>'
    if "rub" == valuta_settings[0]:
        mnoziteli = 79.26
        start_message = '<b>Вы ранее в настройках выбрали валюту RUB<tg-emoji emoji-id="5231449120635370684">💸</tg-emoji>, Поэтому все расчеты будут происходить в этой валюте</b>'
        prem_emoji = '<tg-emoji emoji-id="5231449120635370684">💸</tg-emoji>'

    final_text = str(f'{start_message}\n\n<b><tg-emoji emoji-id="5456140674028019486">⚡️</tg-emoji>Чистый доход с {accs} аккаунтов!</b> \n\n'+
                     f'<b>Со всех аккаунтов, каждый еженедельный дроп тебе будет приносить {round(((one_drop_per_week*mnoziteli)*int(accs)), 2)} {prem_emoji}</b>\n'+
                     f'<b>В месяц же вы будете зарабатывать {round(((one_drop_per_week*mnoziteli)*int(accs))*5, 2)} {prem_emoji}</b>\n'+
                     f'<b>В год же вы будете зарабатывать {round(((one_drop_per_week*mnoziteli)*int(accs))*60, 2)} {prem_emoji}</b>\n\n'+
                     f'<b>Но также у вас и расходы будут. Сначала вам придется закупиться аккаунтами примерно на сумму {round(((price_one_acc*int(accs))*mnoziteli),2)} {prem_emoji}</b>\n'+
                     f'<b>На компьютеры вам нужно потратиться около {round(((price_one_comp*mnoziteli)*int(comps)),2)}</b>\n'+
                     f'<b>В итоге вам нужно потратить {summa_rashodov} {prem_emoji}</b>\n'+
                     f'<b>Теперь поймем сколько времени займет, чтобы выйти в ноль. Вам нужно {int(summa_rashodov/(one_drop_per_week*int(accs)))} недель, или {round(int(summa_rashodov/5)/(one_drop_per_week*int(accs)),1)} месяцов</b>\n\n'
                     f'(Чтобы вернуться в меню, пропишите команду /menu)')
    return final_text

@bot.message_handler(commands=['start'])
def menu (message):
    conn = sqlite3.connect('DadaBasaForBotCS2Farm.sql')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, settings_value varchar(5))')
    cur.execute(f'INSERT OR IGNORE INTO users (id, settings_value) VALUES ({message.chat.id}, "usd")')
    conn.commit()
    cur.close()
    conn.close()
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, f'<b>Привет {message.from_user.first_name} <tg-emoji emoji-id="5461117441612462242">🙂</tg-emoji></b> \n\n'+
                     f'Добро пожаловать в бот, который подсчитывать реальную прибыль с кф фермы.',
                       parse_mode='html', reply_markup=main_menu())

@bot.message_handler(commands=['menu'])
def menu (message):
    conn = sqlite3.connect('DadaBasaForBotCS2Farm.sql')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, settings_value varchar(5))')
    cur.execute(f'INSERT OR IGNORE INTO users (id, settings_value) VALUES ({message.chat.id}, "usd")')
    conn.commit()
    cur.close()
    conn.close()
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id-1)
    bot.send_message(message.chat.id, f'<b>Привет {message.from_user.first_name} <tg-emoji emoji-id="5461117441612462242">🙂</tg-emoji></b> \n\n'+
                     f'Добро пожаловать в бот, который подсчитывать реальную прибыль с кф фермы.',
                       parse_mode='html', reply_markup=main_menu())


@bot.callback_query_handler(func=lambda callback: callback.data == 'calculator')
def main_start_calculate(callback):
    bot.delete_message(callback.message.chat.id, callback.message.message_id)
    bot.send_message(callback.message.chat.id, f'<b><tg-emoji emoji-id="5341715473882955310">⚙️</tg-emoji> Давайте пройдем быстрый опрос из 2-х вопросов, чтобы я мог выдать вам точный результат.</b> \n <b>1/2 Вопрос</b>\n\n'+
                    f'Сколько аккаунтов вы используйте/хотите использовать для кс фермы?\n',
                    parse_mode='html')
    bot.register_next_step_handler(callback.message, question_2)

def question_2 (message):
    accounts = message.text
    bot.delete_message(message.chat.id, message.message_id-1)
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, f'<b><tg-emoji emoji-id="5341715473882955310">⚙️</tg-emoji> 2/2 Вопрос</b>\n\n'+
                     f'Сколько компьютеров вы планируете использовать? \n(Если у вас уже есть компьютер, то напишите просто 0)', parse_mode='html')
    bot.register_next_step_handler(message, final_calculate, accounts=accounts)

def final_calculate (message, accounts):
    conn = sqlite3.connect('DadaBasaForBotCS2Farm.sql')
    cur = conn.cursor()
    computers = message.text
    cur.execute('SELECT settings_value FROM users WHERE id = ?', (message.chat.id,))
    bot.delete_message(message.chat.id, message.message_id-1)
    bot.delete_message(message.chat.id, message.message_id)
    valuta_settings = cur.fetchone()
    print(valuta_settings)
    bot.send_message(message.chat.id, REAL_final_calculate(accs=accounts, comps=computers, valuta_settings=valuta_settings), parse_mode='html')
    cur.close()
    conn.close()


@bot.callback_query_handler(func=lambda callback: callback.data == 'settings')
def main_settings_menu(callback):
    bot.delete_message(callback.message.chat.id, callback.message.message_id)
    bot.send_message(callback.message.chat.id, f'<b><tg-emoji emoji-id="5341715473882955310">⚙️</tg-emoji> Здесь вы можете выбрать валюту, в которой бот будет обрабатывать все подсчеты.</b>',
                    parse_mode='html',reply_markup=settings_menu())


@bot.callback_query_handler(func=lambda callback: callback.data in ['usd','rub','eur','nazad'])
def vubor(callback):
    conn = sqlite3.connect('DadaBasaForBotCS2Farm.sql')
    cur = conn.cursor()

    if callback.data == 'usd':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        cur.execute('UPDATE users SET settings_value = ? WHERE id = ?', 
                   ('usd', callback.message.chat.id))
        conn.commit()
        bot.send_message(callback.message.chat.id, f'<b><tg-emoji emoji-id="5341715473882955310">⚙️</tg-emoji> Здесь вы можете выбрать валюту, в которой бот будет обрабатывать все подсчеты.</b>',
                                    parse_mode='html',reply_markup=settings_menu())
                            
    elif callback.data == 'rub':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        cur.execute('UPDATE users SET settings_value = ? WHERE id = ?', 
                   ('rub', callback.message.chat.id))
        conn.commit()
        bot.send_message(callback.message.chat.id, f'<b><tg-emoji emoji-id="5341715473882955310">⚙️</tg-emoji> Здесь вы можете выбрать валюту, в которой бот будет обрабатывать все подсчеты.</b>',
                            parse_mode='html',reply_markup=settings_menu())
        
    elif callback.data == 'eur':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        cur.execute('UPDATE users SET settings_value = ? WHERE id = ?', 
           ('eur', callback.message.chat.id))
        conn.commit()
        bot.send_message(callback.message.chat.id, f'<b><tg-emoji emoji-id="5341715473882955310">⚙️</tg-emoji> Здесь вы можете выбрать валюту, в которой бот будет обрабатывать все подсчеты.</b>',
                            parse_mode='html',reply_markup=settings_menu())
        
    elif callback.data == 'nazad':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, f'<b>Вы находитесь в меню бота <tg-emoji emoji-id="5461117441612462242">🙂</tg-emoji></b>\n\n'+
                        f'Если что, этот бот умеет подсчитывать доходы и расходы с кс фермы. Внизу находятся кнопки, по которым вы можете двигаться',
                        parse_mode='html', reply_markup=main_menu())
        
    cur.close()
    conn.close()

bot.polling(non_stop=True)

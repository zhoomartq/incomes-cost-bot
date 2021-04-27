import telebot 
import csv

from telebot import types

bot = telebot.TeleBot(token)

entry = {}

inline_keyboard = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton('доход',callback_data='income')
btn2 = types.InlineKeyboardButton('рассход',callback_data='costs')
inline_keyboard.add(btn1,btn2)


@bot.message_handler(commands=['start'])
def start(message):
    chat_id=message.chat.id
    bot.send_message(chat_id,'welcom! make a choise', reply_markup=inline_keyboard)


@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    
    if c.data=='income':
        chat_id=c.message.chat.id
        income_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        k1 = types.KeyboardButton('job')
        k2 = types.KeyboardButton('freelance')
        k3 = types.KeyboardButton('another')
        income_keyboard.add(k1,k2,k3)
        msg = bot.send_message(chat_id,'Choose category',reply_markup=income_keyboard)
        bot.register_next_step_handler(msg,get_category_income)

    if c.data=='costs':
        chat_id=c.message.chat.id
        costs_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        k1 = types.KeyboardButton('food')
        k2 = types.KeyboardButton('clothes')
        k3 = types.KeyboardButton('entertainment')
        costs_keyboard.add(k1,k2,k3)
        msg = bot.send_message(chat_id,'Choose category',reply_markup=costs_keyboard)
        bot.register_next_step_handler(msg,get_category_costs)



def get_category_income(message):
    chat_id=message.chat.id
    entry.update({'category':message.text}) # == entry['category']=message.text
    msg=bot.send_message(chat_id,'indicate the amount')
    bot.register_next_step_handler(msg,get_sum_income)
def get_sum_income(message):
    chat_id=message.chat.id
    entry.update({'sum':message.text})

    file_name = 'income.csv'
    with open(file_name,'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow((entry['category'],entry['sum']))
    bot.send_message(chat_id,'I added your incomes',reply_markup=inline_keyboard)
    bot.send_sticker(chat_id,'CAACAgQAAxkBAAEBNoRghVy-ff-MV1qMT6eLYaZGBsHnEAACDgEAAmuuXgmEqpvy8hiGjR8E')



def get_category_costs(message):
    chat_id=message.chat.id
    entry.update({'category':message.text}) # == entry['category']=message.text
    msg=bot.send_message(chat_id,'indicate the amount')
    bot.register_next_step_handler(msg,get_sum_costs)
def get_sum_costs(message):
    chat_id=message.chat.id
    entry.update({'sum':message.text})   

    file_name = 'costs.csv'
    with open(file_name,'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow((entry['category'],entry['sum']))
    bot.send_message(chat_id,'I added your costs',reply_markup=inline_keyboard)
    bot.send_sticker(chat_id,'CAACAgQAAxkBAAEBNbhghUcnp1VxhzQJSRTH2oY3SY7wTAACPwEAAmuuXgm9uBqL7km33R8E')



bot.polling()
import json
import telebot

from telebot import types
from bot_data import token
from parser.parser import _main


bot = telebot.TeleBot(token)

def parse_json_data(json_data):
    for item in json_data:
        for key, description in item.items():
            yield (key, description)

@bot.message_handler(commands=['start'])
def start_message(message):
    mes = '''
        Привет! Данный бот позволяет посмотреть свежие хакатоны
и информацию о них. Здесь публикуются только актуальные ивенты! 
Для просмотра текущих хакатонов нажми на    
    '''
    bot.send_message(message.chat.id, mes)

@bot.message_handler(commands=['button'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but_get_data = types.KeyboardButton('Get data')
    markup.add(but_get_data),
    bot.send_message(message.chat.id,'Нажмите на кнопку',reply_markup=markup)

@bot.message_handler(content_types=['text'])
def reply_message(message):
    if message.text == 'Get data':
        try:
            _main()
            with open('json/saved_data.json', encoding='utf-8') as fd:
                list_events = json.load(fd)
                data_generator = parse_json_data(list_events)
                mes = ''

                for item in data_generator:
                    mes = mes + f'{item[0]}: {item[1]}'
                bot.send_message(message.chat.id, mes)
        except Exception as ex:
            print(ex)
            bot.send_message(message.chat.id, 
            "Oooops! We have a few problems...")
    else:
        bot.send_message(message.chat.id, "Incorrect command was inputed")

if __name__ == '__main__':
    bot.infinity_polling()

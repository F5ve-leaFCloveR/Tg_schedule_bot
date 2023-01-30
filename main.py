import telebot
from telebot import types
import configparser
import sys


config = configparser.ConfigParser()
try: # попытка чтения cfg файла с токеном
    config.read('token.cfg')
except FileNotFoundError:
    print('Error: token.cfg file not found')
    sys.exit(1)
except configparser.Error as e:
    print(f'Error parsing token.cfg file: {e}')
    sys.exit(1)

try: # получение самого токена из cfg файла
    token = config['Telegram']['token']
except KeyError:
    print('Error: "token" not found in token.cfg file')
    sys.exit(1)

bot = telebot.TeleBot(token) # создание экземпляра класса TeleBot

month = 0 # undefined behavior, нужно заменить глобальные переменные
days = []

@bot.message_handler(commands=['start']) # обработка команды /start
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) # создание кнопок
    btn1 = types.KeyboardButton('Make schedule')
    btn2 = types.KeyboardButton('Leave')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Choose command', reply_markup=markup) #ответ бота


@bot.message_handler(content_types=['text'])  # декоратор обработчик сообщений
def get_text_messages(message):

    if message.text == 'Make schedule': # создание расписания
        bot.send_message(message.chat.id, 'Choose month')
        bot.register_next_step_handler(message, register_month) # переход к следующему шагу

    elif message.text == 'Leave':
        global month, days
        month = 0
        days = []
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Goodbye', reply_markup=markup)

def register_month(message): # запись выбранного месяца
    global month
    month = message.text
    try: # проверка на правильный формат
        month = int(month) 
        if month not in range(1, 13):
            raise ValueError
    except ValueError:
        bot.send_message(message.from_user.id, 'Incorrect month')
        bot.register_next_step_handler(message, register_month)
    if isinstance(month, int) and month in range(1, 13):
        bot.send_message(message.chat.id, "Ok, choose days")
        bot.register_next_step_handler(message, register_days) # переход к записи дней

def register_days(message): # запись выбранных дней
    global days
    days = message.text.split()
    
    try: # проверка на правильный формат
        days = list(map(int, days))      
    except Exception:
        bot.send_message(message.from_user.id, 'Enter the dates in the correct format, for example: 1 2 3 4 5')
        bot.register_next_step_handler(message, register_days)
    if all(isinstance(i, int) for i in days):
        bot.send_message(message.chat.id, "Ok")

bot.polling(non_stop=True)
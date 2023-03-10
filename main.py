import telebot
from telebot import types
import configparser
import sys
import parser_sut
import Authorization
import asyncio

config = configparser.ConfigParser()
try: # попытка чтения cfg файла с токеном
    config.read('.gitignored/token.cfg')
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
async def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('View schedule'), types.KeyboardButton('Check in'), types.KeyboardButton('Leave')) # добавление кнопок в клавиатуру
    await bot.send_message(message.chat.id, 'Choose command', reply_markup=markup) #ответ бота


@bot.message_handler(content_types=['text'])  # декоратор обработчик сообщений
async def get_text_messages(message):

    if message.text == 'View schedule': # показать расписание
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) # создание кнопок
        schedule = parser_sut.parse()
        answer = f'{schedule["information"][0]}'
        await bot.send_message(message.chat.id, answer, reply_markup=markup)
        # bot.register_next_step_handler(message, register_month) # переход к следующему шагу

    elif message.text == 'Check in': # регистразия на занятии
        Authorization.authorization_lk()
        await bot.send_message(message.chat.id, 'Вы зарегистрированы на занятии')

    elif message.text == 'Leave':
        global month, days
        month = 0
        days = []
        markup = types.ReplyKeyboardRemove()
        await bot.send_message(message.chat.id, 'Goodbye', reply_markup=markup)
        
# def register_month(message): # запись выбранного месяца
#     global month
#     month = message.text
#     try: # проверка на правильный формат
#         month = int(month) 
#         if month not in range(1, 13):
#             raise ValueError
#     except ValueError:
#         bot.send_message(message.from_user.id, 'Incorrect month')
#         bot.register_next_step_handler(message, register_month)
#     if isinstance(month, int) and month in range(1, 13):
#         bot.send_message(message.chat.id, "Ok, choose days")
#         bot.register_next_step_handler(message, register_days) # переход к записи дней

# def register_days(message): # запись выбранных дней
#     global days
#     days = message.text.split()
    
#     try: # проверка на правильный формат
#         days = list(map(int, days))
#     except Exception:
#         bot.send_message(message.from_user.id, 'Enter the dates in the correct format, for example: 1 2 3 4 5')
#         bot.register_next_step_handler(message, register_days)
#     if all(isinstance(i, int) for i in days):
#         bot.send_message(message.chat.id, "Ok")

async def main():
    await bot.infinity_polling()

if __name__ == '__main__':
    asyncio.run(main())
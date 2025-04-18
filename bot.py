import logging
import datetime
from telebot import TeleBot, types
import telebot # библиотека telebot
from config import token # импорт токена

bot = telebot.TeleBot(token) 

# Настройки логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом.")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message: #проверка на то, что эта команда была вызвана в ответ на сообщение 
        chat_id = message.chat.id # сохранение id чата
         # сохранение id и статуса пользователя, отправившего сообщение
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
         # проверка пользователя
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id) # пользователь с user_id будет забанен в чате с chat_id
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")

# Хэндлер для всех сообщений
@bot.message_handler(func=lambda message: True)
def check_message(message: types.Message):
    # Проверяем наличие "https://" в сообщении
    if "https://" in message.text:
        try:
            # Сохраняем информацию о пользователе
            user_info = {
                'username': message.from_user.username,
                'first_name': message.from_user.first_name,
                'last_name': message.from_user.last_name,
                'user_id': message.from_user.id,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Баним пользователя
            bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=message.from_user.id,
                permissions=types.ChatPermissions(False)
            )
            
            # Уведомляем пользователя
            bot.reply_to(message, "Вы были забанены за отправку ссылки!")
            
            # Записываем информацию в лог
            logging.info(f"Пользователь забанен: {user_info}")
            
        except Exception as e:
            logging.error(f"Ошибка при бане пользователя: {e}")
            bot.reply_to(message, "Произошла ошибка при обработке сообщения")


bot.infinity_polling(none_stop=True)


import sqlite3
import telebot

bot = telebot.TeleBot('TOKEN')

@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('bazadanix.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(50), pass VARCHAR(50), email VARCHAR(50), phone VARCHAR(20), location VARCHAR(50))')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Привет, тут храняться твой даные логин и пароль от интернета.' 
    '\n Telegram @voron4px'
    '\n')
    
    bot.send_message(message.chat.id, 'Введите логин')
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    name = message.text.strip()

    if not name:
        bot.send_message(message.chat.id, 'Логин не может быть пустым')
        return

    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, user_pass, name)

def user_pass(message, name):
    password = message.text.strip()

    if not password:
        bot.send_message(message.chat.id, 'Пароль не может быть пустым')
        return
    
    bot.send_message(message.chat.id, 'Введите электронную почту')
    bot.register_next_step_handler(message, user_email, name, password)

def user_email(message, name, password):
    email = message.text.strip()

    if not email:
        bot.send_message(message.chat.id, 'Электронная почта не может быть пустой')
        return
    
    bot.send_message(message.chat.id, 'Введите номер телефона')
    bot.register_next_step_handler(message, user_phone, name, password, email)

def user_phone(message, name, password, email):
    phone = message.text.strip()

    if not phone:
        bot.send_message(message.chat.id, 'Номер телефона не может быть пустым')
        return
    
    bot.send_message(message.chat.id, 'Название аккаунта')
    bot.register_next_step_handler(message, user_location, name, password, email, phone)

def user_location(message, name, password, email, phone):
    location = message.text.strip()

    if not location:
        bot.send_message(message.chat.id, 'Название аккаунта не может быть пустым')
        return

    conn = sqlite3.connect('bazadanix.sql')
    cur = conn.cursor()

    cur.execute('INSERT INTO users (name, pass, email, phone, location) VALUES (?, ?, ?, ?, ?)', (name, password, email, phone, location))
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='users'))
    bot.send_message(message.chat.id, 'Регистрация успешна!', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'users':
        conn = sqlite3.connect('bazadanix.sql')
        cur = conn.cursor()

        cur.execute('SELECT * FROM users')
        users = cur.fetchall()

        info = ''
        for el in users:
            info += f'логин: {el[1]}, пароль: {el[2]}, электронная почта: {el[3]}, номер телефона: {el[4]}, название аккаунта: {el[5]}\n'

        cur.close()
        conn.close()

        bot.send_message(call.message.chat.id, info)

bot.polling(none_stop=True)
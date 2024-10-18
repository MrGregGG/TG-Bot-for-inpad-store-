from telebot import TeleBot, types

TOKEN = '7225423787:AAHnZneKoZYzmPGnjH7VmB1DKY6Ykg-PtHg'
bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    answer = f'<b>Привет, пиши /help!</b> <u>{message.from_user.first_name}</u> <u>{message.from_user.last_name}</u>'
    bot.send_message(message.chat.id, text=answer, parse_mode='html')

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def send_help(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    item1 = types.KeyboardButton('Хочу задать вопрос касаемо работы плагина')
    item2 = types.KeyboardButton('Хочу сообщить об ошибке')
    item3 = types.KeyboardButton('Нужна помощь при установке/активации')
    markup.add(item1, item2, item3)
    
    bot.send_message(message.chat.id, "Выберите пункт, по которому вам нужна помощь", reply_markup=markup)

# Обработчик выбора пункта из меню помощи
@bot.message_handler(func=lambda message: message.text in ['Хочу задать вопрос касаемо работы плагина', 'Хочу сообщить об ошибке', 'Нужна помощь при установке/активации'])
def handle_help_selection(message):
    if message.text == 'Нужна помощь при установке/активации':
        send_install_help(message)
    else:
        send_plugin_help(message)

def send_plugin_help(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    buttons = ['Концепция', 'Архитектура', 'Конструктив', 'ОВ и ВК', 'Боксы и отверстия', 'Общие', 'Renga']
    for button in buttons:
        markup.add(types.KeyboardButton(button))
    
    bot.send_message(message.chat.id, "Выберите из какой категории плагин, с которым вам нужна помощь", reply_markup=markup)

def send_install_help(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    buttons = ['Ошибка при установке сборки', 'Не получается зарегистрироваться', 'Не получается ввести ключ активации']
    for button in buttons:
        markup.add(types.KeyboardButton(button))
    
    bot.send_message(message.chat.id, "Выберите категорию, по которой вам нужна помощь", reply_markup=markup)

# Обработчик выбора категории для установки/активации
@bot.message_handler(func=lambda message: message.text in ['Ошибка при установке сборки', 'Не получается зарегистрироваться', 'Не получается ввести ключ активации'])
def handle_install_help_selection(message):
    send_revit_version_request(message)

def send_revit_version_request(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    buttons = ['Revit 2019', 'Revit 2020', 'Revit 2021', 'Revit 2022', 'Revit 2023', 'Revit 2024', 'Revit 2025']
    for button in buttons:
        markup.add(types.KeyboardButton(button))
    
    bot.send_message(message.chat.id, "Выберите версию Revit, в котором запускали плагин", reply_markup=markup)

# Обработчик выбора версии Revit
@bot.message_handler(func=lambda message: message.text in ['Revit 2019', 'Revit 2020', 'Revit 2021', 'Revit 2022', 'Revit 2023', 'Revit 2024', 'Revit 2025'])
def handle_revit_version(message):
    bot.send_message(message.chat.id, "Введите, пожалуйста, ваш лицензионный ключ, который вы использовали")
    bot.register_next_step_handler(message, handle_license_key)

def handle_license_key(message):
    license_key = message.text
    bot.send_message(message.chat.id, "Напишите, пожалуйста, номер сборки, которую вы установили")
    bot.register_next_step_handler(message, handle_build_number, license_key)

def handle_build_number(message, license_key):
    build_number = message.text
    bot.send_message(message.chat.id, "Отправьте, пожалуйста, скриншот ошибки и опишите вашу проблему")
    bot.register_next_step_handler(message, handle_error_screenshot, license_key, build_number)

def handle_error_screenshot(message, license_key, build_number):
    if message.photo:
        photo_id = message.photo[-1].file_id
        problem_description = message.caption
        bot.send_message(message.chat.id, "Данная ошибка была передана отделу разработок, в ближайшее время с вами свяжется специалист")
        # Здесь вы можете добавить код для передачи данных отделу разработок
    else:
        bot.send_message(message.chat.id, "Пожалуйста, отправьте скриншот ошибки и опишите вашу проблему")

if __name__ == '__main__':
    bot.polling(non_stop=True)

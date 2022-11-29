import logging
from aiogram import Bot, Dispatcher, executor, types
import buttons as but
from db import Database
from config import TOKEN
import random
import string


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db = Database('database.db')

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if (not db.user_exists(message.from_user.id)):
        db.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, "Для работы с ботом нужно авторизоваться :)\nУкажите электронную почту с доменом blanc.ru\nВам придет код, отправьте его в чат:")
    elif db.get_email(message.from_user.id) == "blank":
        await bot.send_message(message.from_user.id, "Для работы с ботом нужно авторизоваться :)\nУкажите электронную почту с доменом blanc.ru\nВам придет код, отправьте его в чат:")
    else:
        if db.get_passin(message.from_user.id) == "setpassin": #будет реализовываться в случае изменения логики хранения set_email (сохранения после 'Выйти')
            await bot.send_message(message.from_user.id, "Для работы с ботом нужно авторизоваться :)\nУкажите код, который мы отправили вам на электронную почту.\nЕсли вышли из системы, забыли или утеряли письмо с паролем, можем отправить повторно👇🏻", reply_markup=but.sendpass)    
        else:
            if db.get_passin(message.from_user.id) != "setpassin":
                await bot.send_message(message.from_user.id, "Тут ты можешь посмотреть свой email или разлогиниться", reply_markup=but.mainMenu)


@dp.message_handler()
async def bot_message(message: types.Message):
    if message.chat.type == 'private':
        if message.text == 'Моя почта':
            if db.get_email(message.from_user.id) == "blank":
                await bot.send_message(message.from_user.id, "Так не пойдет :)\nСначала нужно авторизоваться!\nУкажите электронную почту с доменом blanc.ru\nВам придет код для отправки в чат:")
            elif db.get_passin(message.from_user.id) == "setpassin": #будет реализовываться в случае изменения логики хранения set_email (сохранения после 'Выйти')
                await bot.send_message(message.from_user.id, "Для работы с ботом нужно авторизоваться :)\nУкажите код, который мы отправили вам на электронную почту.\nЕсли вышли из системы, забыли или утеряли письмо с паролем, можем отправить повторно👇🏻", reply_markup=but.sendpass)
            else:
                user_emai = "Ваша электронная почта: " + "\n" + db.get_email(message.from_user.id)
                await bot.send_message(message.from_user.id, user_emai)
        elif message.text == 'Войти':
            if (not db.user_exists(message.from_user.id)):
                db.add_user(message.from_user.id)
                await bot.send_message(message.from_user.id, "Для работы с ботом нужно авторизоваться :)\nУкажите электронную почту с доменом blanc.ru\nВам придет код, отправьте его в чат:")
            elif db.get_email(message.from_user.id) == "blank":
                await bot.send_message(message.from_user.id, "Для работы с ботом нужно авторизоваться :)\nУкажите электронную почту с доменом blanc.ru\nВам придет код, отправьте его в чат:")
            else:
                if db.get_passin(message.from_user.id) == "setpassin": #будет реализовываться в случае изменения логики хранения set_email (сохранения после 'Выйти')
                    await bot.send_message(message.from_user.id, "Для работы с ботом нужно авторизоваться :)\nУкажите код, который мы отправили вам на электронную почту.\nЕсли вышли из системы, забыли или утеряли письмо с паролем, можем отправить повторно👇🏻", reply_markup=but.sendpass)    
                else:
                    if db.get_passin(message.from_user.id) != "setpassin":
                        await bot.send_message(message.from_user.id, "Тут ты можешь посмотреть свой email или разлогиниться", reply_markup=but.mainMenu)
        elif message.text == 'Выйти':
            if db.get_email(message.from_user.id) == "blank":
                await bot.send_message(message.from_user.id, "Вы не в системе!\nСначала нужно авторизоваться!\nУкажите электронную почту с доменом blanc.ru \nВам придет код для отправки в чат:")
            elif db.get_passin(message.from_user.id) == "setpassin": #будет реализовываться в случае изменения логики хранения set_email (сохранения после 'Выйти')
                await bot.send_message(message.from_user.id, "Вы не в системе!\nДля работы с ботом нужно авторизоваться :)\nУкажите код, который мы отправили вам на электронную почту.\nЕсли вышли из системы, забыли или утеряли письмо с паролем, можем отправить повторно👇🏻", reply_markup=but.sendpass)
            else:
                db.set_logpass(message.from_user.id, "aaaaaa")
                db.set_passin(message.from_user.id, "setpassin")
                db.set_email(message.from_user.id, "blank")
                await bot.send_message(message.from_user.id, "Ждем вас снова :)", reply_markup=but.startMenu)
        elif db.get_email(message.from_user.id) == "blank":
            if(len(message.text) > 255):
                await bot.send_message(message.from_user.id, "Электронная почта не должна превышать 255 символов")
            elif not '@blanc.ru' in message.text:
                await bot.send_message(message.from_user.id, "Электронная почта должна содержать домен blanc.ru")
            #elif (r'[^a-zA-Zа-яА-Я]') in message.text):
                    #await bot.send_message(message.from_user.id, "Электронная почта должна содержать латинские буквы \nНапример: blanc@blanc.ru")
            else:
                db.set_email(message.from_user.id, message.text)
                db.set_logpass(message.from_user.id, random_pass(6))#random.randint(100001,999999))
                user_logpass = "Ваш код 👉🏻 " + db.get_logpass(message.from_user.id) + " 👈🏻\nВведите его в чат бота:"
                await bot.send_message(message.from_user.id, user_logpass)
        elif db.get_logpass(message.from_user.id) != "aaaaaa":
            if (len(message.text) > 6):
                await bot.send_message(message.from_user.id, "Пароль содержит 6 символов, перепроверьте :)")
            elif db.get_logpass(message.from_user.id) != message.text:
                await bot.send_message(message.from_user.id, "Пароль не верный, перепроверьте :)")
            else:
                if db.get_logpass(message.from_user.id) == message.text:
                    db.set_passin(message.from_user.id, message.text)
                    await bot.send_message(message.from_user.id, "Регистрация прошла успешно", reply_markup=but.mainMenu)
        else:
            await bot.send_message(message.from_user.id, "Я пока не могу поддержать разговор :) \nДля вызова меню используй команду /start")
        
        
        #db.set_compare_pass(message.from_user.id, message.text):
            #if db.get_logpass(message.from_user.id) == db.get_compare_pass(message.from_user.id):
               
def random_pass(length):
    letters = string.ascii_lowercase
    rand_pass = ''.join(random.choice(letters) for i in range(length))
    return rand_pass

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
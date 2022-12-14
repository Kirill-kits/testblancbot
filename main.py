import logging
from aiogram import Bot, Dispatcher, executor, types
import buttons as but
from db import Database
from config import TOKEN
from config import EMAIL_PASSWORD
import random
import string
import smtplib
from email.mime.text import MIMEText


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
        if db.get_passin(message.from_user.id) == "setpassin": #будет реализовываться в случае изменения логики хранения email (сохранения после 'Выйти')
            await bot.send_message(message.from_user.id, "Для работы с ботом нужно авторизоваться :)\nУкажите код, который мы отправили вам на электронную почту.\n\nЕсли вышли из системы, забыли или утеряли письмо с паролем, отправим еще раз :)\n\nДля этого нажмите кнопку 'Отправить код повторно' 👇🏻", reply_markup=but.sendpass)    
        else:
            if db.get_passin(message.from_user.id) != "setpassin":
                await bot.send_message(message.from_user.id, "Тут ты можешь посмотреть свой email или разлогиниться 👇🏻", reply_markup=but.mainMenu)


@dp.message_handler()
async def bot_message(message: types.Message):
    if message.chat.type == 'private':
        if message.text == 'Моя почта':
            if db.get_email(message.from_user.id) == "blank":
                await bot.send_message(message.from_user.id, "Так не пойдет :)\nСначала нужно авторизоваться!\nУкажите электронную почту с доменом blanc.ru\nВам придет код для отправки в чат:")
            elif db.get_passin(message.from_user.id) == "setpassin": #будет реализовываться в случае изменения логики хранения email (сохранения после 'Выйти')
                await bot.send_message(message.from_user.id, "Для работы с ботом нужно авторизоваться :)\nУкажите код, который мы отправили вам на электронную почту.\n\nЕсли вышли из системы, забыли или утеряли письмо с паролем, отправим еще раз :)\n\nДля этого нажмите кнопку 'Отправить код повторно' 👇🏻", reply_markup=but.sendpass)
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
                if db.get_passin(message.from_user.id) == "setpassin": #будет реализовываться в случае изменения логики хранения email (сохранения после 'Выйти')
                    await bot.send_message(message.from_user.id, "Для работы с ботом нужно авторизоваться :)\nУкажите код, который мы отправили вам на электронную почту.\n\nЕсли вышли из системы, забыли или утеряли письмо с паролем, отправим еще раз :)\n\nДля этого нажмите кнопку 'Отправить код повторно' 👇🏻", reply_markup=but.sendpass)    
                else:
                    if db.get_passin(message.from_user.id) != "setpassin":
                        await bot.send_message(message.from_user.id, "Ты можешь посмотреть свой email или разлогиниться", reply_markup=but.mainMenu)
        
        elif message.text == 'Выйти':
            if db.get_email(message.from_user.id) == "blank":
                await bot.send_message(message.from_user.id, "Вы не в системе!\nСначала нужно авторизоваться!\nУкажите электронную почту с доменом blanc.ru \nВам придет код для отправки в чат:")
            elif db.get_passin(message.from_user.id) == "setpassin": #будет реализовываться в случае изменения логики хранения email (сохранения после 'Выйти')
                await bot.send_message(message.from_user.id, "Вы не в системе!\nДля работы с ботом нужно авторизоваться :)\nУкажите код, который мы отправили вам на электронную почту.\nЕсли вышли из системы, забыли или утеряли письмо с паролем, воспользуйтесь кнопкой для повторной отправки👇🏻", reply_markup=but.sendpass)
            else:
                db.set_logpass(message.from_user.id, "aaaaaaa")
                db.set_passin(message.from_user.id, "setpassin")
                db.set_email(message.from_user.id, "blank")
                await bot.send_message(message.from_user.id, "Ждем вас снова :)", reply_markup=but.startMenu)
        
        elif message.text == 'Отправить код повторно':
            if db.get_email(message.from_user.id) == "blank":
                await bot.send_message(message.from_user.id, "Для работы с ботом нужно авторизоваться :)\nУкажите электронную почту с доменом blanc.ru\nВам придет код, отправьте его в чат:")
            else:
                if db.get_passin(message.from_user.id) != "setpassin":
                    await bot.send_message(message.from_user.id, "Вы в системе, отправка кода не требуется :)")
                else:
                    db.set_logpass(message.from_user.id, random_pass(6))#or random.randint(100001,999999))
                    user_logpass = "Ваш код 👉🏻 " + db.get_logpass(message.from_user.id) + " 👈🏻\nВведите его в чат бота:"
                    await bot.send_message(message.from_user.id, user_logpass, reply_markup=but.emailmenu)
            
        elif db.get_email(message.from_user.id) == "blank":
            if(len(message.text) > 255):
                await bot.send_message(message.from_user.id, "Электронная почта не должна превышать 255 символов")
            elif not '@blanc.ru' in message.text:
                await bot.send_message(message.from_user.id, "Электронная почта должна содержать домен blanc.ru")
            #elif (r'[^a-zA-Zа-яА-Я]') in message.text):
                #await bot.send_message(message.from_user.id, "Электронная почта должна содержать латинские буквы \nНапример: blanc@blanc.ru")
            else:
                index = message.text.find("@")
                if index == -1:
                    print('Электронная почта указывается через "@", пример:\nblanc.ru')
                else:
                    if message.text == message.text[0:index+1] + "blanc.ru":              
                        db.set_email(message.from_user.id, message.text)
                        db.set_email_saved(message.from_user.id, message.text)
                        db.set_logpass(message.from_user.id, random_pass(6))#or random.randint(100001,999999))
                        user_logpass = "Код отправлен на электронную почту:\n" + db.get_email(message.from_user.id) + "\n\nВаш код 👉🏻 " + db.get_logpass(message.from_user.id) + " 👈🏻\nВведите его в чат бота для авторизации."
                        user_logpass_email = "Ваш код 👉🏻 " + db.get_logpass(message.from_user.id) + " 👈🏻\nВведите его в чат бота https://t.me/test1blanc_bot для авторизации."
                        print(send_mail(sendmessage=user_logpass_email, receiver=db.get_email(message.from_user.id)))
                        await bot.send_message(message.from_user.id, user_logpass, reply_markup=but.emailmenu)
                    else:
                        await bot.send_message(message.from_user.id, "Электронная почта указана некорректно, проверьте на опечатки, адрес должен содержать домен blanc.ru")
        elif db.get_passin(message.from_user.id) == "setpassin":
            if (len(message.text) > 6):
                await bot.send_message(message.from_user.id, "Пароль содержит 6 символов, перепроверьте :)\nЕсли забыли или утеряли письмо с паролем, воспользуйтесь кнопкой для повторной отправки👇🏻")
            elif db.get_logpass(message.from_user.id) != message.text and db.get_passin(message.from_user.id) == "setpassin":
                await bot.send_message(message.from_user.id, "Пароль не верный, перепроверьте :)\nЕсли забыли или утеряли письмо с паролем, воспользуйтесь кнопкой для повторной отправки👇🏻")
            else:
                if db.get_logpass(message.from_user.id) == message.text and db.get_passin(message.from_user.id) == "setpassin":
                    db.set_passin(message.from_user.id, message.text)
                    await bot.send_message(message.from_user.id, "Регистрация прошла успешно", reply_markup=but.mainMenu)
        else:
            await bot.send_message(message.from_user.id, "Я пока не могу поддержать разговор :) \nДля вызова меню используй команду /start")
            
              

def send_mail(sendmessage, receiver):
    sender = "blancpbt@gmail.com"
    password = EMAIL_PASSWORD

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(sendmessage)
        msg["Subject"] = "Пароль для входа в бота"
        server.sendmail(sender, receiver, msg.as_string())
        return "message send successfully"
    except Exception as _ex:
        return f"{_ex}\nChek your login or password"

def random_pass(length):
    letters = string.ascii_lowercase
    rand_pass = ''.join(random.choice(letters) for i in range(length))
    return rand_pass

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

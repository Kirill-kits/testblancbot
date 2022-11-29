from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

btnemail = KeyboardButton ("Моя почта")
btnout = KeyboardButton('Выйти')

mainMenu = ReplyKeyboardMarkup(resize_keyboard = True)
mainMenu.add(btnemail, btnout)


btnstart = KeyboardButton('Войти')
startMenu = ReplyKeyboardMarkup(resize_keyboard = True)
startMenu.add(btnstart)


sendpass = InlineKeyboardButton("Отправить код повторно", callback_data='user_logpass')
inline_markup = InlineKeyboardMarkup(row_width=1)
inline_markup.insert(sendpass)
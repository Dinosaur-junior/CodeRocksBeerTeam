from telebot import types


def create_keyboard(btn_lines):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for line in btn_lines:
        btn_arr = []
        for name in line:
            btn_arr.append(types.KeyboardButton(text=name))
        keyboard.add(*btn_arr)
    return keyboard


def create_inline_keyboard(btn_lines):
    keyboard = types.InlineKeyboardMarkup()
    for line in btn_lines:
        btn_arr = []
        for name, data in line:
            btn_arr.append(types.InlineKeyboardButton(text=name, callback_data=data))
        keyboard.add(*btn_arr)
    return keyboard


def none():
    return types.ReplyKeyboardRemove()


def menu():
    return create_keyboard([
        ['Ввести код'],
        ['Связаться с админом'],
        ['Посмотреть информацию о компании']
    ])


def menu_reg():
    return create_keyboard([
        ['Частые вопросы', 'Мои коллеги'],
        ['Мои обязанности'],
        ['Пройти обучение'],
        ['Связаться с админом'],
        ['Информация о компании'],
        ['Карта офиса'],
        ['Мой профиль']
    ])


def back():
    return create_keyboard([
        ['<< Назад']
    ])
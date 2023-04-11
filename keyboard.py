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


def start_btn():
    return create_keyboard([
        ['СТАРТ'],
        ['<< Назад']
    ])


def cmp_info_game_1():
    return create_inline_keyboard([
        [('1 л', 'cmp_info_game|1|False'), ('100 л', 'cmp_info_game|1|False'), ('40 тонн', 'cmp_info_game|1|True')],
        [('Завершить игру', 'cmp_info_game|end')]
    ])


def cmp_info_game_1_answer():
    return create_inline_keyboard([
        [('❌ 1 л', 'cmp_info_game|1|'), ('❌ 100 л', 'cmp_info_game|1|'), ('✅ 40 тонн', 'cmp_info_game|1|')],
        [('Далее >>', 'cmp_info_game|1|next')],
        [('Завершить игру', 'cmp_info_game|end')]
    ])


def cmp_info_game_2():
    return create_inline_keyboard([
        [('1', 'cmp_info_game|2|True'), ('2', 'cmp_info_game|2|False')],
        [('Завершить игру', 'cmp_info_game|end')]
    ])


def cmp_info_game_2_answer():
    return create_inline_keyboard([
        [('✅ 1', 'cmp_info_game|2|'), ('❌ 2', 'cmp_info_game|2|')],
        [('Далее >>', 'cmp_info_game|2|next')],
        [('Завершить игру', 'cmp_info_game|end')]
    ])


def cmp_info_game_3():
    return create_inline_keyboard([
        [('1', 'cmp_info_game|3|True'), ('2', 'cmp_info_game|3|False')],
        [('Завершить игру', 'cmp_info_game|end')]
    ])


def cmp_info_game_3_answer():
    return create_inline_keyboard([
        [('✅ 1', 'cmp_info_game|3|'), ('❌ 2', 'cmp_info_game|3|')],
        [('Завершить игру', 'cmp_info_game|end')]
    ])
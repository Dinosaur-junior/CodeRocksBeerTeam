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
        ['🐈 Ввести код'],
        ['📲 Связаться с админом'],
        ['ℹ️ Посмотреть информацию о компании']
    ])


def menu_reg():
    return create_keyboard([
        ['❓ Частые вопросы', '👨🏿‍💻 Мои коллеги'],
        ['❗️ Мои обязанности', '📚 Пройти обучение'],
        ['ℹ️ Информация о компании', '🗺 Карта офиса'],
        ['📲 Связаться с админом', '👤 Мой профиль']
    ])


def profile():
    return create_keyboard([
        ['🍺 Запросить выдачу пива', '🖼 Моя карточка'],
        ['<< Назад']
    ])


def back():
    return create_keyboard([
        ['<< Назад']
    ])


def start_btn():
    return create_keyboard([
        ['▶️ СТАРТ'],
        ['<< Назад']
    ])


# --------------------------------------------------------------------
# Training

def training_again():
    return create_keyboard([
        ['Пройти еще раз'],
        ['<< Назад']
    ])


def duties_training(id, answers):
    answers = [[(answ_inc, f'duties_training|{id}|False')] for answ_inc in answers['incorrect']] + [
        [(answers['correct'], f'duties_training|{id}|True')]]
    return create_inline_keyboard(answers)


def duties_training_answ(id, answers, max_duties_cnt):
    if id + 1 == max_duties_cnt:
        return create_inline_keyboard(
            [[('❌' + answ_inc, f'duties_training|{id}|')] for answ_inc in answers['incorrect']] +
            [[('✅' + answers['correct'], f'duties_training|{id}|')]] +
            [[('🏁 Завершить обучение', f'duties_training|{id}|end')]]
        )
    else:
        return create_inline_keyboard(
            [[('❌' + answ_inc, f'duties_training|{id}|')] for answ_inc in answers['incorrect']] +
            [[('✅' + answers['correct'], f'duties_training|{id}|')]] +
            [[('Далее >>', f'duties_training|{id}|next')]]
        )


# --------------------------------------------------------------------

def card_setup():
    return create_inline_keyboard([
        [('🖊 Изменить описание', 'card_setup|about'), ('📷 Изменить фото', 'card_setup|photo')]
    ])


def cmp_info_game_1():
    return create_inline_keyboard([
        [('1 л', 'cmp_info_game|1|False'), ('100 л', 'cmp_info_game|1|False'), ('40 тонн', 'cmp_info_game|1|True')],
        [('🏁 Завершить игру', 'cmp_info_game|end')]
    ])


def cmp_info_game_1_answer():
    return create_inline_keyboard([
        [('❌ 1 л', 'cmp_info_game|1|'), ('❌ 100 л', 'cmp_info_game|1|'), ('✅ 40 тонн', 'cmp_info_game|1|')],
        [('Далее >>', 'cmp_info_game|1|next')],
        [('🏁 Завершить игру', 'cmp_info_game|end')]
    ])


def cmp_info_game_2():
    return create_inline_keyboard([
        [('15%', 'cmp_info_game|2|False'), ('40%', 'cmp_info_game|2|False'), ('95%', 'cmp_info_game|2|True')],
        [('🏁 Завершить игру', 'cmp_info_game|end')]
    ])


def cmp_info_game_2_answer():
    return create_inline_keyboard([
        [('❌ 15%', 'cmp_info_game|2|'), ('❌ 40%', 'cmp_info_game|2|'), ('✅ 95%', 'cmp_info_game|2|')],
        [('Далее >>', 'cmp_info_game|2|next')],
        [('🏁 Завершить игру', 'cmp_info_game|end')]
    ])


def cmp_info_game_3():
    return create_inline_keyboard([
        [('Вишневое пиво', 'cmp_info_game|3|True'), ('Светлое пиво', 'cmp_info_game|3|True'),
         ('Темное пиво', 'cmp_info_game|3|True')],
        [('🏁 Завершить игру', 'cmp_info_game|end')]
    ])


def cmp_info_game_3_answer():
    return create_inline_keyboard([
        [('✅ Вишневое пиво', 'cmp_info_game|3|'), ('✅ Светлое пиво', 'cmp_info_game|3|'),
         ('✅ Темное пиво', 'cmp_info_game|3|')],
        [('🏁 Завершить игру', 'cmp_info_game|end')]
    ])


# --------------------------------------------------------------------

def often_questions(questions):
    return create_inline_keyboard(
        [[(f'{question.question}', f'often_questions|{question.id}')] for question in questions]
    )


# --------------------------------------------------------------------

def nav_bar(id, max_user_cnt):
    return create_inline_keyboard([
        [('<', f'nav_bar|{id}|back'), (f'{id + 1}/{max_user_cnt}', f'nav_bar|{id}|'), ('>', f'nav_bar|{id}|next')]
    ])

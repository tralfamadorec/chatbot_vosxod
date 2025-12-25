"""Telegram-бот для выполнения учебных заданий по обработке массивов

Основной модуль, реализующий взаимодействие с пользователем через Telegram API
Использует конечные автоматы (FSM) для управления состояниями каждого задания

Функционал:
- Задание 1: Обработка двух массивов
- Задание 5: Подмассивы с заданной суммой
- Задание 8: Общие числа с перевёрнутыми

Архитектура:
- Нисходящее проектирование: от главного файла к модулям задач
- FSM через словарь состояний (согласно лекции "Автоматное программирование")
- Многопользовательская поддержка через сессии (user_id -> FSM)
- Текстовые кнопки вместо цифрового ввода для удобства пользователя
"""

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from tasks.task1 import Task1FSM
from tasks.task5 import Task5FSM
from tasks.task8 import Task8FSM
from tasks.messages import Messages
from config import TOKEN

# инициализация Telegram-бота
bot = telebot.TeleBot(TOKEN)

# хранилище сессий пользователей: user_id -> {"state": str, "fsm": FSM}
sessions = {}


def get_main_keyboard():
    """Создаёт клавиатуру главного меню

    Returns:
        ReplyKeyboardMarkup: Клавиатура с выбором заданий
    """
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    kb.row("Задание 1", "Задание 5", "Задание 8")
    kb.row("Все задания")
    return kb


def get_task1_actions():
    """Создаёт клавиатуру действий для задания 1

    Returns:
        ReplyKeyboardMarkup: Клавиатура с действиями задания 1
    """
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    kb.row("Ввести вручную", "Сгенерировать")
    kb.row("Выполнить", "Результат")
    kb.row("Назад")
    return kb


def get_task5_actions():
    """Создаёт клавиатуру действий для задания 5

    Returns:
        ReplyKeyboardMarkup: Клавиатура с действиями задания 5
    """
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    kb.row("Ввести вручную", "Сгенерировать")
    kb.row("Выполнить", "Результат")
    kb.row("Назад")
    return kb


def get_task8_actions():
    """Создаёт клавиатуру действий для задания 8

    Returns:
        ReplyKeyboardMarkup: Клавиатура с действиями задания 8
    """
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    kb.row("Ввести вручную", "Сгенерировать")
    kb.row("Выполнить", "Результат")
    kb.row("Назад")
    return kb


@bot.message_handler(commands=['start'])
def start(message):
    """Обрабатывает команду /start

    Инициализирует сессию пользователя и отправляет приветственное сообщение с клавиатурой главного меню

    Args:
        message (telebot.types.Message): Входящее сообщение от пользователя
    """
    user_id = message.from_user.id
    sessions[user_id] = {"state": "main_menu", "fsm": None}
    bot.send_message(
        user_id,
        Messages.GREETING,
        reply_markup=get_main_keyboard()
    )


@bot.message_handler(func=lambda m: True)
def handle_message(message):
    """Обрабатывает все текстовые сообщения от пользователя

    Управляет навигацией между заданиями и передаёт управление соответствующему FSM для обработки действий

    Args:
        message (telebot.types.Message): Входящее текстовое сообщение
    """
    user_id = message.from_user.id
    text = message.text.strip()

    # инициализация сессии для новых пользователей
    if user_id not in sessions:
        sessions[user_id] = {"state": "main_menu", "fsm": None}
        bot.send_message(user_id, Messages.MAIN_MENU_PROMPT, reply_markup=get_main_keyboard())
        return

    session = sessions[user_id]

    # обработка главного меню
    if session["state"] == "main_menu":
        if text == "Задание 1":
            fsm = Task1FSM()
            sessions[user_id] = {"state": "task1", "fsm": fsm}
            bot.send_message(user_id, Messages.TASK1_DESCRIPTION)
            bot.send_message(user_id, Messages.ACTION_PROMPT, reply_markup=get_task1_actions())

        elif text == "Задание 5":
            fsm = Task5FSM()
            sessions[user_id] = {"state": "task5", "fsm": fsm}
            bot.send_message(user_id, Messages.TASK5_DESCRIPTION)
            bot.send_message(user_id, Messages.ACTION_PROMPT, reply_markup=get_task5_actions())

        elif text == "Задание 8":
            fsm = Task8FSM()
            sessions[user_id] = {"state": "task8", "fsm": fsm}
            bot.send_message(user_id, Messages.TASK8_DESCRIPTION)
            bot.send_message(user_id, Messages.ACTION_PROMPT, reply_markup=get_task8_actions())

        elif text == "Все задания":
            bot.send_message(user_id, Messages.ALL_TASKS_DESCRIPTION)
            bot.send_message(user_id, Messages.MAIN_MENU_PROMPT, reply_markup=get_main_keyboard())

        else:
            bot.send_message(user_id, Messages.INVALID_MAIN_CHOICE, reply_markup=get_main_keyboard())

    # обработка внутри задания
    else:
        fsm = session["fsm"]
        try:
            response = fsm.handle(text)
            if response == "exit":
                sessions[user_id] = {"state": "main_menu", "fsm": None}
                bot.send_message(user_id, Messages.BACK_TO_MAIN, reply_markup=get_main_keyboard())
            else:
                # отправка ответа от FSM
                bot.send_message(user_id, response)

                # показ клавиатуры действий только если FSM вернулся в меню
                current_state = fsm.state
                if current_state == "menu":
                    if session["state"] == "task1":
                        bot.send_message(user_id, Messages.NEXT_ACTION_PROMPT, reply_markup=get_task1_actions())
                    elif session["state"] == "task5":
                        bot.send_message(user_id, Messages.NEXT_ACTION_PROMPT, reply_markup=get_task5_actions())
                    elif session["state"] == "task8":
                        bot.send_message(user_id, Messages.NEXT_ACTION_PROMPT, reply_markup=get_task8_actions())
                # если FSM ожидает ввод (например, "input_random"), клавиатура не показывается

        except Exception as e:
            bot.send_message(user_id, f"{Messages.INVALID_INPUT}: {e}")
            # повторное отображение клавиатуры при ошибках
            if session["state"] == "task1":
                bot.send_message(user_id, Messages.ACTION_PROMPT, reply_markup=get_task1_actions())
            elif session["state"] == "task5":
                bot.send_message(user_id, Messages.ACTION_PROMPT, reply_markup=get_task5_actions())
            elif session["state"] == "task8":
                bot.send_message(user_id, Messages.ACTION_PROMPT, reply_markup=get_task8_actions())
            return


if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)
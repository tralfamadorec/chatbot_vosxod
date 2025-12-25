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
import logging
import sys
import time
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.apihelper import ApiTelegramException
from tasks.task1 import Task1FSM
from tasks.task5 import Task5FSM
from tasks.task8 import Task8FSM
from tasks.messages import Messages
from config import TOKEN


# безопасная отправка "печатает..."
def safe_send_chat_action(user_id, action="typing"):
    try:
        bot.send_chat_action(user_id, action)
    except ApiTelegramException:
        pass  # игнорировать 403


# безопасная отправка сообщений
def safe_send_message(user_id, text, reply_markup=None):
    try:
        bot.send_message(user_id, text, reply_markup=reply_markup)
    except ApiTelegramException as e:
        if e.error_code == 403 and "bot was blocked by the user" in e.description:
            logger.warning(f"Пользователь {user_id} заблокировал бота. Сообщение не отправлено.")
        else:
            logger.error(f"Ошибка отправки сообщения пользователю {user_id}: {e}", exc_info=True)


# кастомный форматтер для логов
class CustomFormatter(logging.Formatter):
    def format(self, record):
        time_str = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
        if record.msg in ["ЗАПУСК TELEGRAM-БОТА", "Бот остановлен пользователем"]:
            return f"{time_str} - {record.msg}"
        if record.levelno >= logging.ERROR:
            return f"{time_str} - {record.name} - {record.levelname} - {record.getMessage()}"
        if hasattr(record, 'user_id') and hasattr(record, 'username') and hasattr(record, 'action'):
            return f"{time_str} - {record.user_id} (@{record.username}) - {record.action}"
        return f"{time_str} - {record.getMessage()}"


# настройка логгера
formatter = CustomFormatter()
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
file_handler = logging.FileHandler("bot.log", encoding="utf-8")
file_handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
logger.addHandler(file_handler)


bot = telebot.TeleBot(TOKEN)
sessions = {}


def get_main_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    kb.row("Задание 1", "Задание 5", "Задание 8")
    kb.row("Все задания")
    return kb


def get_task1_actions():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    kb.row("Ввести вручную", "Сгенерировать")
    kb.row("Выполнить", "Результат")
    kb.row("Назад")
    return kb


def get_task5_actions():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    kb.row("Ввести вручную", "Сгенерировать")
    kb.row("Выполнить", "Результат")
    kb.row("Назад")
    return kb


def get_task8_actions():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    kb.row("Ввести вручную", "Сгенерировать")
    kb.row("Выполнить", "Результат")
    kb.row("Назад")
    return kb


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username or "unknown"
    logger.info("", extra={
        'user_id': user_id,
        'username': username,
        'action': "Пользователь запустил бота (/start)"
    })
    sessions[user_id] = {"state": "main_menu", "fsm": None}
    safe_send_message(user_id, Messages.GREETING, reply_markup=get_main_keyboard())


@bot.message_handler(commands=['help'])
def help_command(message):
    # отправляет справку по командам
    user_id = message.from_user.id
    help_text = (
        "Справка по боту\n\n"
        "Доступные команды:\n"
        "/start — перезапуск бота\n"
        "/help — эта справка\n\n"
        "Как пользоваться:\n"
        "1. Выберите задание\n"
        "2. Нажмите «Ввести вручную» или «Сгенерировать»\n"
        "3. Выполните алгоритм\n"
        "4. Посмотрите результат\n\n"
        "! Используйте кнопки - они упрощают работу!"
    )
    safe_send_message(user_id, help_text, reply_markup=None)


@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.from_user.id
    username = message.from_user.username or "unknown"
    text = message.text.strip()

    if user_id not in sessions:
        logger.info("", extra={
            'user_id': user_id,
            'username': username,
            'action': "Новый пользователь"
        })
        sessions[user_id] = {"state": "main_menu", "fsm": None}
        safe_send_message(user_id, Messages.MAIN_MENU_PROMPT, reply_markup=get_main_keyboard())
        return

    session = sessions[user_id]

    if session["state"] == "main_menu":
        if text == "Задание 1":
            logger.info("", extra={
                'user_id': user_id,
                'username': username,
                'action': "Пользователь выбрал Задание 1"
            })
            fsm = Task1FSM()
            sessions[user_id] = {"state": "task1", "fsm": fsm}
            safe_send_message(user_id, Messages.TASK1_DESCRIPTION)
            safe_send_message(user_id, Messages.ACTION_PROMPT, reply_markup=get_task1_actions())

        elif text == "Задание 5":
            logger.info("", extra={
                'user_id': user_id,
                'username': username,
                'action': "Пользователь выбрал Задание 5"
            })
            fsm = Task5FSM()
            sessions[user_id] = {"state": "task5", "fsm": fsm}
            safe_send_message(user_id, Messages.TASK5_DESCRIPTION)
            safe_send_message(user_id, Messages.ACTION_PROMPT, reply_markup=get_task5_actions())

        elif text == "Задание 8":
            logger.info("", extra={
                'user_id': user_id,
                'username': username,
                'action': "Пользователь выбрал Задание 8"
            })
            fsm = Task8FSM()
            sessions[user_id] = {"state": "task8", "fsm": fsm}
            safe_send_message(user_id, Messages.TASK8_DESCRIPTION)
            safe_send_message(user_id, Messages.ACTION_PROMPT, reply_markup=get_task8_actions())

        elif text == "Все задания":
            logger.info("", extra={
                'user_id': user_id,
                'username': username,
                'action': "Пользователь запросил все задания"
            })
            safe_send_message(user_id, Messages.ALL_TASKS_DESCRIPTION)
            safe_send_message(user_id, Messages.MAIN_MENU_PROMPT, reply_markup=get_main_keyboard())

        else:
            logger.info("", extra={
                'user_id': user_id,
                'username': username,
                'action': f"Пользователь отправил неизвестную команду: '{text}'"
            })
            safe_send_message(user_id, Messages.INVALID_MAIN_CHOICE, reply_markup=get_main_keyboard())

    else:
        fsm = session["fsm"]
        try:
            response = fsm.handle(text)

            if response == "exit":
                logger.info("", extra={
                    'user_id': user_id,
                    'username': username,
                    'action': "Пользователь вернулся в главное меню"
                })
                sessions[user_id] = {"state": "main_menu", "fsm": None}
                safe_send_message(user_id, Messages.BACK_TO_MAIN, reply_markup=get_main_keyboard())
            else:
                # анимация "печатает..." для действий, требующих обработки
                if "Сгенерировано" in response or "Результат:" in response or "выполнен" in response.lower():
                    safe_send_chat_action(user_id, "typing")
                    time.sleep(0.4)

                safe_send_message(user_id, response)

                current_state = fsm.state
                if current_state == "menu":
                    prompt_msg = Messages.NEXT_ACTION_PROMPT
                    if session["state"] == "task1":
                        safe_send_message(user_id, prompt_msg, reply_markup=get_task1_actions())
                    elif session["state"] == "task5":
                        safe_send_message(user_id, prompt_msg, reply_markup=get_task5_actions())
                    elif session["state"] == "task8":
                        safe_send_message(user_id, prompt_msg, reply_markup=get_task8_actions())

        except Exception as e:
            logger.error(f"Ошибка у пользователя {user_id} (@{username}): {e}", exc_info=True)
            safe_send_message(user_id, f"{Messages.INVALID_INPUT}: {e}")
            if session["state"] == "task1":
                safe_send_message(user_id, Messages.ACTION_PROMPT, reply_markup=get_task1_actions())
            elif session["state"] == "task5":
                safe_send_message(user_id, Messages.ACTION_PROMPT, reply_markup=get_task5_actions())
            elif session["state"] == "task8":
                safe_send_message(user_id, Messages.ACTION_PROMPT, reply_markup=get_task8_actions())
            return


if __name__ == "__main__":
    logger.info("ЗАПУСК TELEGRAM-БОТА")
    try:
        bot.polling(none_stop=True)
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.critical("КРИТИЧЕСКАЯ ОШИБКА: Бот завершил работу с ошибкой", exc_info=True)
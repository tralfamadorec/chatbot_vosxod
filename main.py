import telebot
from telebot.apihelper import ApiTelegramException
from tasks.task1 import Task1FSM
from tasks.task5 import Task5FSM
from tasks.task8 import Task8FSM
from config import TOKEN

bot = telebot.TeleBot(TOKEN)
sessions = {}


def safe_send_message(user_id, text):
    # отправить сообщение, игнорируя ошибку 403 (пользователь заблокировал бота)
    try:
        bot.send_message(user_id, text)
    except ApiTelegramException as e:
        if e.error_code == 403 and "bot was blocked by the user" in e.description:
            print(f"Пользователь {user_id} заблокировал бота. Сообщение не отправлено.")
        else:
            raise  # другие ошибки - реальные проблемы


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    sessions[user_id] = {"state": "main_menu", "fsm": None}
    safe_send_message(
        user_id,
        "Привет! Выберите задание:\n"
        "1. Обработка двух массивов\n"
        "2. Подмассивы с заданной суммой\n"
        "3. Общие числа с перевёрнутыми"
    )


@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text.strip()

    if user_id not in sessions:
        sessions[user_id] = {"state": "main_menu", "fsm": None}
        safe_send_message(
            user_id,
            "Привет! Выберите задание:\n"
            "1. Обработка двух массивов\n"
            "2. Подмассивы с заданной суммой\n"
            "3. Общие числа с перевёрнутыми"
        )
        return

    session = sessions[user_id]

    if session["state"] == "main_menu":
        if text == "1":
            fsm = Task1FSM()
            sessions[user_id] = {"state": "task1", "fsm": fsm}
            safe_send_message(user_id, "Задание 1. Отправьте:\n1. Ввести вручную\n2. Сгенерировать\n3. Выполнить\n4. Результат\n5. Назад")
        elif text == "2":
            fsm = Task5FSM()
            sessions[user_id] = {"state": "task5", "fsm": fsm}
            safe_send_message(user_id, "Задание 5...")
        elif text == "3":
            fsm = Task8FSM()
            sessions[user_id] = {"state": "task8", "fsm": fsm}
            safe_send_message(user_id, "Задание 8...")
        else:
            safe_send_message(user_id, "Пожалуйста, отправьте 1, 2 или 3.")
    else:
        fsm = session["fsm"]
        try:
            response = fsm.handle(text)
            if response == "exit":
                sessions[user_id] = {"state": "main_menu", "fsm": None}
                safe_send_message(user_id, "Возврат в главное меню.")
            else:
                safe_send_message(user_id, response)
        except Exception as e:
            safe_send_message(user_id, f"Ошибка: {e}")


if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)
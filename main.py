import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from tasks.task1 import Task1FSM
from tasks.task5 import Task5FSM
from tasks.task8 import Task8FSM
from config import TOKEN

bot = telebot.TeleBot(TOKEN)
sessions = {}

# клавиатуры

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


# описания заданий

TASK1_DESC = (
    "Задание 1: Обработка двух массивов\n\n"
    "Алгоритм:\n"
    "1. Первый массив сортируется по убыванию\n"
    "2. Второй - по возрастанию\n"
    "3. Элементы складываются, если совпадают - обнуляются\n"
    "4. Результат сортируется по возрастанию"
)

TASK5_DESC = (
    "Задание 5: Подмассивы с заданной суммой\n\n"
    "Найти количество непрерывных подмассивов, сумма элементов которых равна заданному числу."
)

TASK8_DESC = (
    "Задание 8: Общие числа с перевёрнутыми\n\n"
    "Для каждого числа в первом массиве проверить, встречается ли оно или его перевёрнутая версия во втором массиве.\n"
    "Пример: 12 <-> 21"
)

ALL_TASKS_DESC = (
    "Все задания:\n\n"
    "1. Обработка двух массивов\n"
    "2. Подмассивы с заданной суммой\n"
    "3. Общие числа с перевёрнутыми\n\n"
    "Выберите задание для работы."
)


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    sessions[user_id] = {"state": "main_menu", "fsm": None}
    bot.send_message(
        user_id,
        "Привет! Я - бот для выполнения заданий по обработке массивов.\n\n"
        "Выберите задание:",
        reply_markup=get_main_keyboard()
    )


@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text.strip()

    if user_id not in sessions:
        sessions[user_id] = {"state": "main_menu", "fsm": None}
        bot.send_message(user_id, "Выберите задание:", reply_markup=get_main_keyboard())
        return

    session = sessions[user_id]

    # главное меню
    if session["state"] == "main_menu":
        if text == "Задание 1":
            fsm = Task1FSM()
            sessions[user_id] = {"state": "task1", "fsm": fsm}
            bot.send_message(user_id, TASK1_DESC)
            bot.send_message(user_id, "Выберите действие:", reply_markup=get_task1_actions())

        elif text == "Задание 5":
            fsm = Task5FSM()
            sessions[user_id] = {"state": "task5", "fsm": fsm}
            bot.send_message(user_id, TASK5_DESC)
            bot.send_message(user_id, "Выберите действие:", reply_markup=get_task5_actions())

        elif text == "Задание 8":
            fsm = Task8FSM()
            sessions[user_id] = {"state": "task8", "fsm": fsm}
            bot.send_message(user_id, TASK8_DESC)
            bot.send_message(user_id, "Выберите действие:", reply_markup=get_task8_actions())

        elif text == "Все задания":
            bot.send_message(user_id, ALL_TASKS_DESC)
            bot.send_message(user_id, "Выберите задание:", reply_markup=get_main_keyboard())

        else:
            bot.send_message(user_id, "Пожалуйста, используйте кнопки.", reply_markup=get_main_keyboard())

    # внутри задания
    else:
        fsm = session["fsm"]
        try:
            response = fsm.handle(text)
            if response == "exit":
                sessions[user_id] = {"state": "main_menu", "fsm": None}
                bot.send_message(user_id, "Возврат в главное меню.", reply_markup=get_main_keyboard())
            else:
                # после любого ответа - снова показываем кнопки действий
                bot.send_message(user_id, response)

                # определяем, нужно ли показывать клавиатуру
                current_state = fsm.state  # предполагаем, что fsm.state доступен

                if current_state == "menu":
                    if session["state"] == "task1":
                        bot.send_message(user_id, "Выберите следующее действие:", reply_markup=get_task1_actions())
                    elif session["state"] == "task5":
                        bot.send_message(user_id, "Выберите следующее действие:", reply_markup=get_task5_actions())
                    elif session["state"] == "task8":
                        bot.send_message(user_id, "Выберите следующее действие:", reply_markup=get_task8_actions())
                # если state != "menu" (например, "input_random"), то НИЧЕГО НЕ ОТПРАВЛЯЕМ
        except Exception as e:
            bot.send_message(user_id, f"Ошибка: {e}")
            if session["state"] == "task1":
                bot.send_message(user_id, "Выберите действие:", reply_markup=get_task1_actions())
            elif session["state"] == "task5":
                bot.send_message(user_id, "Выберите действие:", reply_markup=get_task5_actions())
            elif session["state"] == "task8":
                bot.send_message(user_id, "Выберите действие:", reply_markup=get_task8_actions())
            return


if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)
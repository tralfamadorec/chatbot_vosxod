"""Модуль для выполнения задания 5: подмассивы с заданной суммой

Реализует алгоритм с использованием функционального программирования:
- Чистая функция без побочных эффектов
- Генератор всех подмассивов (ленивые вычисления)
- Использование встроенных функций высшего порядка: sum, generator expression
- Отсутствие императивных циклов
- Неизменяемость данных

Алгоритм:
Подсчитывает количество непрерывных подмассивов, сумма элементов которых равна заданному числу
"""

from .errors import EmptyArrayError
from .messages import Messages

# функциональное ядро (чистая функция)

def count_subarrays_with_sum(arr, target):
    """Подсчитывает количество подмассивов с заданной суммой (ФП-стиль)

    Использует генераторное выражение для ленивого перебора всех подмассивов
    Не мутирует входной массив

    Пример логики как пайплайна:
        arr -> все подмассивы -> фильтрация по сумме -> подсчёт

    Args:
        arr (list[int]): Исходный массив целых чисел
        target (int): Целевая сумма

    Returns:
        int: Количество подмассивов, сумма которых равна target

    Raises:
        EmptyArrayError: Если входной массив пуст
    """
    if not arr:
        raise EmptyArrayError(Messages.TASK5_EMPTY_ARRAY)

    n = len(arr)
    # генератор всех непрерывных подмассивов: arr[i:j] для 0 <= i < j <= n
    subarrays = (arr[i:j] for i in range(n) for j in range(i + 1, n + 1))
    # декларативный подсчёт: сколько подмассивов имеют сумму == target
    return sum(1 for sub in subarrays if sum(sub) == target)


# FSM через словарь состояний (адаптирован под Telegram)

from .errors import InvalidInputError
from .messages import Messages
import random

class Task5FSM:
    """Конечный автомат для задания 5

    Управляет состояниями пользователя в Telegram-боте:
    - главное меню
    - ввод массива и цели вручную
    - генерация случайных данных
    - выполнение алгоритма
    - показ результата

    Attributes:
        state (str): Текущее состояние FSM (например, "menu", "input_manual")
        context (dict): Хранит данные пользователя (массив, цель, результат)
    """

    def __init__(self):
        # инициализирует FSM в состоянии "menu"
        self.state = "menu"
        self.context = {"arr": None, "target": None, "result": None}

    def handle(self, text):
        """Обрабатывает текстовое сообщение от пользователя

        Args:
            text (str): Текст сообщения (обычно текст кнопки или ввод данных)

        Returns:
            str: Ответное сообщение для отправки пользователю
        """
        if self.state == "menu":
            return self._handle_menu(text)
        elif self.state == "input_manual":
            return self._handle_input_manual(text)
        elif self.state == "input_random":
            return self._handle_input_random(text)
        elif self.state == "execute":
            return self._handle_execute()
        elif self.state == "show_result":
            return self._handle_show_result()
        else:
            return Messages.UNKNOWN_STATE

    def _handle_menu(self, text):
        """Обрабатывает выбор действия в главном меню задания 5

        Args:
            text (str): Текст кнопки ("Ввести вручную", "Сгенерировать" и т.д.)

        Returns:
            str: Ответное сообщение
        """
        if text == "Ввести вручную":
            self.state = "input_manual"
            return Messages.INPUT_MANUAL_TASK5
        elif text == "Сгенерировать":
            self.state = "input_random"
            return Messages.INPUT_RANDOM_SIZE
        elif text == "Выполнить":
            self.state = "execute"
            return self._handle_execute()
        elif text == "Результат":
            self.state = "show_result"
            return self._handle_show_result()
        elif text == "Назад":
            return "exit"
        else:
            return Messages.PLEASE_USE_BUTTONS

    def _handle_input_manual(self, text):
        """Обрабатывает ручной ввод массива и цели

        Args:
            text (str): Массив и цель, разделённые ';'

        Returns:
            str: Результат обработки или сообщение об ошибке
        """
        try:
            parts = text.split(";")
            if len(parts) != 2:
                return Messages.INVALID_FORMAT
            arr = list(map(int, parts[0].split()))
            target = int(parts[1])
            if not arr:
                raise EmptyArrayError(Messages.TASK5_EMPTY_ARRAY)
            self.context["arr"] = arr
            self.context["target"] = target
            self.context["result"] = None
            self.state = "menu"
            return Messages.DATA_SAVED
        except Exception as e:
            self.state = "menu"
            return f"{Messages.INVALID_INPUT}: {e}"

    def _handle_input_random(self, text):
        """Обрабатывает ввод размера для генерации случайных данных

        Args:
            text (str): Размер массива (целое число)

        Returns:
            str: Результат генерации или сообщение об ошибке
        """
        try:
            n = int(text)
            if n <= 0:
                raise InvalidInputError(Messages.INVALID_INPUT_SIZE)
            self.context["arr"] = [random.randint(-10, 10) for _ in range(n)]
            self.context["target"] = random.randint(-5, 10)
            self.context["result"] = None
            self.state = "menu"
            return f"{Messages.GENERATED_SUCCESS}\nМассив: {self.context['arr']}\nЦель: {self.context['target']}"
        except Exception as e:
            self.state = "menu"
            return f"{Messages.INVALID_INPUT}: {e}"

    def _handle_execute(self):
        """Выполняет алгоритм задания 5

        Returns:
            str: Результат выполнения или сообщение об ошибке
        """
        if self.context["arr"] is None or self.context["target"] is None:
            self.state = "menu"
            return Messages.NO_DATA
        try:
            self.context["result"] = count_subarrays_with_sum(self.context["arr"], self.context["target"])
            self.state = "menu"
            return Messages.ALGORITHM_DONE
        except Exception as e:
            self.state = "menu"
            return f"{Messages.INVALID_INPUT}: {e}"

    def _handle_show_result(self):
        """Возвращает результат выполнения алгоритма

        Returns:
            str: Результат или сообщение об ошибке
        """
        if self.context["result"] is None:
            self.state = "menu"
            return Messages.NOT_EXECUTED
        result = self.context["result"]
        target = self.context["target"]
        self.state = "menu"
        return f"{Messages.TASK5_RESULT_PREFIX}{target}: {result}"


# тестирование чистой логики
if __name__ == "__main__":
    print("Тест task5:")
    try:
        res = count_subarrays_with_sum([1, 1, 1], 2)
        print("Успешно:", res)
        assert res == 2
    except Exception as e:
        print("Ошибка:", e)

    try:
        count_subarrays_with_sum([], 5)
        print("Исключение не возникло")
    except EmptyArrayError:
        print("Поймана ожидаемая ошибка")
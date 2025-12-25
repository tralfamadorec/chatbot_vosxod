"""Модуль для выполнения задания 1: обработка двух массивов

Реализует алгоритм:
1. Первый массив сортируется по убыванию
2. Второй - по возрастанию
3. Элементы складываются; если совпадают - обнуляются
4. Результат сортируется по возрастанию
"""

from .errors import ArraysLengthMismatchError, InvalidInputError
from .messages import Messages
import random

# чистая логика

def sort_desc(arr):
    """Сортирует массив по убыванию

    Args:
        arr (list[int]): Исходный массив целых чисел

    Returns:
        list[int]: Новый массив, отсортированный по убыванию
    """
    return sorted(arr, reverse=True)


def sort_asc(arr):
    """Сортирует массив по возрастанию

    Args:
        arr (list[int]): Исходный массив целых чисел

    Returns:
        list[int]: Новый массив, отсортированный по возрастанию
    """
    return sorted(arr)


def sum_arrays_with_zero(a, b):
    """Выполняет поэлементную сумму двух массивов с обнулением совпадений

    Если элементы на одинаковых позициях равны, результат - 0
    Иначе - сумма элементов

    Args:
        a (list[int]): Первый массив
        b (list[int]): Второй массив (той же длины)

    Returns:
        list[int]: Результирующий массив
    """
    return [0 if x == y else x + y for x, y in zip(a, b)]


def solve(arr1, arr2):
    """Выполняет полный алгоритм задания 1

    Args:
        arr1 (list[int]): Первый массив
        arr2 (list[int]): Второй массив (той же длины)

    Returns:
        list[int]: Отсортированный по возрастанию результат обработки

    Raises:
        ArraysLengthMismatchError: Если длины массивов не совпадают
    """
    if len(arr1) != len(arr2):
        raise ArraysLengthMismatchError(Messages.TASK1_ARRAYS_LEN_MISMATCH)
    a_sorted = sort_desc(arr1)
    b_sorted = sort_asc(arr2)
    summed = sum_arrays_with_zero(a_sorted, b_sorted)
    return sort_asc(summed)


# FSM через словарь состояний (адаптирован под Telegram)

class Task1FSM:
    """Конечный автомат для задания 1

    Управляет состояниями пользователя в Telegram-боте:
    - главное меню
    - ввод данных вручную
    - генерация случайных данных
    - выполнение алгоритма
    - показ результата

    Attributes:
        state (str): Текущее состояние FSM (например, "menu", "input_manual")
        context (dict): Хранит данные пользователя (массивы, результат)
    """

    def __init__(self):
        # инициализирует FSM в состоянии "menu"
        self.state = "menu"
        self.context = {"arr1": None, "arr2": None, "result": None}

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
        """Обрабатывает выбор действия в главном меню задания 1

        Args:
            text (str): Текст кнопки ("Ввести вручную", "Сгенерировать" и т.д.)

        Returns:
            str: Ответное сообщение
        """
        if text == "Ввести вручную":
            self.state = "input_manual"
            return Messages.INPUT_MANUAL_TASK1
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
        """Обрабатывает ручной ввод двух массивов

        Args:
            text (str): Два массива, разделённые ';'

        Returns:
            str: Результат обработки или сообщение об ошибке
        """
        try:
            parts = text.split(";")
            if len(parts) != 2:
                return Messages.INVALID_FORMAT
            arr1 = list(map(int, parts[0].split()))
            arr2 = list(map(int, parts[1].split()))
            if len(arr1) != len(arr2):
                raise ArraysLengthMismatchError(Messages.TASK1_ARRAYS_LEN_MISMATCH)
            self.context["arr1"] = arr1
            self.context["arr2"] = arr2
            self.context["result"] = None
            self.state = "menu"
            return Messages.DATA_SAVED
        except Exception as e:
            self.state = "menu"
            return f"{Messages.INVALID_INPUT}: {e}"

    def _handle_input_random(self, text):
        """Обрабатывает ввод размера для генерации случайных массивов

        Args:
            text (str): Размер массивов (целое число)

        Returns:
            str: Результат генерации или сообщение об ошибке
        """
        try:
            n = int(text)
            if n <= 0:
                raise InvalidInputError(Messages.INVALID_INPUT_SIZE)
            self.context["arr1"] = [random.randint(1, 20) for _ in range(n)]
            self.context["arr2"] = [random.randint(1, 20) for _ in range(n)]
            self.context["result"] = None
            self.state = "menu"
            return f"{Messages.GENERATED_SUCCESS}\nМассив 1: {self.context['arr1']}\nМассив 2: {self.context['arr2']}"
        except Exception as e:
            self.state = "menu"
            return f"{Messages.INVALID_INPUT}: {e}"

    def _handle_execute(self):
        """Выполняет алгоритм задания 1

        Returns:
            str: Результат выполнения или сообщение об ошибке
        """
        if self.context["arr1"] is None or self.context["arr2"] is None:
            self.state = "menu"
            return Messages.NO_DATA
        try:
            self.context["result"] = solve(self.context["arr1"], self.context["arr2"])
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
        self.state = "menu"
        return f"{Messages.TASK1_RESULT}{result}"


if __name__ == "__main__":
    print("Тест task1: solve")
    try:
        res = solve([5, 7, 4], [4, 9, 3])
        print("Успешно:", res)
        assert res == [7, 8, 16]
    except Exception as e:
        print("Ошибка:", e)

    try:
        solve([1, 2], [3, 4, 5])
        print("Исключение не возникло")
    except ArraysLengthMismatchError:
        print("Поймана ожидаемая ошибка")
"""Модуль для выполнения задания 8: общие числа с перевёрнутыми

Реализует алгоритм подсчёта количества элементов из первого массива,
которые встречаются во втором массиве либо в виде исходного числа, либо в виде его перевёрнутой версии (например, 12 <-> 21)
"""

from .errors import EmptyArrayError, NegativeNumberError, InvalidInputError
from .messages import Messages
import random

# чистая логика

def reverse_number(n):
    """Возвращает перевёрнутое число без лидирующих нулей

    Args:
        n (int): Исходное неотрицательное целое число

    Returns:
        int: Перевёрнутое число

    Raises:
        NegativeNumberError: Если входное число отрицательное
    """
    if n < 0:
        raise NegativeNumberError(Messages.TASK8_NEGATIVE_NUMBER)
    return int(str(n)[::-1])


def count_common_with_reverse(arr1, arr2):
    """Считает количество общих элементов с учётом перевёрнутых чисел

    Для каждого элемента из первого массива проверяется,
    встречается ли он или его перевёрнутая версия во втором массиве

    Args:
        arr1 (list[int]): Первый массив целых чисел (только положительные)
        arr2 (list[int]): Второй массив целых чисел (только положительные)

    Returns:
        int: Количество элементов из arr1, имеющих совпадения в arr2

    Raises:
        EmptyArrayError: Если хотя бы один из массивов пуст
    """
    if not arr1 or not arr2:
        raise EmptyArrayError(Messages.TASK8_EMPTY_ARRAY)
    count = 0
    for x in arr1:
        if x in arr2 or reverse_number(x) in arr2:
            count += 1
    return count


# FSM через словарь состояний (адаптирован под Telegram)

class Task8FSM:
    """Конечный автомат для задания 8

    Управляет состояниями пользователя в Telegram-боте:
    - главное меню
    - ввод двух массивов вручную
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
        """Обрабатывает выбор действия в главном меню задания 8

        Args:
            text (str): Текст кнопки ("Ввести вручную", "Сгенерировать" и т.д.)

        Returns:
            str: Ответное сообщение
        """
        if text == "Ввести вручную":
            self.state = "input_manual"
            return Messages.INPUT_MANUAL_TASK8
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
            if not arr1 or not arr2:
                raise EmptyArrayError(Messages.TASK8_EMPTY_ARRAY)
            if any(x < 0 for x in arr1 + arr2):
                raise NegativeNumberError(Messages.TASK8_NEGATIVE_NUMBER)
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
            # генерируем ТОЛЬКО положительные числа (для корректного reverse)
            self.context["arr1"] = [random.randint(10, 999) for _ in range(n)]
            self.context["arr2"] = [random.randint(10, 999) for _ in range(n)]
            self.context["result"] = None
            self.state = "menu"
            return f"{Messages.GENERATED_SUCCESS}\nМассив 1: {self.context['arr1']}\nМассив 2: {self.context['arr2']}"
        except Exception as e:
            self.state = "menu"
            return f"{Messages.INVALID_INPUT}: {e}"

    def _handle_execute(self):
        """Выполняет алгоритм задания 8

        Returns:
            str: Результат выполнения или сообщение об ошибке
        """
        if self.context["arr1"] is None or self.context["arr2"] is None:
            self.state = "menu"
            return Messages.NO_DATA
        try:
            self.context["result"] = count_common_with_reverse(self.context["arr1"], self.context["arr2"])
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
        return f"{Messages.TASK8_RESULT_PREFIX}{result}"


if __name__ == "__main__":
    print("Тест task8:")
    try:
        res = count_common_with_reverse([12, 34, 56], [21, 78, 65])
        print("Успешно:", res)
        assert res == 2  # 12 <-> 21, 56 <-> 65
    except Exception as e:
        print("Ошибка:", e)

    try:
        count_common_with_reverse([-5], [5])
        print("Исключение не возникло")
    except NegativeNumberError:
        print("Поймана ожидаемая ошибка")

    try:
        count_common_with_reverse([], [1])
        print("Исключение не возникло")
    except EmptyArrayError:
        print("Поймана ожидаемая ошибка")
from errors import ArraysLengthMismatchError, EmptyArrayError, NegativeNumberError, InvalidInputError
import random

def reverse_number(n):
    if n < 0:
        raise NegativeNumberError("Число не должно быть отрицательным")
    return int(str(n)[::-1])

def count_common_with_reverse(arr1, arr2):
    if not arr1 or not arr2:
        raise EmptyArrayError("Массивы не должны быть пустыми")
    count = 0
    for x in arr1:
        if x in arr2 or reverse_number(x) in arr2:
            count += 1
    return count


class Task8FSM:
    def __init__(self):
        self.state = "menu"
        self.context = {"arr1": None, "arr2": None, "result": None}
        self.handlers = {
            "menu": self._menu,
            "input_manual": self._input_manual,
            "input_random": self._input_random,
            "execute": self._execute,
            "show_result": self._show_result,
        }

    def handle(self, event):
        handler = self.handlers.get(self.state)
        if handler:
            return handler(event)
        return "Неверное состояние"

    def _menu(self, event):
        choice = event.get("choice")
        if choice == "1":
            self.state = "input_manual"
            return "Введите массивы..."
        elif choice == "2":
            self.state = "input_random"
            return "Введите размер массивов:"
        elif choice == "3":
            self.state = "execute"
            return self.handle({"choice": "3"})
        elif choice == "4":
            self.state = "show_result"
            return self.handle({"choice": "4"})
        elif choice == "5":
            return "exit"
        else:
            return "Неверный выбор"

    def _input_manual(self, event):
        try:
            arr1 = list(map(int, event["arr1"].split()))
            arr2 = list(map(int, event["arr2"].split()))
            if not arr1 or not arr2:
                raise EmptyArrayError("Массивы не должны быть пустыми")
            if any(x < 0 for x in arr1 + arr2):
                raise NegativeNumberError("Числа не должны быть отрицательными")
            self.context["arr1"] = arr1
            self.context["arr2"] = arr2
            self.context["result"] = None
            self.state = "menu"
            return "Данные введены"
        except Exception as e:
            self.state = "menu"
            return f"Ошибка: {e}"

    def _input_random(self, event):
        try:
            n = int(event["n"])
            if n <= 0:
                raise InvalidInputError("Размер должен быть положительным")
            # Только положительные числа для корректного reverse
            self.context["arr1"] = [random.randint(10, 999) for _ in range(n)]
            self.context["arr2"] = [random.randint(10, 999) for _ in range(n)]
            self.context["result"] = None
            self.state = "menu"
            return f"Сгенерировано: {self.context['arr1']}, {self.context['arr2']}"
        except Exception as e:
            self.state = "menu"
            return f"Ошибка: {e}"

    def _execute(self, event):
        if self.context["arr1"] is None or self.context["arr2"] is None:
            self.state = "menu"
            return "Сначала введите данные!"
        try:
            self.context["result"] = count_common_with_reverse(self.context["arr1"], self.context["arr2"])
            self.state = "menu"
            return "Алгоритм выполнен"
        except Exception as e:
            self.state = "menu"
            return f"Ошибка: {e}"

    def _show_result(self, event):
        if self.context["result"] is None:
            self.state = "menu"
            return "Сначала выполните алгоритм!"
        result = self.context["result"]
        self.state = "menu"
        return f"Количество общих элементов: {result}"


if __name__ == "__main__":
    print("Тест task8:")
    try:
        res = count_common_with_reverse([12, 34, 56], [21, 78, 65])
        print("Успешно:", res)
        assert res == 2
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
from errors import ArraysLengthMismatchError, EmptyArrayError, NegativeNumberError, InvalidInputError
import random

def sort_desc(arr):
    return sorted(arr, reverse=True)

def sort_asc(arr):
    return sorted(arr)

def sum_arrays_with_zero(a, b):
    return [0 if x == y else x + y for x, y in zip(a, b)]

def solve(arr1, arr2):
    if len(arr1) != len(arr2):
        raise ArraysLengthMismatchError("Массивы должны быть одинаковой длины")
    a_sorted = sort_desc(arr1)
    b_sorted = sort_asc(arr2)
    summed = sum_arrays_with_zero(a_sorted, b_sorted)
    return sort_asc(summed)


class Task1FSM:
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
            return self.handle({"choice": "3"})  # перезапуск в новом состоянии
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
            if len(arr1) != len(arr2):
                raise ArraysLengthMismatchError("Массивы должны быть одинаковой длины")
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
                raise InvalidInputError("Размер массивов должен быть положительным")
            self.context["arr1"] = [random.randint(1, 20) for _ in range(n)]
            self.context["arr2"] = [random.randint(1, 20) for _ in range(n)]
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
            self.context["result"] = solve(self.context["arr1"], self.context["arr2"])
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
        return f"Результат: {result}"


if __name__ == "__main__":
    print("Тест task1:")
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
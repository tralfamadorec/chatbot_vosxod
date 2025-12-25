from errors import ArraysLengthMismatchError, EmptyArrayError, NegativeNumberError, InvalidInputError
import random

def count_subarrays_with_sum(arr, target):
    if not arr:
        raise EmptyArrayError("Массив не должен быть пустым")
    count = 0
    n = len(arr)
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += arr[j]
            if current_sum == target:
                count += 1
    return count


class Task5FSM:
    def __init__(self):
        self.state = "menu"
        self.context = {"arr": None, "target": None, "result": None}
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
            return "Введите массив и цель..."
        elif choice == "2":
            self.state = "input_random"
            return "Введите размер массива:"
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
            arr = list(map(int, event["arr"].split()))
            target = int(event["target"])
            if not arr:
                raise EmptyArrayError("Массив не должен быть пустым")
            self.context["arr"] = arr
            self.context["target"] = target
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
            self.context["arr"] = [random.randint(-10, 10) for _ in range(n)]
            self.context["target"] = random.randint(-5, 10)
            self.context["result"] = None
            self.state = "menu"
            return f"Сгенерировано: {self.context['arr']}, цель={self.context['target']}"
        except Exception as e:
            self.state = "menu"
            return f"Ошибка: {e}"

    def _execute(self, event):
        if self.context["arr"] is None or self.context["target"] is None:
            self.state = "menu"
            return "Сначала введите данные!"
        try:
            self.context["result"] = count_subarrays_with_sum(self.context["arr"], self.context["target"])
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
        target = self.context["target"]
        self.state = "menu"
        return f"Количество подмассивов с суммой {target}: {result}"


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
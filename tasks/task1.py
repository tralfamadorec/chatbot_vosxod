from .errors import ArraysLengthMismatchError, InvalidInputError
import random

# чистая логика

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


# FSM через словарь состояний (адаптирован под Telegram)

class Task1FSM:
    def __init__(self):
        self.state = "menu"
        self.context = {"arr1": None, "arr2": None, "result": None}

    def handle(self, text):
        # обрабатывает текстовое сообщение от пользователя
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
            return "Неизвестное состояние"

    def _handle_menu(self, text):
        if text == "1":
            self.state = "input_manual"
            return "Введите два массива через ';' (пример: 1 2 3; 4 5 6)"
        elif text == "2":
            self.state = "input_random"
            return "Введите размер массивов (целое число > 0):"
        elif text == "3":
            self.state = "execute"
            return self._handle_execute()
        elif text == "4":
            self.state = "show_result"
            return self._handle_show_result()
        elif text == "5":
            return "exit"
        else:
            return "Неверный выбор. Отправьте 1–5."

    def _handle_input_manual(self, text):
        try:
            parts = text.split(";")
            if len(parts) != 2:
                return "Неверный формат. Отправьте: 'массив1; массив2'"
            arr1 = list(map(int, parts[0].split()))
            arr2 = list(map(int, parts[1].split()))
            if len(arr1) != len(arr2):
                raise ArraysLengthMismatchError("Массивы разной длины")
            self.context["arr1"] = arr1
            self.context["arr2"] = arr2
            self.context["result"] = None
            self.state = "menu"
            return "Данные сохранены. Выберите:\n1–Ввести\n2–Сгенерировать\n3–Выполнить\n4–Результат\n5–Назад"
        except Exception as e:
            self.state = "menu"
            return f"Ошибка: {e}"

    def _handle_input_random(self, text):
        try:
            n = int(text)
            if n <= 0:
                raise InvalidInputError("Размер должен быть > 0")
            self.context["arr1"] = [random.randint(1, 20) for _ in range(n)]
            self.context["arr2"] = [random.randint(1, 20) for _ in range(n)]
            self.context["result"] = None
            self.state = "menu"
            return f"Сгенерировано.\nМассив 1: {self.context['arr1']}\nМассив 2: {self.context['arr2']}\nВыберите действие (1–5):"
        except Exception as e:
            self.state = "menu"
            return f"Ошибка: {e}"

    def _handle_execute(self):
        if self.context["arr1"] is None or self.context["arr2"] is None:
            self.state = "menu"
            return "Сначала введите данные!"
        try:
            self.context["result"] = solve(self.context["arr1"], self.context["arr2"])
            self.state = "menu"
            return "Алгоритм выполнен. Результат сохранён."
        except Exception as e:
            self.state = "menu"
            return f"Ошибка: {e}"

    def _handle_show_result(self):
        if self.context["result"] is None:
            self.state = "menu"
            return "Сначала выполните алгоритм!"
        result = self.context["result"]
        self.state = "menu"
        return f"Результат: {result}"


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
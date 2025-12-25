from .errors import EmptyArrayError, InvalidInputError
import random

# чистая логика

def count_subarrays_with_sum(arr, target):
    # считает количество подмассивов с заданной суммой
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


# FSM через словарь состояний (адаптирован под Telegram)

class Task5FSM:
    def __init__(self):
        self.state = "menu"
        self.context = {"arr": None, "target": None, "result": None}

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
        if text == "Ввести вручную":
            self.state = "input_manual"
            return "Введите массив и цель через ';' (например: 1 2 3; 5)"
        elif text == "Сгенерировать":
            self.state = "input_random"
            return "Введите размер массива (целое число > 0):"
        elif text == "Выполнить":
            self.state = "execute"
            return self._handle_execute()
        elif text == "Результат":
            self.state = "show_result"
            return self._handle_show_result()
        elif text == "Назад":
            return "exit"
        else:
            return "Пожалуйста, используйте кнопки."

    def _handle_input_manual(self, text):
        try:
            parts = text.split(";")
            if len(parts) != 2:
                return "Неверный формат. Отправьте: 'массив; цель'"
            arr = list(map(int, parts[0].split()))
            target = int(parts[1])
            if not arr:
                raise EmptyArrayError("Массив пуст")
            self.context["arr"] = arr
            self.context["target"] = target
            self.context["result"] = None
            self.state = "menu"
            return "Данные сохранены."
        except Exception as e:
            self.state = "menu"
            return f"Ошибка: {e}"

    def _handle_input_random(self, text):
        try:
            n = int(text)
            if n <= 0:
                raise InvalidInputError("Размер должен быть > 0")
            self.context["arr"] = [random.randint(-10, 10) for _ in range(n)]
            self.context["target"] = random.randint(-5, 10)
            self.context["result"] = None
            self.state = "menu"
            return f"Сгенерировано.\nМассив: {self.context['arr']}\nЦель: {self.context['target']}"
        except Exception as e:
            self.state = "menu"
            return f"Ошибка: {e}"

    def _handle_execute(self):
        if self.context["arr"] is None or self.context["target"] is None:
            self.state = "menu"
            return "Сначала введите данные!"
        try:
            self.context["result"] = count_subarrays_with_sum(self.context["arr"], self.context["target"])
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
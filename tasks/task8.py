from .errors import EmptyArrayError, NegativeNumberError, InvalidInputError
import random

# чистая логика

def reverse_number(n):
    # возвращает перевёрнутое число без лидирующих нулей
    if n < 0:
        raise NegativeNumberError("Отрицательные числа не допускаются")
    return int(str(n)[::-1])

def count_common_with_reverse(arr1, arr2):
    # считает, сколько элементов из arr1 встречаются в arr2 или в виде перевёрнутых
    if not arr1 or not arr2:
        raise EmptyArrayError("Массивы не должны быть пустыми")
    count = 0
    for x in arr1:
        if x in arr2 or reverse_number(x) in arr2:
            count += 1
    return count


# FSM через словарь состояний (адаптирован под Telegram)

class Task8FSM:
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
        if text == "Ввести вручную":
            self.state = "input_manual"
            return "Введите два массива через ';' (например: 12 34; 21 56)"
        elif text == "Сгенерировать":
            self.state = "input_random"
            return "Введите размер массивов (целое число > 0):"
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
                return "Неверный формат. Отправьте: 'массив1; массив2'"
            arr1 = list(map(int, parts[0].split()))
            arr2 = list(map(int, parts[1].split()))
            if not arr1 or not arr2:
                raise EmptyArrayError("Массивы не должны быть пустыми")
            if any(x < 0 for x in arr1 + arr2):
                raise NegativeNumberError("Отрицательные числа не допускаются")
            self.context["arr1"] = arr1
            self.context["arr2"] = arr2
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
            # генерируем ТОЛЬКО положительные числа (для корректного reverse)
            self.context["arr1"] = [random.randint(10, 999) for _ in range(n)]
            self.context["arr2"] = [random.randint(10, 999) for _ in range(n)]
            self.context["result"] = None
            self.state = "menu"
            return f"Сгенерировано.\nМассив 1: {self.context['arr1']}\nМассив 2: {self.context['arr2']}"
        except Exception as e:
            self.state = "menu"
            return f"Ошибка: {e}"

    def _handle_execute(self):
        if self.context["arr1"] is None or self.context["arr2"] is None:
            self.state = "menu"
            return "Сначала введите данные!"
        try:
            self.context["result"] = count_common_with_reverse(self.context["arr1"], self.context["arr2"])
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
        return f"Количество общих элементов (с учётом перевёрнутых): {result}"


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
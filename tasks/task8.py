from errors import EmptyArrayError, NegativeNumberError

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
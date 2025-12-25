from errors import EmptyArrayError

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
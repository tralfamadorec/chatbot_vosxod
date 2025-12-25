from errors import ArraysLengthMismatchError

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
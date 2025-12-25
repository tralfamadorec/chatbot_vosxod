def zip_with(func, *iterables):
    """Применяет функцию к элементам нескольких итерируемых объектов (как zip + map)

    Аналог Haskell `zipWith` или lodash `zipWith`

    Args:
        func (callable): Функция, принимающая столько аргументов, сколько iterables
        *iterables: Один или несколько итерируемых объектов

    Returns:
        list: Список результатов применения func к соответствующим элементам
    """
    return [func(*args) for args in zip(*iterables)]


def compose(*functions):
    """Композиция функций: compose(f, g)(x) == f(g(x))

    Функции применяются справа налево
    """
    return lambda x: x if not functions else functions[0](compose(*functions[1:])(x))


def identity(x):
    # возвращает аргумент без изменений (нейтральный элемент композиции)
    return x
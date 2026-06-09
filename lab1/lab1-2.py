"""Модуль для изучения итераторов, генераторов и сопрограмм (корутин).

Содержит инструменты для работы с числовой последовательностью Фибоначчи:
1. Класс-итератор FibonacciIterator (генерация по количеству n).
2. Класс-итератор FibonacchiLst (фильтрация произвольного списка).
3. Функция-генератор fibonacci_generator.
4. Сопрограмма my_genn для динамического получения списков.
"""

from typing import Any, Callable, Generator, List, Optional, Set


# === ЗАДАНИЕ 1: ИТЕРАТОРЫ (СПОСОБ 1 И СПОСОБ 2) ===

class FibonacciIterator:
    """Класс-итератор для последовательного получения n чисел Фибоначчи."""

    def __init__(self, n: int) -> None:
        """Инициализирует итератор заданным количеством элементов."""
        self.n: int = n
        self.count: int = 0
        self.a: int = 0
        self.b: int = 1

    def __iter__(self) -> "FibonacciIterator":
        """Возвращает сам объект итератора."""
        return self

    def __next__(self) -> int:
        """Возвращает следующее число Фибоначчи или вызывает StopIteration."""
        if self.count >= self.n:
            raise StopIteration
        
        current_value = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return current_value


def fibonacci_generator(n: int) -> Generator[int, None, None]:
    """Функция-генератор (Способ 2) для получения n чисел Фибоначчи."""
    a: int = 0
    b: int = 1
    for _ in range(n):
        yield a
        a, b = b, a + b


# === ДОПОЛНЕНИЕ К ЗАДАНИЮ 1: ФИЛЬТРУЮЩИЙ ИТЕРАТОР ===

class FibonacchiLst:
    """Класс-итератор для фильтрации элементов из заданного списка.
    
    Возвращает только те элементы переданного списка, которые принадлежат
    числовому ряду Фибоначчи.
    """

    def __init__(self, lst: List[int]) -> None:
        """Инициализирует итератор входным списком и генерирует сет чисел Фибоначчи.

        Аргументы:
            lst: Список целых чисел для фильтрации.
        """
        self.lst: List[int] = lst
        self.index: int = 0
        self.fib_set: Set[int] = self._generate_fib_set_up_to(max(lst) if lst else 0)

    def _generate_fib_set_up_to(self, max_val: int) -> Set[int]:
        """Вспомогательный метод для генерации множества чисел Фибоначчи до max_val."""
        set_fib: Set[int] = set()
        a, b = 0, 1
        while a <= max_val:
            set_fib.add(a)
            a, b = b, a + b
        return set_fib

    def __iter__(self) -> "FibonacchiLst":
        """Возвращает объект-итератор."""
        return self

    def __next__(self) -> int:
        """Возвращает следующий элемент списка, являющийся числом Фибоначчи."""
        while self.index < len(self.lst):
            current_item = self.lst[self.index]
            self.index += 1
            if current_item in self.fib_set:
                return current_item
        raise StopIteration


# === ЗАДАНИЕ 2: СОПРОГРАММА (КОРУТИНА) ===

def prime_coroutine(func: Callable[..., Generator[Any, Any, Any]]) -> Callable[..., Generator[Any, Any, Any]]:
    """Декоратор для автоматической инициализации (примирования) сопрограммы."""
    def wrapper(*args: Any, **kwargs: Any) -> Generator[Any, Any, Any]:
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return wrapper


@prime_coroutine
def my_genn() -> Generator[Optional[List[int]], int, None]:
    """Сопрограмма, динамически возвращающая список чисел Фибоначчи длины n."""
    fib_list: List[int] = []
    a: int = 0
    b: int = 1
    
    # Первичная точка остановки примирования
    n = yield None 
    
    while True:
        # Блок находится строго внутри бесконечного цикла
        while len(fib_list) < n:
            fib_list.append(a)
            a, b = b, a + b
            
        n = yield fib_list[:n]
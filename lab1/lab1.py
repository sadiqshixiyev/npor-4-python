"""Модуль для изучения итераторов, генераторов и сопрограмм (корутин)."""

from typing import Any, Callable, Generator, Optional


# === ЗАДАНИЕ 1 ===

class FibonacciIterator:
    """Класс-итератор для последовательного получения чисел Фибоначчи."""

    def __init__(self, n: int) -> None:
        """Инициализация итератора."""
        self.n: int = n
        self.count: int = 0
        self.a: int = 0
        self.b: int = 1

    def __iter__(self) -> "FibonacciIterator":
        """Возвращает объект итератора."""
        return self

    def __next__(self) -> int:
        """Возвращает следующее число Фибоначчи."""
        if self.count >= self.n:
            raise StopIteration
        
        current_value = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return current_value


def fibonacci_generator(n: int) -> Generator[int, None, None]:
    """Функция-генератор для получения чисел Фибоначчи."""
    a: int = 0
    b: int = 1
    for _ in range(n):
        yield a
        a, b = b, a + b


# === ЗАДАНИЕ 2 ===

def prime_coroutine(func: Callable[..., Generator[Any, Any, Any]]) -> Callable[..., Generator[Any, Any, Any]]:
    """Декоратор для автоматической инициализации (примирования) сопрограммы."""
    def wrapper(*args: Any, **kwargs: Any) -> Generator[Any, Any, Any]:
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return wrapper


@prime_coroutine
def my_genn() -> Generator[Optional[list[int]], int, None]:
    """Сопрограмма, динамически возвращающая список чисел Фибоначчи длины n."""
    fib_list: list[int] = []
    a: int = 0
    b: int = 1
    
    # Ждем первую отправку n через метод .send()
    n = yield None 
    
    while True:
        # ИСПРАВЛЕНО: Теперь этот блок находится строго внутри цикла while True
        while len(fib_list) < n:
            fib_list.append(a)
            a, b = b, a + b
            
        # ИСПРАВЛЕНО: yield тоже сдвинут внутрь тела основного цикла
        n = yield fib_list[:n]
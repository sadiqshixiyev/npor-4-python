"""Модуль для автоматического тестирования генераторов и корутины Фибоначчи."""

import unittest
from lab1 import FibonacciIterator, fibonacci_generator, my_genn


class TestFibonacciStructures(unittest.TestCase):
    """Набор тестов для проверки корректности работы итераторов и корутины."""

    def test_class_iterator(self) -> None:
        """Проверка генерации ряда через класс-итератор FibonacciIterator."""
        fib_iter = FibonacciIterator(5)
        result = list(fib_iter)
        self.assertEqual(result, [0, 1, 1, 2, 3])

    def test_function_generator(self) -> None:
        """Проверка ленивой генерации через функцию fibonacci_generator."""
        result = list(fibonacci_generator(6))
        self.assertEqual(result, [0, 1, 1, 2, 3, 5])

    def test_coroutine_dynamic_send(self) -> None:
        """Проверка корутины my_genn на соответствие тестовому сценарию задания.
        
        Сценарий: отправка последовательностей длин 3, 5 и 8.
        """
        gen = my_genn()
        
        self.assertEqual(gen.send(3), [0, 1, 1])
        self.assertEqual(gen.send(5), [0, 1, 1, 2, 3])
        self.assertEqual(gen.send(8), [0, 1, 1, 2, 3, 5, 8, 13])

    def test_coroutine_shrink_request(self) -> None:
        """Проверка корутины на корректный возврат при уменьшении запроса n."""
        gen = my_genn()
        gen.send(6)  # Сначала генерируем длинный список
        
        # Если запросить меньше, она должна отдать корректно усеченный срез
        self.assertEqual(gen.send(2), [0, 1])


if __name__ == "__main__":
    unittest.main()
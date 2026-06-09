"""Модуль для автоматического тестирования генераторов и корутины Фибоначчи."""

import unittest

# Динамический импорт для корректной работы с файлами, содержащими дефис в имени
lab_module = __import__("lab1-2")
FibonacciIterator = lab_module.FibonacciIterator
fibonacci_generator = lab_module.fibonacci_generator
FibonacchiLst = lab_module.FibonacchiLst
my_genn = lab_module.my_genn


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

    def test_fibonacci_list_filter(self) -> None:
        """Проверка фильтрующего итератора FibonacchiLst на кастомном списке."""
        input_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
        fib_lst_iter = FibonacchiLst(input_list)
        result = list(fib_lst_iter)
        self.assertEqual(result, [0, 1, 2, 3, 5, 8, 1])

    def test_coroutine_dynamic_send(self) -> None:
        """Проверка корутины my_genn на соответствие тестовому сценарию задания."""
        gen = my_genn()
        self.assertEqual(gen.send(3), [0, 1, 1])
        self.assertEqual(gen.send(5), [0, 1, 1, 2, 3])
        self.assertEqual(gen.send(8), [0, 1, 1, 2, 3, 5, 8, 13])


if __name__ == "__main__":
    unittest.main()
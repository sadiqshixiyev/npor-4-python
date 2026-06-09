import unittest
import json
import os
from lab2 import CurrencyComponent, JsonDecorator, YamlDecorator, CsvDecorator

class TestCurrencyDecorators(unittest.TestCase):
    """Тесты для проверки функциональности декораторов валют."""

    def setUp(self):
        # Инициализируем базовый компонент
        self.base = CurrencyComponent()

    def test_json_decorator(self):
        """Проверка работы JsonDecorator."""
        decorator = JsonDecorator(self.base)
        result = decorator.operation()
        # Проверяем, что результат является валидным JSON
        data = json.loads(result)
        self.assertIn("Valute", data)
        print("\nJSON Decorator тест пройден!")

    def test_yaml_decorator(self):
        """Проверка работы YamlDecorator."""
        decorator = YamlDecorator(self.base)
        result = decorator.operation()
        self.assertIsInstance(result, str)
        print("YAML Decorator тест пройден!")

    def test_csv_decorator(self):
        """Проверка работы CsvDecorator."""
        decorator = CsvDecorator(self.base)
        result = decorator.operation()
        self.assertTrue(result.startswith("CharCode,Value"))
        print("CSV Decorator тест пройден!")

if __name__ == "__main__":
    unittest.main()
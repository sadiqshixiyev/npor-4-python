"""Модуль реализации паттерна 'Декоратор' для форматирования курсов валют ЦБ РФ.

Данный модуль содержит абстрактные интерфейсы и конкретные реализации
компонентов и декораторов, позволяющих получать данные о курсах валют
и приводить их к форматам JSON, YAML и CSV, а также сохранять в файлы.
"""

from abc import ABC, abstractmethod
import csv
import io
import json
from typing import Any, Dict
import requests
import yaml


class Component(ABC):
    """Абстрактный Базовый Компонент.
    
    Определяет интерфейс для динамического расширения обязанностей
    через декораторы в соответствии с паттерном.
    """

    @abstractmethod
    def operation(self) -> str:
        """Возвращает строковое представление данных валют."""
        pass


class CurrencyComponent(Component):
    """Конкретный Компонент бизнес-логики.
    
    Отвечает за прямое обращение к API Центробанка России и возврат
    базового словаря с курсами валют в формате JSON-строки.
    """

    def __init__(self) -> None:
        """Инициализирует URL-адрес API Центробанка."""
        self._url: str = "https://www.cbr-xml-daily.ru/daily_json.js"

    def operation(self) -> str:
        """Запрашивает данные с API ЦБ РФ.

        Возвращает:
            str: Неформатированная JSON-строка с данными курсов валют.
                 В случае ошибки сети возвращает JSON-строку с ошибкой.
        """
        try:
            response = requests.get(self._url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            return json.dumps({"error": f"Failed to fetch data: {str(e)}"})


class BaseDecorator(Component):
    """Базовый класс Декоратора.
    
    Следует тому же интерфейсу Component, агрегирует внутри себя
    завёрнутый компонент и делегирует ему выполнение базовой операции.
    """

    def __init__(self, component: Component) -> None:
        """Инициализирует декоратор обёртываемым компонентом.

        Аргументы:
            component: Любой объект, реализующий интерфейс Component.
        """
        self._component: Component = component

    @property
    def component(self) -> Component:
        """Возвращает обёрнутый компонент."""
        return self._component

    def operation(self) -> str:
        """Делегирует выполнение операции вложенному компоненту."""
        return self._component.operation()


class JsonDecorator(BaseDecorator):
    """Декоратор для форматирования данных в красивый (Pretty) JSON."""

    def operation(self) -> str:
        """Преобразует сырой JSON в форматированную строку с отступами.

        Возвращает:
            str: Валидный JSON с форматированием в 4 пробела.
        """
        raw_data = self.component.operation()
        data: Dict[str, Any] = json.loads(raw_data)
        return json.dumps(data, indent=4, ensure_ascii=False)

    def save_to_file(self, filepath: str) -> None:
        """Сохраняет форматированные JSON данные в файл.

        Аргументы:
            filepath: Путь к сохраняемому файлу.
        """
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.operation())


class YamlDecorator(BaseDecorator):
    """Декоратор для преобразования данных в YAML формат."""

    def operation(self) -> str:
        """Преобразует JSON-данные от компонента в строку формата YAML.

        Возвращает:
            str: Данные в структурированном формате YAML.
        """
        raw_data = self.component.operation()
        data: Dict[str, Any] = json.loads(raw_data)
        return yaml.dump(data, allow_unicode=True, sort_keys=False)

    def save_to_file(self, filepath: str) -> None:
        """Сохраняет YAML данные в файл.

        Аргументы:
            filepath: Путь к сохраняемому файлу.
        """
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.operation())


class CsvDecorator(BaseDecorator):
    """Декоратор для плоского табличного преобразования данных в формат CSV.
    
    Извлекает из структуры ЦБ блок 'Valute' и представляет его строками.
    """

    def operation(self) -> str:
        """Преобразует вложенную структуру курсов валют в плоскую CSV таблицу.

        Возвращает:
            str: Строковое представление CSV таблицы.
        """
        raw_data = self.component.operation()
        data: Dict[str, Any] = json.loads(raw_data)
        
        output = io.StringIO()
        writer = csv.writer(output, lineterminator="\n")
        
        # Заголовки таблицы
        writer.writerow(["ID", "NumCode", "CharCode", "Nominal", "Name", "Value", "Previous"])
        
        # Валюты находятся внутри ключа 'Valute'
        valutes: Dict[str, Dict[str, Any]] = data.get("Valute", {})
        
        for valute_data in valutes.values():
            writer.writerow([
                valute_data.get("ID"),
                valute_data.get("NumCode"),
                valute_data.get("CharCode"),
                valute_data.get("Nominal"),
                valute_data.get("Name"),
                valute_data.get("Value"),
                valute_data.get("Previous")
            ])
            
        return output.getvalue()

    def save_to_file(self, filepath: str) -> None:
        """Сохраняет CSV таблицу в файл.

        Аргументы:
            filepath: Путь к сохраняемому файлу.
        """
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            f.write(self.operation())
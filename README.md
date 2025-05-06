# Repo Service
Сервис FastAPI с использованием паттерна репозиторий и команда для описания бизнес логики

## Prerequisites
- python 3.11 [requirements](requirements.txt)
- MongoDB
- ClickHouse


## Установка виртуального окружения
1. Устанавливаем виртуальную среду командой `python -m venv venv`

### Установка зависимостей через Poetry
1. На компьютере должен быть установлен `poetry` с помощью команды `pip install poetry`
2. Устанавливаем основные зависимости через `poetry` с помощью команд:
    - `poetry install --without dev` - для установки основных зависимостей
    - `poetry install --with dev` - для установки тестовых библиотек разработки
3. Необязательный плагин `poetry` для экспорта в `requirements.txt`: `pip install poetry-plugin-export`
4. Usage : `poetry export -f requirements.txt --output requirements.txt --without-hashes`

### Установка зависимостей через Pip
1. Альтернативное решение запустить `pip install -r requirements.txt`


## Запуск приложения стандартным способом
1. Требуется указать переменные окружения для подключения к Kafka в `src/configs.py`
2. Запускаем приложение с помощью команды:
    - `python -m uvicorn --host 0.0.0.0 --port 5032 src.main:app`,
##### Аргументы
`port` указывается по желанию
--log-level: задает уровень логирования (debug, info, warning, error, critical)
--workers: определяет количество воркеров в приложении (задается как целое число, по умолчанию 1)

## Запуск линтеров isort, flake8
Запуск линтеров осуществляется командами из корневого каталога:
    - isort: `isort .`
    - flake8: `flake8 .`

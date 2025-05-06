# Bookkeeper Service

Микросервис расчета состояния стратегий

## Prerequisites
- python 3.11 [requirements](requirements.txt)
- MongoDB
- ClickHouse


## Подготовка перед запуском приложения
Переходим в каталог в приложением

### Создаем виртуальное окружение

```shell
python3.11 -m venv venv
```

### Активируем виртуальное окружение

```shell
source /venv/bin/activate
```

### Устанавливаем библиотеки и зависимости

```shell
pip install -r requirements.txt
```
### Экпортируем переменные окружения
* export environment variables

```shell
export RABBIT_URI="amqp://user:pass@host:5672/vhost"
export MONGO_URI="mongodb://user:pass@host:27017/database?authSource=admin"
```

### Запускаем приложение
#### development
Запуск приложения, когда виртуальное окружение активировано
Осуществляется из каталога приложения

```shell
faststream run src.main:app --log-level debug
```

Быстрый запуск, когда виртуальное окружение установлено и имеет установленные зависимости. Но не активировано.
Указываем абсолютный путь к папке с виртуальным окружением
```sh
/var/www/vhosts/cryptobot/bookkeeper/venv/bin/faststream run src.main:app --log-level warning --workers 8
```
##### Аргументы
--log-level: задает уровень логирования (debug, info, warning, error, critical)
--workers: определяет количество воркеров в приложении

#### production
Для запуска в production используется конфиг супервизора
use [.ini](bookkeeper.ini) file and make your own system supervisor config under /etc/supervisord.d/bookkeeper.ini

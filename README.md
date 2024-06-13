# ZyfraTestTask
Веб-приложение для расчёта данных о выгрузках на карьере.

## В приложении используются:
* Python (3.11)
* Django (5.0.6)
* SQLite

## Инструкция для установки:
1. Клонируйте репозиторий 

* ```git clone https://github.com/lowec21/ZyfraTestTask.git```

2. Перейдите в директорию TestTask

* ```cd TestTask```

3. Создайте виртуальное окружение

* ```python -m venv venv```

4. Активируйте виртуальное окружение

* ```source venv/bin/activate```

5. Установите зависимости

* ```pip install -r requirements.txt```

В репозитории сформированы фикстуры для заполнения базы данных.
Если нужно будет вернуть БД в исходное состояние, перейдите в директорию quarryweb и выполните команды:

* ```python manage.py loaddata quarryapp/fixtures/storage.json```
* ```python manage.py loaddata quarryapp/fixtures/dumptruck.json```
* ```python manage.py loaddata quarryapp/fixtures/trip.json```

Для запуска приложения, находясь в директории quarryweb выполните команду:

* ```python manage.py runserver```

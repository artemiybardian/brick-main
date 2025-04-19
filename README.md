# Этапы запуска проекта

## 1. Создание файла окружения

Создайте файл `.env` на основе примера `.env.example`:

```
cp .env.example .env
```

## 2. Создание виртуального окружения (для Windows)

```
python -m venv venv
```

## 3. Активация виртуального окружения

```
venv\Scripts\activate
```

## 4. Установка зависимостей

```
pip install -r requirements.txt
```

## 5. Запуск базы данных с помощью Docker

```
docker compose up -d
```

## 6. Применение миграций

```
python server/manage.py migrate
```

## 7. Запуск сервера разработки

```
python server/manage.py runserver
```

После выполнения этих шагов ваш проект должен быть доступен по адресу http://127.0.0.1:8000/
Swagger: http://127.0.0.1:8000/swagger/

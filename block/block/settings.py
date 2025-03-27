"""
Настройки проекта BRICK.

Этот файл содержит все основные настройки Django-проекта.
Для получения дополнительной информации о настройках Django, посетите:
https://docs.djangoproject.com/en/5.1/topics/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
# Этот файл содержит конфиденциальные данные и не должен быть в репозитории
load_dotenv()

# Определение базовой директории проекта
# Используется для построения путей к другим файлам проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Настройки безопасности
# ВНИМАНИЕ: Храните секретный ключ в безопасном месте и не публикуйте его в репозитории!
# Секретный ключ используется для криптографической подписи
SECRET_KEY = os.getenv('SECRET_KEY')

# Режим отладки
# ВНИМАНИЕ: Не включайте режим отладки в продакшене!
# В режиме отладки:
# - Показываются подробные сообщения об ошибках
# - Автоматически перезагружается сервер при изменении кода
# - Отключаются некоторые проверки безопасности
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Список разрешенных хостов
# Указывает, какие домены могут обслуживать этот сайт
# В продакшене замените на реальные домены
ALLOWED_HOSTS = ['127.0.0.1']

# Список установленных приложений
INSTALLED_APPS = [
    # Встроенные приложения Django
    'django.contrib.admin',      # Административный интерфейс
    'django.contrib.auth',      # Система аутентификации
    'django.contrib.contenttypes',  # Система типов контента
    'django.contrib.sessions',  # Система сессий
    'django.contrib.messages',  # Система сообщений
    'django.contrib.staticfiles',  # Управление статическими файлами
    
    # Сторонние приложения
    'allauth',  # Система аутентификации и авторизации
    'allauth.account',  # Управление аккаунтами пользователей
    'allauth.socialaccount',  # Поддержка социальной аутентификации
    'allauth.socialaccount.providers.google',  # Поддержка входа через Google
    'allauth.socialaccount.providers.github',  # Поддержка входа через GitHub
    
    # Локальные приложения
    'database',  # Приложение для работы с базой данных
    'front',     # Приложение для фронтенда
    'users',     # Приложение для управления пользователями
]

# Настройки промежуточного ПО
# Middleware - это набор функций, которые выполняются при каждом запросе
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Базовые настройки безопасности
    'django.contrib.sessions.middleware.SessionMiddleware',  # Управление сессиями
    'django.middleware.common.CommonMiddleware',  # Общие настройки
    'django.middleware.csrf.CsrfViewMiddleware',  # Защита от CSRF-атак
    'allauth.account.middleware.AccountMiddleware',  # Middleware для allauth
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Аутентификация
    'django.contrib.messages.middleware.MessageMiddleware',  # Система сообщений
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Защита от clickjacking
]

# Корневая конфигурация URL
# Указывает Django, где искать основные URL-маршруты
ROOT_URLCONF = 'block.urls'

# Настройки шаблонов
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Движок шаблонов
        'DIRS': [BASE_DIR / 'templates'],  # Путь к глобальным шаблонам
        'APP_DIRS': True,  # Поиск шаблонов в папках приложений
        'OPTIONS': {
            'context_processors': [  # Процессоры контекста для шаблонов
                'django.template.context_processors.debug',  # Информация об отладке
                'django.template.context_processors.request',  # Объект запроса
                'django.contrib.auth.context_processors.auth',  # Информация о пользователе
                'django.contrib.messages.context_processors.messages',  # Система сообщений
                'django.template.context_processors.static',  # Статические файлы
                'django.template.context_processors.media',  # Медиафайлы
            ],
        },
    },
]

# WSGI приложение
# Путь к WSGI-приложению для развертывания
WSGI_APPLICATION = 'block.wsgi.application'

# Настройки базы данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Тип базы данных
        'NAME': os.getenv('DB_NAME'),  # Имя базы данных
        'USER': os.getenv('DB_USER'),  # Пользователь базы данных
        'PASSWORD': os.getenv('DB_PASSWORD'),  # Пароль
        'HOST': os.getenv('DB_HOST'),  # Хост базы данных
    }
}

# Настройки валидации паролей
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        # Проверяет схожесть пароля с атрибутами пользователя
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        # Проверяет минимальную длину пароля
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        # Проверяет, не является ли пароль слишком распространенным
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        # Проверяет, не состоит ли пароль только из цифр
    },
]

# Настройки интернационализации
LANGUAGE_CODE = 'en-us'  # Код языка по умолчанию
TIME_ZONE = 'UTC'  # Часовой пояс
USE_I18N = True  # Включение интернационализации
USE_TZ = True  # Использование часовых поясов

# Настройки статических файлов
STATIC_URL = '/static/'  # URL для статических файлов
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Директория для собранных статических файлов
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Дополнительные директории со статическими файлами
]

# Настройки медиафайлов
MEDIA_URL = '/media/'  # URL для медиафайлов
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Директория для загруженных файлов

# Создание необходимых директорий
os.makedirs(STATIC_ROOT, exist_ok=True)  # Директория для статических файлов
os.makedirs(MEDIA_ROOT, exist_ok=True)  # Директория для медиафайлов
os.makedirs(os.path.join(MEDIA_ROOT, 'avatars'), exist_ok=True)  # Директория для аватаров

# Тип первичного ключа по умолчанию
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # Использование 64-битных целых чисел

# Модель пользователя по умолчанию
AUTH_USER_MODEL = 'users.CustomUser'  # Использование кастомной модели пользователя

# Настройки аутентификации
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Стандартная аутентификация
    'allauth.account.auth_backends.AuthenticationBackend',  # Аутентификация через allauth
]

# Настройки OAuth провайдеров
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],  # Запрашиваемые разрешения
        'AUTH_PARAMS': {'access_type': 'online'},  # Тип доступа
    },
    'github': {
        'SCOPE': ['user:email'],  # Запрашиваемые разрешения
    },
}

# Настройки редиректов после входа/выхода
LOGIN_REDIRECT_URL = '/'  # Куда перенаправлять после входа
LOGOUT_REDIRECT_URL = '/'  # Куда перенаправлять после выхода

# Настройки аккаунта пользователя
ACCOUNT_LOGOUT_REDIRECT_URL = '/'  # Редирект после выхода
ACCOUNT_LOGIN_METHODS = {'email', 'username'}  # Разрешенные методы входа
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']  # Обязательные поля при регистрации

# Настройки подтверждения email
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # Обязательное подтверждение email
ACCOUNT_UNIQUE_EMAIL = True  # Уникальный email для каждого пользователя

# Настройки отправки email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"  # Бэкенд для отправки email
EMAIL_HOST = os.getenv('EMAIL_HOST')  # SMTP-сервер
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))  # Порт SMTP
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'  # Использование TLS
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')  # Логин для SMTP
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')  # Пароль для SMTP
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')  # Email отправителя по умолчанию
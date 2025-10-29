# Task Manager with JWT

Это веб-приложение для управления задачами (Task Manager), построенное на FastAPI с использованием JWT-аутентификации. Пользователи могут регистрироваться, авторизовываться и управлять своими задачами (создавать, просматривать, обновлять, удалять и искать).

## Функциональность

- **Аутентификация и авторизация**: Регистрация пользователей, вход с JWT-токенами.
- **Управление задачами**:
  - Создание задач (title, description).
  - Просмотр списка задач пользователя.
  - Просмотр конкретной задачи.
  - Частичное обновление задач (только указанные поля).
  - Удаление задач.
  - Поиск задач по заголовку.
- **Безопасность**: Все эндпоинты задач защищены JWT. Только владелец может управлять своими задачами.
- **API документация**: Автоматическая генерация Swagger UI на `/docs`.

## Требования

- Python 3.11 или выше
- PostgreSQL (локально или удалённо)
- Виртуальное окружение (venv)

## Установка

1. **Клонируйте репозиторий**:
   ```
   git clone https://github.com/dikend1/Task-Manager-with-JWT.git
   cd Task-Manager-with-JWT
   ```

2. **Создайте виртуальное окружение**:
   ```
   python3 -m venv venv
   source venv/bin/activate  # На Windows: venv\Scripts\activate
   ```

3. **Установите зависимости**:
   ```
   pip install fastapi sqlalchemy psycopg2-binary python-jose[cryptography] passlib[bcrypt] pydantic-settings alembic uvicorn
   ```

4. **Настройте базу данных**:
   - Установите PostgreSQL, если не установлено.
   - Создайте базу данных (например, `task_manager`).

5. **Создайте файл `.env`** в корне проекта с переменными окружения:
   ```
   DATABASE_URL=postgresql://username:password@localhost/task_manager
   SECRET_KEY=your-secret-key-here  # Случайная строка для JWT
   ```

6. **Примените миграции базы данных**:
   ```
   alembic upgrade head
   ```

## Запуск

1. **Активируйте виртуальное окружение** (если не активировано):
   ```
   source venv/bin/activate
   ```

2. **Запустите сервер**:
   ```
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Откройте браузер**:
   - API: http://localhost:8000
   - Документация Swagger: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Endpoints

### Аутентификация
- **POST /auth/register**: Регистрация нового пользователя. Тело: `{"username": "string", "password": "string"}`
- **POST /auth/login**: Вход пользователя. Тело: `{"username": "string", "password": "string"}`. Возвращает JWT-токен.

### Задачи (требуют заголовка `Authorization: Bearer <token>`)
- **POST /tasks**: Создать задачу. Тело: `{"title": "string", "description": "string"}`
- **GET /tasks**: Получить все задачи пользователя.
- **GET /tasks/{task_id}**: Получить задачу по ID.
- **PUT /tasks/{task_id}**: Обновить задачу (частичное обновление). Тело: `{"title": "string"}` или `{"description": "string"}` (опционально)
- **DELETE /tasks/{task_id}**: Удалить задачу.
- **GET /tasks/search/?q={query}**: Поиск задач по заголовку.

## Использование

### Регистрация и вход
- **Регистрация**: POST `/auth/register` с JSON `{"username": "user", "password": "pass"}`
- **Вход**: POST `/auth/login` с теми же данными. Получите JWT-токен в ответе.

### Работа с задачами
Все запросы к задачам требуют заголовка `Authorization: Bearer <token>`.

- **Создать задачу**: POST `/tasks` с JSON `{"title": "Моя задача", "description": "Описание"}`
- **Получить все задачи**: GET `/tasks`
- **Получить задачу по ID**: GET `/tasks/{id}`
- **Обновить задачу**: PUT `/tasks/{id}` с JSON (только нужные поля, например `{"description": "Новое описание"}`)
- **Удалить задачу**: DELETE `/tasks/{id}`
- **Поиск задач**: GET `/tasks/search/?q=ключевое_слово`

## Структура проекта

```
Task Manager with JWT/
├── app/
│   ├── __init__.py
│   ├── main.py              # Точка входа FastAPI
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── auth_routes.py  # Маршруты аутентификации
│   │       └── task_routes.py  # Маршруты задач
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py         # Настройки (pydantic-settings)
│   │   └── security.py       # JWT и хэширование паролей
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py           # Базовая модель
│   │   └── session.py        # Сессия БД
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task_model.py           # Модель Task
│   │   └── user_model.py           # Модель User
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth_service.py   # Схемы аутентификации
│   │   └── task_schema.py    # Схемы задач
│   └── services/
│       ├── __init__.py
│       ├── auth_service.py   # Логика аутентификации
│       └── task_service.py   # Логика задач
├── alembic/                  # Миграции БД
├── venv/                     # Виртуальное окружение (не в Git)
├── .env                      # Переменные окружения (не в Git)
└── README.md                 # Этот файл
```

## Разработка

- **Тестирование**: Используйте Swagger UI для ручного тестирования API.
- **Миграции**: После изменений моделей: `alembic revision --autogenerate -m "Описание"` затем `alembic upgrade head`.
- **Линтинг**: Рекомендуется использовать black, flake8 или аналогичные инструменты.



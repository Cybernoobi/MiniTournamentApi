# Tournament Registration System

Микросервис для управления турнирами и регистрации игроков с соблюдением бизнес-правил. Реализован на современном async-стеке Python.

## 🚀 Особенности
- **Полностью асинхронная архитектура** (FastAPI + SQLAlchemy 2.0)
- **Строгая типизация** (mypy + Pydantic)
- **DDD-подход** (разделение на слои)
- **Гибкие лимиты игроков** с валидацией
- **Уникальные email** в рамках турнира
- **Полное покрытие тестами** (pytest + async fixtures)
- **Готово к продакшену** (Docker + PostgreSQL + Alembic)

## 📦 Быстрый старт

Запуск через Docker:
```bash
docker-compose up -d
```

Запуск через poetry:
```bash
poetry install
cd ./app
poetry run python main.py
```

Запуск через Python:
```bash
pip install -r requirements.txt
cd ./app
python main.py
```
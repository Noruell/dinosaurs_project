# 🦕 Динозавры — менеджер базы данных динозавров

Веб-приложение для управления коллекцией динозавров: просмотр, добавление, редактирование, удаление, поиск, фильтрация и загрузка изображений.

---

## 📦 Стек технологий

| Компонент | Технология |
|-----------|------------|
| **Backend** | Python 3.12+, FastAPI |
| **База данных** | PostgreSQL 15+ (SQLAlchemy ORM) |
| **Асинхронность** | asyncpg, асинхронный SQLAlchemy |
| **Миграции** | Alembic |
| **Контейнеризация** | Docker, docker-compose |
| **Фронтенд** | HTML5, CSS3, Vanilla JS |
| **Деплой** | Railway / Render |

---

## 🚀 Быстрый запуск (локально)

### 1. Клонируй репозиторий

```bash
git clone https://github.com/ТВОЙ_НИК/dinosaurs_project.git
cd dinosaurs_project
```
### 2. Создай виртуальное окружение и установи зависимости
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
# или
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

### 3. Запусти PostgreSQL через Docker
```bash
docker-compose up -d db
```
### 4. Запусти приложение
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
### 5. Открой в браузере
```text
http://localhost:8000
```
🐳 Запуск через Docker (всё вместе)
```bash
docker-compose up --build
```
📁 Структура проекта
```text
dinosaurs_project/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI приложение
│   ├── models.py        # SQLAlchemy модели
│   ├── schemas.py       # Pydantic схемы
│   ├── database.py      # Подключение к БД
│   └── templates/
│       └── index.html   # Фронтенд
├── static/
│   └── images/          # Загруженные картинки
├── migrations/          # Alembic миграции
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── Procfile
├── .gitignore
└── README.md
```
🧩 Эндпоинты API
Метод	Эндпоинт	Описание
GET	/dinosaurs	Получить всех динозавров (с фильтрацией)
GET	/dinosaurs/{id}	Получить динозавра по ID
POST	/dinosaurs	Добавить нового динозавра
PUT	/dinosaurs/{id}	Обновить динозавра
DELETE	/dinosaurs/{id}	Удалить динозавра
POST	/dinosaurs/{id}/image	Загрузить изображение
Параметры фильтрации
Параметр	Описание
search	Поиск по имени (частичное совпадение)
period	Фильтр по периоду
limit	Количество записей на странице
offset	Смещение для пагинации

🖼️ Фронтенд
Просмотр всех динозавров в виде карточек

Поиск по имени

Фильтр по периоду

Добавление нового динозавра

Редактирование существующего

Удаление с подтверждением

Загрузка изображений
# Shartash Bot (aiogram)

Telegram-бот на `aiogram` для проекта «Клуб друзей Шарташа» со структурой меню по предоставленному документу.

## Что реализовано

- Главное меню с разделами:
  - О клубе
  - Школа ведущих прогулок
  - Контакты
  - Интервью и проекты
  - Интерактивный путеводитель
- Подменю и карточки с текстом по каждому пункту.
- Навигация:
  - Назад к разделу
  - Назад в главное меню
- Контент вынесен в отдельный модуль `bot/data/content.py`.

## Установка

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Настройка

1. Скопируйте `.env.example` в `.env`.
2. Укажите токен бота:

```env
BOT_TOKEN=your_telegram_bot_token_here
```

## Запуск

```bash
python main.py
```

## Структура проекта

```text
.
├── main.py
├── config.py
├── requirements.txt
└── bot
    ├── data
    │   └── content.py
    ├── handlers
    │   ├── menu.py
    │   └── start.py
    └── keyboards
        └── menu.py
```

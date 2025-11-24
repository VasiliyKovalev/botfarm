# 🚀 Botfarm

**Botfarm** — сервис, который отдает реальные креды пользователя, чтобы использовать его в E2E-тестах для проверки работоспособности функционала.

## ⚙️ Как запустить проект:

1. Клонировать репозиторий и перейти в него в командной строке::

```bash
git clone https://github.com/VasiliyKovalev/botfarm.git
cd botfarm
```

2. Создать файл `.env` и заполнить переменные окружения:

```bash
touch .env
```

```env
API_V1_STR=/api/v1
PROJECT_NAME=botfarm
ENVIRONMENT=local
SECRET_KEY=Secret_key_password

POSTGRES_SERVER=localhost
POSTGRES_USER=botfarm_user
POSTGRES_PASSWORD=botfarm_password
POSTGRES_DB=botfarm_db
POSTGRES_PORT=5432
```

4. Запустить проект с помощью docker-compose:

```bash
docker-compose up
```

## 📄 Документация
После запуска проект будет доступен по адресам:

**API: http://localhost:8000**

**Документация Swagger: http://localhost:8000/docs**

## 🤝 Контакты

Автор: **[Василий Ковалев](https://github.com/VasiliyKovalev)**  
Telegram: [@kovalev97v](https://t.me/kovalev97v)  
Email: [kovalev97v@yandex.com](mailto:kovalev97v@yandex.com)

# Вариант 1

# Первоначальная настройка и запуск проекта TeamFinder 

## 1. Скопировать репозиторий

```bash
git clone ...
```

```bash
cd team-finder-ad
```

## 2. Создание `.env`

Файл `.env` содержит конфиденциальные настройки проекта — ключ Django, параметры БД и другие переменные.  

Особое внимание обратите на строчку `TASK_VERSION=`.
Там должна быть цифра 1.

В репозитории есть пример `.env_example`, который нужно скопировать и заполнить:

```bash
cp .env_example .env
```

После этого откройте `.env` и укажите свои значения.  

| Переменная            | Назначение                                                                                                                                                 |
|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **DJANGO_SECRET_KEY** | Секретный ключ Django, используемый для подписи cookie и токенов. Можно сгенерировать при помощи `get_random_secret_key` из `django.core.management.utils` |
| **DJANGO_DEBUG**      | Режим отладки. Установите `True` во время разработки.                                                                                                      |
| **POSTGRES_DB**       | Имя базы данных PostgreSQL, которую будет использовать Django.                                                                                             |
| **POSTGRES_USER**     | Имя пользователя PostgreSQL.                                                                                                                               |
| **POSTGRES_PASSWORD** | Пароль пользователя PostgreSQL.                                                                                                                            |
| **POSTGRES_HOST**     | Адрес сервера БД. В случае локальной разработки localhost.                                                                                                 |
| **POSTGRES_PORT**     | Порт подключения к БД (по умолчанию `5432`).                                                                                                               |
| **TASK_VERSION**      | Номер варианта вашего задания (1). Используется для определения набора HTML-шаблонов.                                                                          |

---
## 3. Запуск проекта через Docker

Запустить проект
```bash
docker compose up -d --build
```

Применить миграции
```bash
docker compose exec backend python manage.py migrate
```

Создать тестовых пользователей с проектами
```bash
docker compose exec backend python manage.py create_test_users
```

Теперь проект доступен по адресу [http://localhost:8000](http://localhost:8000)

Если возникает ошибка "permission denied while trying to connect to the Docker daemon socket", то может потребоваться добавить `sudo` перед командой

## Проверка на flake8
- ### Через venv
    #### Создать venv
    ```bash
    python -m venv .venv
    ```

    #### Активировать venv
    - на windows
    ```bash
    .\.venv\Scripts\Activate.ps1
    ```
    - на Linux 
    ```bash
    source .venv/bin/activate
    ```

    #### Скачать flake8
    ```bash
    pip install flake8
    ```

    #### Запустить проверку
    ```bash
    flake8 .
    ```
- ### Через docker
    #### Запустить проект
    ```bash
    docker compose up -d --build
    ```

    #### Скачать flake8
    ```bash
    docker compose exec backend pip install flake8
    ```

    #### Запустить проверку
    ```bash
    docker compose exec backend flake8 .
    ```

# Изменения в templates
В `participants.html` и `project_list.html` был добавлен блок для пагинации

# Изменения в css
В `participants.css` и `project_list.css` были добавлены стили для блока с пагинацией

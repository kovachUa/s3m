### 1. Структура Каталогів

```
s3m/
│
├── main.py
├── key.json
├── README.md
└── requirements.txt
```

### 2. `README.md`

```markdown
# s3m

`s3m` — це CLI утиліта для роботи з MinIO, яка підтримує функції шифрування та дешифрування файлів за допомогою GPG.

## Встановлення

### Залежності

1. [MinIO Python SDK](https://pypi.org/project/minio/)
2. [python-gnupg](https://pypi.org/project/python-gnupg/)

Встановіть залежності з `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Налаштування

1. Створіть файл конфігурації `key.json` з наступним вмістом:

    ```json
    {
        "url": "http://localhost:9000",
        "accessKey": "your-access-key",
        "secretKey": "your-secret-key",
        "api": "s3v4"
    }
    ```

    Замініть `url`, `accessKey`, `secretKey` на ваші дані.

## Використання

### Шифрування файлу

```bash
python main.py encrypt <шлях_до_файлу> <email_отримувача> [--upload --bucket <ім'я_бакета>]
```

### Дешифрування файлу

```bash
python main.py decrypt <шлях_до_зашифрованого_файлу> <шлях_до_виходу>
```

### Команди MinIO

- **Створити bucket**:

    ```bash
    python main.py create
    ```

- **Видалити bucket**:

    ```bash
    python main.py delete
    ```

- **Переглянути всі buckets**:

    ```bash
    python main.py buckets
    ```

- **Перелічити об'єкти у bucket**:

    ```bash
    python main.py ls <ім'я_бакета>
    ```

- **Завантажити файл у bucket**:

    ```bash
    python main.py put <ім'я_бакета> <шлях_до_файлу>
    ```

- **Завантажити каталог у bucket**:

    ```bash
    python main.py put-dir <ім'я_бакета> <шлях_до_каталогу>
    ```

## Ліцензія

MIT License. Дивіться файл [LICENSE](LICENSE) для деталей.
```

### 3. `requirements.txt`

```text
minio
python-gnupg
```

### 4. Додатково

- **Файл `key.json`**: Це файл конфігурації для зберігання даних для підключення до MinIO. Забезпечте, що він не потрапить в репозиторій, якщо ви публікуєте його в загальнодоступному репозиторії. Ви можете додати його до `.gitignore`, якщо використовуєте git.



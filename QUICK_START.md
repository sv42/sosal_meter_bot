# 🚀 Швидкий запуск Telegram Code Executor Bot

## ✅ Що вже готово:
- ✅ Встановлено залежності Python
- ✅ Налаштовано кодування для української мови
- ✅ Протестовано виконання Python коду
- ✅ Бот готовий до запуску!

## 🔧 Налаштування токена бота:

### Варіант 1: Через змінну середовища (рекомендовано)
```bash
# Windows PowerShell
$env:BOT_TOKEN="your_bot_token_here"

# Windows CMD
set BOT_TOKEN=your_bot_token_here
```

### Варіант 2: Через файл config.py
Відкрийте `config.py` та замініть `YOUR_BOT_TOKEN_HERE` на ваш токен.

## 🤖 Отримання токена бота:

1. Відкрийте [@BotFather](https://t.me/botfather) в Telegram
2. Надішліть команду `/newbot`
3. Введіть назву бота (наприклад: "My Code Executor")
4. Введіть username бота (наприклад: "my_code_executor_bot")
5. Скопіюйте отриманий токен

## ▶️ Запуск бота:

```bash
python run.py
```

## 📱 Використання:

1. Знайдіть вашого бота в Telegram
2. Надішліть `/start`
3. Надішліть `/language` та оберіть Python
4. Надішліть код для виконання

### Приклад коду:
```python
print("Привіт, світ!")
for i in range(5):
    print(f"Число: {i}")
```

## 🔧 Додавання Ruby (опціонально):

Якщо хочете додати підтримку Ruby:

1. Встановіть Ruby: https://rubyinstaller.org/
2. Відкрийте `config.py`
3. Розкоментуйте секцію Ruby:
```python
SUPPORTED_LANGUAGES = {
    'python': {
        'extension': '.py',
        'command': 'python',
        'name': 'Python'
    },
    'ruby': {
        'extension': '.rb', 
        'command': 'ruby',
        'name': 'Ruby'
    }
}
```

## 🛠️ Команди бота:

- `/start` - Головне меню
- `/help` - Довідка
- `/language` - Вибрати мову програмування
- `/run` - Підготуватися до виконання коду

## ❗ Важливо:

- Бот працює тільки з Python (Ruby можна додати пізніше)
- Максимум 10,000 символів коду
- Час виконання: 10 секунд
- Заборонені небезпечні операції

## 🆘 Якщо щось не працює:

1. Перевірте, що токен встановлено правильно
2. Переконайтеся, що Python встановлено
3. Перевірте, що всі залежності встановлено: `pip install -r requirements.txt`

Готово! 🎉



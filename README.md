# 🤖 Telegram Code Executor Bot

Telegram бот для безпечного виконання коду на Python та Ruby.

## ✨ Можливості

- 🐍 Виконання Python коду
- 💎 Виконання Ruby коду
- 🔒 Безпечне виконання з обмеженнями
- ⏱️ Таймаут виконання (10 секунд)
- 📏 Обмеження на довжину коду (10,000 символів)
- 🛡️ Захист від небезпечних операцій

## 🚀 Встановлення

### 1. Клонування репозиторію
```bash
git clone <your-repo-url>
cd telegram-bot
```

### 2. Встановлення залежностей
```bash
pip install -r requirements.txt
```

### 3. Налаштування бота

#### Варіант 1: Через змінні середовища (рекомендовано)
```bash
# Windows
set BOT_TOKEN=your_bot_token_here

# Linux/Mac
export BOT_TOKEN=your_bot_token_here
```

#### Варіант 2: Через файл config.py
Відкрийте `config.py` та замініть `YOUR_BOT_TOKEN_HERE` на ваш токен бота.

### 4. Отримання токена бота

1. Відкрийте [@BotFather](https://t.me/botfather) в Telegram
2. Надішліть команду `/newbot`
3. Введіть назву бота (наприклад: "My Code Executor")
4. Введіть username бота (наприклад: "my_code_executor_bot")
5. Скопіюйте отриманий токен

### 5. Запуск бота
```bash
python bot.py
```

## 📖 Використання

### Команди бота

- `/start` - Головне меню та привітання
- `/help` - Детальна довідка
- `/language` - Вибрати мову програмування
- `/run` - Підготуватися до виконання коду

### Приклади використання

#### Python код:
```python
print("Привіт, світ!")
for i in range(5):
    print(f"Число: {i}")

# Математичні операції
result = 2 + 2 * 3
print(f"Результат: {result}")

# Робота зі списками
numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers]
print(f"Квадрати: {squares}")
```

#### Ruby код:
```ruby
puts "Привіт, світ!"
5.times do |i|
    puts "Число: #{i}"
end

# Математичні операції
result = 2 + 2 * 3
puts "Результат: #{result}"

# Робота з масивами
numbers = [1, 2, 3, 4, 5]
squares = numbers.map { |x| x**2 }
puts "Квадрати: #{squares}"
```

## 🔒 Безпека

Бот має вбудовані захисти:

### Обмеження:
- Максимум 10,000 символів коду
- Час виконання: 10 секунд
- Максимум 4,000 символів виводу

### Заборонені операції:
- `import os`, `import subprocess`, `import sys`
- `open()`, `file()`, `exec()`, `eval()`
- `system()`, `popen()`, `spawn()`
- `__import__`, `getattr`, `setattr`
- `globals()`, `locals()`

## 🛠️ Налаштування

Ви можете змінити налаштування в файлі `config.py`:

```python
# Обмеження безпеки
MAX_CODE_LENGTH = 10000      # Максимальна довжина коду
EXECUTION_TIMEOUT = 10       # Таймаут виконання в секундах
MAX_OUTPUT_LENGTH = 4000     # Максимальна довжина виводу
```

## 📁 Структура проекту

```
telegram-bot/
├── bot.py              # Основний файл бота
├── code_executor.py    # Виконавець коду
├── config.py           # Конфігурація
├── requirements.txt    # Залежності
└── README.md          # Документація
```

## 🔧 Розробка

### Додавання нових мов програмування

1. Відкрийте `config.py`
2. Додайте нову мову в `SUPPORTED_LANGUAGES`:

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
    },
    'javascript': {  # Новий приклад
        'extension': '.js',
        'command': 'node',
        'name': 'JavaScript'
    }
}
```

3. Оновіть емодзі в `bot.py`:

```python
def _get_lang_emoji(self, language: str) -> str:
    emojis = {
        'python': '🐍',
        'ruby': '💎',
        'javascript': '🟨'  # Новий емодзі
    }
    return emojis.get(language, '📝')
```

## 🐛 Вирішення проблем

### Помилка "BOT_TOKEN не встановлено"
- Перевірте, що токен встановлено в змінних середовища або в `config.py`

### Помилка "Непідтримувана мова"
- Перевірте, що мова додана в `SUPPORTED_LANGUAGES`

### Помилка "Час виконання перевищено"
- Зменшіть складність коду або збільшіть `EXECUTION_TIMEOUT`

### Помилка "Код занадто довгий"
- Зменшіть довжину коду або збільшіть `MAX_CODE_LENGTH`

## 📝 Ліцензія

Цей проект розповсюджується під ліцензією MIT.

## 🤝 Внесок

Вітаються pull requests та звіти про помилки!

## 📞 Підтримка

Якщо у вас виникли питання або проблеми, створіть issue в репозиторії.



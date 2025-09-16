FROM python:3.11-slim

# Встановлюємо системні залежності
RUN apt-get update && apt-get install -y \
    ruby \
    && rm -rf /var/lib/apt/lists/*

# Створюємо робочу директорію
WORKDIR /app

# Копіюємо файли залежностей
COPY requirements.txt .

# Встановлюємо Python залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо код додатку
COPY . .

# Створюємо користувача для безпеки
RUN useradd -m -u 1000 botuser && chown -R botuser:botuser /app
USER botuser

# Запускаємо бота
CMD ["python", "run.py"]



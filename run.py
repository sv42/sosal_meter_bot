#!/usr/bin/env python3
"""
Скрипт для запуску Telegram Code Executor Bot
"""

import os
import sys
from bot import main

if __name__ == '__main__':
    # Перевіряємо наявність токена
    if not os.getenv('BOT_TOKEN') and 'YOUR_BOT_TOKEN_HERE' in open('config.py', encoding='utf-8').read():
        print("❌ Помилка: BOT_TOKEN не встановлено!")
        print("Встановіть змінну середовища BOT_TOKEN або відредагуйте config.py")
        sys.exit(1)
    
    print("🚀 Запуск Telegram Code Executor Bot...")
    print("Для зупинки натисніть Ctrl+C")
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Бот зупинено користувачем")
    except Exception as e:
        print(f"❌ Помилка запуску: {e}")
        sys.exit(1)

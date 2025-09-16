#!/usr/bin/env python3
"""
Скрипт для налаштування Sosal метр бота в BotFather
"""

import asyncio
from telegram import Bot
from config import BOT_TOKEN, BOT_NAME, BOT_DESCRIPTION

async def setup_bot():
    """Налаштовує бота в BotFather"""
    bot = Bot(token=BOT_TOKEN)
    
    try:
        # Отримуємо інформацію про бота
        bot_info = await bot.get_me()
        print(f"✅ Бот підключений: @{bot_info.username}")
        print(f"📝 Назва: {bot_info.first_name}")
        
        print("\n🔧 Налаштування бота в BotFather:")
        print("1. Відкрийте @BotFather в Telegram")
        print("2. Надішліть команди:")
        print(f"   /setdescription")
        print(f"   Виберіть бота: @{bot_info.username}")
        print(f"   Введіть опис: {BOT_DESCRIPTION}")
        print()
        print("   /setcommands")
        print(f"   Виберіть бота: @{bot_info.username}")
        print("   Введіть команди:")
        print("   start - Головне меню")
        print("   help - Довідка")
        print()
        print("   /setuserpic")
        print(f"   Виберіть бота: @{bot_info.username}")
        print("   Надішліть зображення з емодзі 🔮")
        
    except Exception as e:
        print(f"❌ Помилка: {e}")

if __name__ == '__main__':
    asyncio.run(setup_bot())


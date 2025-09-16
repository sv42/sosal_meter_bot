#!/usr/bin/env python3
"""
Бот для відправки одного повідомлення другу
"""

import asyncio
from telegram import Bot
from config import BOT_TOKEN

# ID вашого друга (замініть на справжній ID)
FRIEND_ID = 1276988338  # ЗАМІНІТЬ НА СПРАВЖНІЙ ID ВАШОГО ДРУГА

async def send_message_to_friend():
    """Відправляє повідомлення другу"""
    bot = Bot(token=BOT_TOKEN)
    
    try:
        # Відправляємо повідомлення
        await bot.send_message(
            chat_id=FRIEND_ID,
            text="Міша гей"
        )
        print(f"✅ Повідомлення успішно відправлено другу (ID: {FRIEND_ID})")
        
    except Exception as e:
        print(f"❌ Помилка відправки: {e}")
        print("💡 Перевірте:")
        print("1. Чи правильний ID друга")
        print("2. Чи бот доданий в контакти друга")
        print("3. Чи правильний токен бота")

def main():
    """Головна функція"""
    print("🤖 Бот для відправки повідомлення другу")
    print(f"📱 ID друга: {FRIEND_ID}")
    print("🚀 Відправляю повідомлення...")
    
    asyncio.run(send_message_to_friend())

if __name__ == '__main__':
    main()
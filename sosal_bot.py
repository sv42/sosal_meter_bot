import logging
import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from config import BOT_TOKEN, BOT_NAME, BOT_DESCRIPTION, YES_ANSWERS, NO_ANSWERS, THINKING_EMOJIS

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class SosalMeterBot:
    def __init__(self):
        pass
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обробник команди /start"""
        welcome_text = f"""
🔮 **Ласкаво просимо до {BOT_NAME}!** 🔮

{BOT_DESCRIPTION}

**Як грати:**
1. Натисніть кнопку "Sosal ?"
2. Програма сама визначить відповідь
3. Отримайте магічну відповідь!

**Команди:**
/start - Головне меню
/help - Довідка

🎯 **Натисніть кнопку і отримайте відповідь!**
        """
        
        keyboard = [
            [InlineKeyboardButton("🔮 Sosal ?", callback_data="ask_sosal")],
            [InlineKeyboardButton("❓ Довідка", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=reply_markup)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обробник команди /help"""
        help_text = f"""
📚 **Довідка по {BOT_NAME}**

**Як грати:**
1. Натисніть кнопку "Sosal ?"
2. Програма сама визначить відповідь
3. Отримайте магічну відповідь!

**Команди:**
/start - Головне меню
/help - Ця довідка

**Правила:**
• Просто натисніть кнопку "Sosal ?"
• Програма сама визначить "Так" або "Ні"
• Це гра для розваги, не сприймайте серйозно

🎯 **Гарної гри!**
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обробник натискань на кнопки"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "ask_sosal":
            # Показуємо анімацію "думає"
            await query.edit_message_text(
                f"🔮 **Sosal ?**\n\n"
                f"{random.choice(THINKING_EMOJIS)} Думаю...",
                parse_mode='Markdown'
            )
            
            # Невелика затримка для ефекту
            await asyncio.sleep(2)
            
            # Програма сама визначає відповідь (50/50)
            is_yes = random.choice([True, False])
            if is_yes:
                answer = random.choice(YES_ANSWERS)
            else:
                answer = random.choice(NO_ANSWERS)
            
            # Відправляємо відповідь
            keyboard = [
                [InlineKeyboardButton("🔄 Спитати знову", callback_data="ask_sosal")],
                [InlineKeyboardButton("🏠 Головне меню", callback_data="start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                f"🔮 **Sosal ?**\n\n"
                f"🎯 **Відповідь:** {answer}\n\n"
                f"✨ **Магія завершена!**",
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
        
        elif query.data == "help":
            help_text = f"""
📚 **Довідка по {BOT_NAME}**

**Як грати:**
1. Натисніть кнопку "Sosal ?"
2. Програма сама визначить відповідь
3. Отримайте магічну відповідь!

**Команди:**
/start - Головне меню
/help - Ця довідка

**Правила:**
• Просто натисніть кнопку "Sosal ?"
• Програма сама визначить "Так" або "Ні"
• Це гра для розваги, не сприймайте серйозно

🎯 **Гарної гри!**
            """
            keyboard = [
                [InlineKeyboardButton("🔮 Sosal ?", callback_data="ask_sosal")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(help_text, parse_mode='Markdown', reply_markup=reply_markup)
        
        elif query.data == "start":
            welcome_text = f"""
🔮 **Ласкаво просимо до {BOT_NAME}!** 🔮

{BOT_DESCRIPTION}

**Як грати:**
1. Натисніть кнопку "Sosal ?"
2. Програма сама визначить відповідь
3. Отримайте магічну відповідь!

🎯 **Натисніть кнопку і отримайте відповідь!**
            """
            
            keyboard = [
                [InlineKeyboardButton("🔮 Sosal ?", callback_data="ask_sosal")],
                [InlineKeyboardButton("❓ Довідка", callback_data="help")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(welcome_text, parse_mode='Markdown', reply_markup=reply_markup)
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обробник помилок"""
        logger.error(f"Update {update} caused error {context.error}")
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ Виникла помилка при обробці запиту. Спробуйте ще раз."
            )

def main():
    """Головна функція для запуску бота"""
    if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        print("❌ Помилка: Встановіть BOT_TOKEN в змінних середовища або в config.py")
        return
    
    # Створюємо екземпляр бота
    sosal_bot = SosalMeterBot()
    
    # Створюємо додаток
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Додаємо обробники
    application.add_handler(CommandHandler("start", sosal_bot.start))
    application.add_handler(CommandHandler("help", sosal_bot.help_command))
    application.add_handler(CallbackQueryHandler(sosal_bot.handle_callback))
    
    # Додаємо обробник помилок
    application.add_error_handler(sosal_bot.error_handler)
    
    # Запускаємо бота
    print(f"🔮 Запуск {BOT_NAME}...")
    application.run_polling()

if __name__ == '__main__':
    main()

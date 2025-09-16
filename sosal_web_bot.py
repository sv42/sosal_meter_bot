import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN, BOT_NAME, BOT_DESCRIPTION

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class SosalWebBot:
    def __init__(self):
        # Отримуємо URL з конфігу або використовуємо за замовчуванням
        try:
            from config import WEB_APP_URL
            self.web_app_url = WEB_APP_URL
        except ImportError:
            # За замовчуванням використовуємо ngrok URL (потрібно налаштувати)
            self.web_app_url = "https://your-ngrok-url.ngrok.io/web_app.html"
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обробник команди /start"""
        welcome_text = f"""
🔮 **Ласкаво просимо до {BOT_NAME}!** 🔮

{BOT_DESCRIPTION}

**Як грати:**
1. Натисніть кнопку "Відкрити Sosal метр"
2. В веб-додатку натисніть "Спитати Sosal"
3. Отримайте магічну відповідь!

**Команди:**
/start - Головне меню
/help - Довідка
        """
        
        # Створюємо кнопку з Web App
        keyboard = [
            [InlineKeyboardButton(
                "🔮 Відкрити Sosal метр", 
                web_app=WebAppInfo(url=self.web_app_url)
            )],
            [InlineKeyboardButton("❓ Довідка", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=reply_markup)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обробник команди /help"""
        help_text = f"""
📚 **Довідка по {BOT_NAME}**

**Як грати:**
1. Натисніть кнопку "Відкрити Sosal метр"
2. В веб-додатку натисніть "Спитати Sosal"
3. Отримайте магічну відповідь!

**Особливості:**
• Красивий веб-інтерфейс
• Анімації та ефекти
• Рандомні відповіді
• Можна грати знову

**Команди:**
/start - Головне меню
/help - Ця довідка

🎯 **Гарної гри!**
        """
        
        keyboard = [
            [InlineKeyboardButton(
                "🔮 Відкрити Sosal метр", 
                web_app=WebAppInfo(url=self.web_app_url)
            )]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(help_text, parse_mode='Markdown', reply_markup=reply_markup)
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обробник натискань на кнопки"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "help":
            help_text = f"""
📚 **Довідка по {BOT_NAME}**

**Як грати:**
1. Натисніть кнопку "Відкрити Sosal метр"
2. В веб-додатку натисніть "Спитати Sosal"
3. Отримайте магічну відповідь!

**Особливості:**
• Красивий веб-інтерфейс
• Анімації та ефекти
• Рандомні відповіді
• Можна грати знову

🎯 **Гарної гри!**
            """
            
            keyboard = [
                [InlineKeyboardButton(
                    "🔮 Відкрити Sosal метр", 
                    web_app=WebAppInfo(url=self.web_app_url)
                )]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(help_text, parse_mode='Markdown', reply_markup=reply_markup)
    
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
    sosal_bot = SosalWebBot()
    
    # Створюємо додаток
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Додаємо обробники
    application.add_handler(CommandHandler("start", sosal_bot.start))
    application.add_handler(CommandHandler("help", sosal_bot.help_command))
    application.add_handler(CallbackQueryHandler(sosal_bot.handle_callback))
    
    # Додаємо обробник помилок
    application.add_error_handler(sosal_bot.error_handler)
    
    # Запускаємо бота
    print(f"🔮 Запуск {BOT_NAME} з веб-інтерфейсом...")
    application.run_polling()

if __name__ == '__main__':
    main()

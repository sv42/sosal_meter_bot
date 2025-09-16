import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from code_executor import CodeExecutor
from config import BOT_TOKEN, SUPPORTED_LANGUAGES

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class CodeBot:
    def __init__(self):
        self.executor = CodeExecutor()
        self.user_languages = {}  # Зберігаємо вибрану мову для кожного користувача
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обробник команди /start"""
        welcome_text = """
🤖 **Ласкаво просимо до Code Executor Bot!**

Цей бот дозволяє вам виконувати код на Python.

**Доступні команди:**
/start - Показати це повідомлення
/help - Довідка
/language - Вибрати мову програмування
/run - Виконати код

**Як користуватися:**
1. Оберіть мову програмування командою /language
2. Надішліть код в блоці ``` або звичайним текстом
3. Бот виконає код та поверне результат

**Приклад коду:**
```python
print("Привіт, світ!")
for i in range(3):
    print(f"Число: {i}")
```

**Підтримувані мови:**
• Python 🐍
        """
        await update.message.reply_text(welcome_text, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обробник команди /help"""
        help_text = """
📚 **Довідка по використанню бота**

**Команди:**
/start - Головне меню
/help - Ця довідка
/language - Вибрати мову програмування
/run - Виконати код

**Як надсилати код:**

**Спосіб 1 - В блоці ``` (рекомендовано):**
```python
print("Привіт, світ!")
for i in range(5):
    print(f"Число: {i}")
```

**Спосіб 2 - Звичайний текст:**
print("Привіт, світ!")
for i in range(5):
    print(f"Число: {i}")

**Підтримувані блоки:**
• ```python``` - для Python
• ```py``` - скорочено для Python  
• ``` ``` - загальний блок

**Обмеження:**
• Максимум 10,000 символів коду
• Час виконання: 10 секунд
• Максимум 4,000 символів виводу
• Заборонені небезпечні операції

**Безпека:**
Бот має обмеження для захисту від небезпечного коду.
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def language_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обробник команди /language"""
        keyboard = []
        for lang_code, lang_info in SUPPORTED_LANGUAGES.items():
            keyboard.append([InlineKeyboardButton(
                f"{lang_info['name']} {self._get_lang_emoji(lang_code)}",
                callback_data=f"lang_{lang_code}"
            )])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Оберіть мову програмування:",
            reply_markup=reply_markup
        )
    
    async def language_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обробник вибору мови програмування"""
        query = update.callback_query
        await query.answer()
        
        if query.data.startswith("lang_"):
            language = query.data[5:]  # Видаляємо "lang_"
            user_id = query.from_user.id
            
            if language in SUPPORTED_LANGUAGES:
                self.user_languages[user_id] = language
                lang_name = SUPPORTED_LANGUAGES[language]['name']
                emoji = self._get_lang_emoji(language)
                
                await query.edit_message_text(
                    f"✅ Мову змінено на {lang_name} {emoji}\n\n"
                    f"Тепер надсилайте код для виконання!"
                )
            else:
                await query.edit_message_text("❌ Невідома мова програмування")
    
    async def run_code(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обробник команди /run"""
        user_id = update.from_user.id
        
        if user_id not in self.user_languages:
            await update.message.reply_text(
                "⚠️ Спочатку оберіть мову програмування командою /language"
            )
            return
        
        await update.message.reply_text(
            "📝 Надішліть код для виконання. "
            f"Поточна мова: {SUPPORTED_LANGUAGES[self.user_languages[user_id]]['name']}"
        )
    
    async def handle_code_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обробник повідомлень з кодом"""
        user_id = update.message.from_user.id
        
        if user_id not in self.user_languages:
            await update.message.reply_text(
                "⚠️ Спочатку оберіть мову програмування командою /language"
            )
            return
        
        text = update.message.text
        language = self.user_languages[user_id]
        lang_name = SUPPORTED_LANGUAGES[language]['name']
        
        # Перевіряємо, чи код в блоці ``` ```
        code = self._extract_code_from_message(text, language)
        
        if not code:
            await update.message.reply_text(
                "❌ Не знайдено код для виконання.\n\n"
                "💡 **Як надсилати код:**\n"
                "1. Оберіть мову командою /language\n"
                "2. Надішліть код в блоці:\n"
                "```python\n"
                "print('Привіт, світ!')\n"
                "for i in range(3):\n"
                "    print(f'Число: {i}')\n"
                "```\n"
                "3. Або просто надішліть код без блоку"
            )
            return
        
        # Показуємо, що бот обробляє код
        processing_msg = await update.message.reply_text(
            f"🔄 Виконую {lang_name} код...\n"
            f"```{language}\n{code[:100]}{'...' if len(code) > 100 else ''}\n```",
            parse_mode='Markdown'
        )
        
        try:
            # Виконуємо код
            success, output, error = await self.executor.execute_code(code, language)
            
            # Формуємо відповідь
            if success:
                if output.strip():
                    result_text = f"✅ **Результат виконання {lang_name}:**\n```\n{output}\n```"
                else:
                    result_text = f"✅ **Код {lang_name} виконано успішно!**\n(Немає виводу)"
            else:
                # Додаємо підказку для помилок відступів
                if "IndentationError" in error:
                    result_text = f"❌ **Помилка відступів {lang_name}:**\n```\n{error}\n```\n\n💡 **Підказка:** Перевірте відступи в коді. Використовуйте 4 пробіли для кожного рівня відступу."
                else:
                    result_text = f"❌ **Помилка виконання {lang_name}:**\n```\n{error}\n```"
            
            # Обмежуємо довжину повідомлення
            if len(result_text) > 4000:
                result_text = result_text[:4000] + "\n... (результат обрізано)"
            
            # Видаляємо попереднє повідомлення та надсилаємо результат
            await processing_msg.delete()
            await update.message.reply_text(result_text, parse_mode='Markdown')
            
        except Exception as e:
            await processing_msg.edit_text(f"❌ **Помилка бота:** {str(e)}")
    
    def _extract_code_from_message(self, text: str, language: str) -> str:
        """Витягує код з повідомлення, перевіряючи блоки ``` та звичайний текст"""
        import re
        
        # Шукаємо код в блоках ``` ```
        # Підтримуємо різні варіанти: ```python, ```py, ```, ```{language}
        patterns = [
            rf'```{language}\s*\n(.*?)\n```',
            rf'```py\s*\n(.*?)\n```',
            rf'```\s*\n(.*?)\n```',
            rf'```{language}\s*(.*?)```',
            rf'```py\s*(.*?)```',
            rf'```\s*(.*?)```'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                code = match.group(1).strip()
                if code:
                    return code
        
        # Якщо не знайдено блоків ```, перевіряємо чи весь текст - це код
        # (якщо текст містить ключові слова Python)
        python_keywords = ['print(', 'def ', 'if ', 'for ', 'while ', 'import ', 'class ', 'return ']
        if any(keyword in text for keyword in python_keywords):
            return text.strip()
        
        return ""
    
    def _get_lang_emoji(self, language: str) -> str:
        """Повертає емодзі для мови програмування"""
        emojis = {
            'python': '🐍',
            'ruby': '💎'
        }
        return emojis.get(language, '📝')
    
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
        print("❌ Помилка: Встановіть BOT_TOKEN в змінні середовища або в config.py")
        return
    
    # Створюємо екземпляр бота
    code_bot = CodeBot()
    
    # Створюємо додаток
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Додаємо обробники
    application.add_handler(CommandHandler("start", code_bot.start))
    application.add_handler(CommandHandler("help", code_bot.help_command))
    application.add_handler(CommandHandler("language", code_bot.language_selection))
    application.add_handler(CommandHandler("run", code_bot.run_code))
    application.add_handler(CallbackQueryHandler(code_bot.language_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, code_bot.handle_code_message))
    
    # Додаємо обробник помилок
    application.add_error_handler(code_bot.error_handler)
    
    # Запускаємо бота
    print("🤖 Запуск Code Executor Bot...")
    application.run_polling()

if __name__ == '__main__':
    main()

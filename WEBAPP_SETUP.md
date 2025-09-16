# 🔮 Налаштування Sosal метр Web App

## 📱 Варіанти створення Web App:

### Варіант 1: ngrok (найпростіший)

1. **Завантажте ngrok:**
   - Перейдіть на https://ngrok.com/download
   - Завантажте для вашої ОС
   - Розпакуйте в папку проекту

2. **Запустіть налаштування:**
   ```bash
   python setup_ngrok.py
   ```

3. **Запустіть бота:**
   ```bash
   python sosal_web_bot.py
   ```

### Варіант 2: GitHub Pages (безкоштовний)

1. **Підготуйте файли:**
   ```bash
   python deploy_github.py
   ```

2. **Створіть репозиторій на GitHub:**
   - Перейдіть на https://github.com/new
   - Назва: `sosal-meter-webapp`
   - Публічний репозиторій

3. **Завантажте файли:**
   - Завантажте файли з папки `sosal-meter-webapp`
   - Закомітьте зміни

4. **Увімкніть GitHub Pages:**
   - Settings → Pages
   - Source: Deploy from a branch
   - Branch: main
   - Save

5. **Отримайте URL:**
   - `https://yourusername.github.io/sosal-meter-webapp`

6. **Оновіть config.py:**
   ```python
   WEB_APP_URL = "https://yourusername.github.io/sosal-meter-webapp"
   ```

### Варіант 3: Netlify (альтернатива)

1. **Підготуйте файли:**
   ```bash
   python deploy_github.py
   ```

2. **Перейдіть на https://netlify.com**
3. **Drag & Drop папку `sosal-meter-webapp`**
4. **Отримайте URL:**
   - `https://random-name.netlify.app`

5. **Оновіть config.py:**
   ```python
   WEB_APP_URL = "https://random-name.netlify.app"
   ```

## 🚀 Після налаштування:

1. **Оновіть config.py з правильним URL**
2. **Запустіть бота:**
   ```bash
   python sosal_web_bot.py
   ```

3. **Протестуйте в Telegram:**
   - Відкрийте бота
   - Натисніть "Відкрити Sosal метр"
   - Веб-додаток відкриється в Telegram

## ✨ Результат:

- **В Telegram:** Кнопка "Відкрити Sosal метр"
- **Web App:** Красивий інтерфейс як у Hamster Kombat
- **Функціонал:** Повноцінний веб-додаток з анімаціями

## 🔧 Налаштування бота в BotFather:

1. **Відкрийте @BotFather**
2. **Надішліть команди:**
   ```
   /setdescription
   Виберіть бота
   Введіть: 🔮 Магічний бот з веб-додатком для відповідей "Sosal ?"
   
   /setcommands
   Виберіть бота
   Введіть:
   start - Головне меню
   help - Довідка
   ```

**Готово! Тепер у вас є справжній Web App!** 🔮✨


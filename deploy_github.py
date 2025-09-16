#!/usr/bin/env python3
"""
Скрипт для деплою Sosal метр Web App на GitHub Pages
"""

import os
import shutil
import subprocess

def create_github_repo():
    """Створює GitHub репозиторій для Web App"""
    print("🔮 Створення GitHub репозиторію для Sosal метр...")
    
    # Створюємо папку для деплою
    deploy_dir = "sosal-meter-webapp"
    if os.path.exists(deploy_dir):
        shutil.rmtree(deploy_dir)
    os.makedirs(deploy_dir)
    
    # Копіюємо HTML файл
    shutil.copy("web_app.html", os.path.join(deploy_dir, "index.html"))
    
    # Створюємо README
    readme_content = """# 🔮 Sosal метр Web App

Магічний веб-додаток для відповідей на питання "Sosal ?"

## 🚀 Деплой на GitHub Pages

1. Створіть новий репозиторій на GitHub
2. Завантажте файли з цієї папки
3. Увімкніть GitHub Pages в налаштуваннях репозиторію
4. Отримайте URL: `https://username.github.io/repository-name`

## 📱 Використання

Відкрийте `index.html` в браузері або використовуйте як Web App в Telegram боті.

## ✨ Особливості

- Красивий градієнтний дизайн
- Анімації та ефекти
- Рандомні відповіді
- Адаптивний інтерфейс
"""
    
    with open(os.path.join(deploy_dir, "README.md"), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✅ Файли підготовлено в папці: {deploy_dir}")
    print("\n📋 Наступні кроки:")
    print("1. Створіть новий репозиторій на GitHub")
    print("2. Завантажте файли з папки 'sosal-meter-webapp'")
    print("3. Увімкніть GitHub Pages в налаштуваннях")
    print("4. Отримайте URL: https://username.github.io/repository-name")
    print("5. Використовуйте цей URL в боті")

def main():
    """Головна функція"""
    print("🔮 Підготовка Sosal метр Web App для GitHub Pages...")
    create_github_repo()

if __name__ == '__main__':
    main()


#!/usr/bin/env python3
"""
Скрипт для налаштування ngrok для Sosal метр Web App
"""

import subprocess
import time
import requests
import json
import os
from sosal_web_bot import main as bot_main

def install_ngrok():
    """Встановлює ngrok якщо не встановлено"""
    try:
        result = subprocess.run(['ngrok', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ ngrok вже встановлено")
            return True
    except FileNotFoundError:
        pass
    
    print("📥 Встановлення ngrok...")
    print("1. Завантажте ngrok з https://ngrok.com/download")
    print("2. Розпакуйте в папку проекту")
    print("3. Запустіть скрипт знову")
    return False

def start_ngrok(port=8000):
    """Запускає ngrok для локального сервера"""
    try:
        # Запускаємо ngrok
        ngrok_process = subprocess.Popen([
            'ngrok', 'http', str(port), '--log=stdout'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Чекаємо поки ngrok запуститься
        time.sleep(3)
        
        # Отримуємо URL
        try:
            response = requests.get('http://localhost:4040/api/tunnels')
            data = response.json()
            if data['tunnels']:
                https_url = data['tunnels'][0]['public_url']
                print(f"🌐 ngrok URL: {https_url}")
                return https_url
        except:
            pass
        
        print("❌ Не вдалося отримати ngrok URL")
        return None
        
    except Exception as e:
        print(f"❌ Помилка запуску ngrok: {e}")
        return None

def start_web_server(port=8000):
    """Запускає локальний веб-сервер"""
    import http.server
    import socketserver
    import threading
    
    class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            super().end_headers()
    
    def run_server():
        with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
            print(f"🌐 Локальний сервер запущено на порт {port}")
            httpd.serve_forever()
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    return server_thread

def main():
    """Головна функція"""
    print("🔮 Налаштування Sosal метр Web App з ngrok...")
    
    # Перевіряємо ngrok
    if not install_ngrok():
        return
    
    # Запускаємо локальний сервер
    start_web_server()
    time.sleep(2)
    
    # Запускаємо ngrok
    https_url = start_ngrok()
    if not https_url:
        print("❌ Не вдалося запустити ngrok")
        return
    
    # Оновлюємо URL в боті
    web_app_url = f"{https_url}/web_app.html"
    print(f"📱 Web App URL: {web_app_url}")
    
    # Оновлюємо config.py
    with open('config.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Додаємо URL до конфігу
    if 'WEB_APP_URL' not in content:
        content += f"\n# Web App URL\nWEB_APP_URL = '{web_app_url}'\n"
        with open('config.py', 'w', encoding='utf-8') as f:
            f.write(content)
    
    print("✅ Налаштування завершено!")
    print("🚀 Тепер запустіть бота командою: python sosal_web_bot.py")
    print(f"📱 Web App буде доступний за URL: {web_app_url}")

if __name__ == '__main__':
    main()


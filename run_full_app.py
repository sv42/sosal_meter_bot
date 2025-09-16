#!/usr/bin/env python3
"""
Скрипт для запуску повного додатку Sosal метр (веб-сервер + бот)
"""

import os
import sys
import threading
import time
import subprocess
from sosal_web_bot import main as bot_main

def start_web_server():
    """Запускає веб-сервер в окремому потоці"""
    try:
        import http.server
        import socketserver
        
        class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
            def end_headers(self):
                # Додаємо CORS заголовки для Telegram Web App
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                super().end_headers()
        
        port = 8000
        with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
            print(f"🌐 Веб-сервер запущено на http://localhost:{port}")
            print(f"📱 Web App URL: http://localhost:{port}/web_app.html")
            httpd.serve_forever()
    except Exception as e:
        print(f"❌ Помилка веб-сервера: {e}")

def main():
    """Головна функція"""
    if not os.getenv('BOT_TOKEN') and 'YOUR_BOT_TOKEN_HERE' in open('config.py', encoding='utf-8').read():
        print("❌ Помилка: BOT_TOKEN не встановлено!")
        print("Встановіть змінну середовища BOT_TOKEN або відредагуйте config.py")
        sys.exit(1)
    
    print("🔮 Запуск повного додатку Sosal метр...")
    print("📱 Веб-сервер + Telegram бот")
    print("Для зупинки натисніть Ctrl+C")
    
    try:
        # Запускаємо веб-сервер в окремому потоці
        web_thread = threading.Thread(target=start_web_server, daemon=True)
        web_thread.start()
        
        # Чекаємо, поки сервер запуститься
        time.sleep(2)
        
        # Запускаємо бота
        bot_main()
        
    except KeyboardInterrupt:
        print("\n👋 Додаток зупинено користувачем")
    except Exception as e:
        print(f"❌ Помилка запуску: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()


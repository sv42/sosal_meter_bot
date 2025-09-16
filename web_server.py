#!/usr/bin/env python3
"""
Простий веб-сервер для Sosal метр Web App
"""

import http.server
import socketserver
import webbrowser
import os
import threading
import time

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Додаємо CORS заголовки для Telegram Web App
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def start_web_server(port=8000):
    """Запускає локальний веб-сервер"""
    try:
        with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
            print(f"🌐 Веб-сервер запущено на http://localhost:{port}")
            print(f"📱 Web App URL: http://localhost:{port}/web_app.html")
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"❌ Порт {port} зайнято. Спробуємо порт {port + 1}")
            start_web_server(port + 1)
        else:
            print(f"❌ Помилка запуску сервера: {e}")

if __name__ == '__main__':
    print("🚀 Запуск веб-сервера для Sosal метр...")
    start_web_server()


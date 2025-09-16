import subprocess
import tempfile
import os
import asyncio
from typing import Dict, Tuple
from config import SUPPORTED_LANGUAGES, MAX_CODE_LENGTH, EXECUTION_TIMEOUT, MAX_OUTPUT_LENGTH

class CodeExecutor:
    """Безпечний виконавець коду для Python та Ruby"""
    
    def __init__(self):
        self.supported_languages = SUPPORTED_LANGUAGES
    
    async def execute_code(self, code: str, language: str) -> Tuple[bool, str, str]:
        """
        Виконує код та повертає результат
        
        Args:
            code: Код для виконання
            language: Мова програмування ('python' або 'ruby')
            
        Returns:
            Tuple[bool, str, str]: (успіх, вивід, помилка)
        """
        if language not in self.supported_languages:
            return False, "", f"Непідтримувана мова: {language}"
        
        if len(code) > MAX_CODE_LENGTH:
            return False, "", f"Код занадто довгий. Максимум: {MAX_CODE_LENGTH} символів"
        
        # Перевіряємо на небезпечні команди
        dangerous_patterns = [
            'import os', 'import subprocess', 'import sys',
            'open(', 'file(', 'exec(', 'eval(',
            'system(', 'popen(', 'spawn(',
            '__import__', 'getattr', 'setattr',
            'delattr', 'hasattr', 'globals', 'locals'
        ]
        
        for pattern in dangerous_patterns:
            if pattern in code.lower():
                return False, "", f"Виявлено небезпечний код: {pattern}"
        
        # Простий виправлення відступів - замінюємо табуляції на пробіли
        code = code.replace('\t', '    ')
        
        # Видаляємо зайві пробіли на початку рядків
        lines = code.split('\n')
        fixed_lines = []
        
        for line in lines:
            # Видаляємо пробіли на початку, але зберігаємо структуру
            stripped = line.strip()
            if not stripped:  # Порожній рядок
                fixed_lines.append('')
                continue
            
            # Додаємо базовий відступ для рядків, що починаються з ключових слів
            if stripped.startswith(('if ', 'for ', 'while ', 'def ', 'class ', 'try:', 'except', 'finally:', 'with ', 'elif ', 'else:')):
                fixed_lines.append(stripped)
            else:
                # Для звичайних рядків додаємо базовий відступ
                fixed_lines.append('    ' + stripped)
        
        # Оновлюємо код з виправленими відступами
        code = '\n'.join(fixed_lines)
        
        try:
            # Створюємо тимчасовий файл з правильним кодуванням
            with tempfile.NamedTemporaryFile(
                mode='w', 
                suffix=self.supported_languages[language]['extension'],
                delete=False,
                encoding='utf-8'
            ) as temp_file:
                temp_file.write(code)
                temp_file_path = temp_file.name
            
            # Виконуємо код
            command = [self.supported_languages[language]['command'], temp_file_path]
            
            # Встановлюємо змінні середовища для правильного кодування
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=tempfile.gettempdir(),  # Виконуємо в тимчасовій директорії
                env=env
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), 
                    timeout=EXECUTION_TIMEOUT
                )
                
                # Декодуємо вивід з обробкою помилок кодування
                try:
                    output = stdout.decode('utf-8')
                except UnicodeDecodeError:
                    output = stdout.decode('cp1251', errors='ignore')
                
                try:
                    error = stderr.decode('utf-8')
                except UnicodeDecodeError:
                    error = stderr.decode('cp1251', errors='ignore')
                
                # Обмежуємо довжину виводу
                if len(output) > MAX_OUTPUT_LENGTH:
                    output = output[:MAX_OUTPUT_LENGTH] + "\n... (вивід обрізано)"
                
                if len(error) > MAX_OUTPUT_LENGTH:
                    error = error[:MAX_OUTPUT_LENGTH] + "\n... (помилка обрізано)"
                
                success = process.returncode == 0
                
                return success, output, error
                
            except asyncio.TimeoutError:
                process.kill()
                return False, "", f"Час виконання перевищено ({EXECUTION_TIMEOUT} секунд)"
                
        except Exception as e:
            return False, "", f"Помилка виконання: {str(e)}"
        
        finally:
            # Видаляємо тимчасовий файл
            try:
                if 'temp_file_path' in locals():
                    os.unlink(temp_file_path)
            except:
                pass
    
    def get_supported_languages(self) -> Dict:
        """Повертає список підтримуваних мов програмування"""
        return self.supported_languages

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Система ежедневных уведомлений ZODI
Поддерживает Desktop (Windows/macOS/Linux) и Mobile платформы
"""

import os
import sys
import platform
import json
import schedule
import time
from datetime import datetime, date
from typing import Optional, Dict, Any
import threading

# Импорты для системных уведомлений
try:
    import win10toast
    WINDOWS_TOAST_AVAILABLE = True
except ImportError:
    WINDOWS_TOAST_AVAILABLE = False

try:
    import pync
    MACOS_NOTIFICATIONS_AVAILABLE = True
except ImportError:
    MACOS_NOTIFICATIONS_AVAILABLE = False

# Импорты для Linux
try:
    import subprocess
    LINUX_NOTIFICATIONS_AVAILABLE = True
except ImportError:
    LINUX_NOTIFICATIONS_AVAILABLE = False

from .zodiac_calculator import get_zodiac_sign
from .daily_manager import DailyPredictionManager
from .zodiac_data import ZODIAC_DATA


class NotificationSystem:
    """Система уведомлений для ZODI"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.daily_manager = DailyPredictionManager()
        self.is_running = False
        self.notification_thread = None
        
        # Настройки уведомлений
        self.settings = {
            'enabled': True,
            'time': '07:00',
            'show_detailed': True,
            'sound': True,
            'duration': 10  # секунд
        }
    
    def get_daily_prediction_for_sign(self, zodiac_sign: str) -> Dict[str, Any]:
        """Получить предсказание на сегодня для знака зодиака"""
        try:
            # Получаем предсказание через daily_manager
            prediction = self.daily_manager.get_daily_general_prediction(zodiac_sign)
            
            # Формируем структурированное предсказание
            return {
                'sign': zodiac_sign,
                'date': date.today().strftime('%d.%m.%Y'),
                'general': prediction.get('general', ''),
                'love': prediction.get('love', ''),
                'career': prediction.get('career', ''),
                'health': prediction.get('health', ''),
                'finance': prediction.get('finance', ''),
                'advice': prediction.get('advice', ''),
                'opportunities': prediction.get('opportunities', ''),
                'warnings': prediction.get('warnings', '')
            }
        except Exception as e:
            print(f"Ошибка получения предсказания: {e}")
            return {
                'sign': zodiac_sign,
                'date': date.today().strftime('%d.%m.%Y'),
                'general': 'Сегодня звезды приготовили для вас особые сюрпризы!',
                'love': 'В любви вас ждут приятные моменты.',
                'career': 'Карьера развивается в положительном направлении.',
                'health': 'Здоровье требует внимания.',
                'finance': 'Финансы стабильны.',
                'advice': 'Слушайте свою интуицию.',
                'opportunities': 'Новые возможности на горизонте.',
                'warnings': 'Будьте осторожны с важными решениями.'
            }
    
    def create_notification_content(self, prediction: Dict[str, Any]) -> Dict[str, str]:
        """Создать контент для уведомления"""
        sign_symbol = ZODIAC_DATA.get(prediction['sign'], {}).get('symbol', '🔮')
        
        # Основное уведомление
        title = f"{sign_symbol} {prediction['sign']} - {prediction['date']}"
        
        if self.settings['show_detailed']:
            # Детальное уведомление с несколькими категориями
            content = f"🔮 {prediction['general']}\n\n"
            content += f"💖 Любовь: {prediction['love']}\n"
            content += f"💼 Карьера: {prediction['career']}\n"
            content += f"💰 Финансы: {prediction['finance']}"
        else:
            # Краткое уведомление
            content = f"🔮 {prediction['general']}"
        
        return {
            'title': title,
            'content': content,
            'icon': self._get_notification_icon_path()
        }
    
    def _get_notification_icon_path(self) -> Optional[str]:
        """Получить путь к иконке для уведомления"""
        # Ищем иконку в директории assets
        icon_paths = [
            'zodi_app/assets/icon.ico',
            'assets/icon.ico',
            'icon.ico'
        ]
        
        for path in icon_paths:
            if os.path.exists(path):
                return os.path.abspath(path)
        
        return None
    
    def show_windows_notification(self, title: str, content: str, icon_path: Optional[str] = None):
        """Показать уведомление в Windows"""
        if not WINDOWS_TOAST_AVAILABLE:
            print("win10toast не установлен. Установите: pip install win10toast")
            return False
        
        try:
            toaster = win10toast.ToastNotifier()
            toaster.show_toast(
                title=title,
                msg=content,
                icon_path=icon_path,
                duration=self.settings['duration'],
                threaded=True
            )
            return True
        except Exception as e:
            print(f"Ошибка показа уведомления Windows: {e}")
            return False
    
    def show_macos_notification(self, title: str, content: str, icon_path: Optional[str] = None):
        """Показать уведомление в macOS"""
        if not MACOS_NOTIFICATIONS_AVAILABLE:
            print("pync не установлен. Установите: pip install pync")
            return False
        
        try:
            pync.notify(
                message=content,
                title=title,
                appIcon=icon_path,
                sound='default' if self.settings['sound'] else None
            )
            return True
        except Exception as e:
            print(f"Ошибка показа уведомления macOS: {e}")
            return False
    
    def show_linux_notification(self, title: str, content: str, icon_path: Optional[str] = None):
        """Показать уведомление в Linux"""
        if not LINUX_NOTIFICATIONS_AVAILABLE:
            print("Системные уведомления Linux недоступны")
            return False
        
        try:
            cmd = ['notify-send', title, content]
            if icon_path and os.path.exists(icon_path):
                cmd.extend(['-i', icon_path])
            
            if self.settings['duration']:
                cmd.extend(['-t', str(self.settings['duration'] * 1000)])
            
            subprocess.run(cmd, check=True)
            return True
        except Exception as e:
            print(f"Ошибка показа уведомления Linux: {e}")
            return False
    
    def show_notification(self, title: str, content: str, icon_path: Optional[str] = None) -> bool:
        """Показать системное уведомление в зависимости от ОС"""
        if not self.settings['enabled']:
            return False
        
        if self.system == 'windows':
            return self.show_windows_notification(title, content, icon_path)
        elif self.system == 'darwin':  # macOS
            return self.show_macos_notification(title, content, icon_path)
        elif self.system == 'linux':
            return self.show_linux_notification(title, content, icon_path)
        else:
            print(f"Неподдерживаемая ОС: {self.system}")
            return False
    
    def send_daily_notification(self, user_zodiac_sign: str):
        """Отправить ежедневное уведомление для знака зодиака"""
        try:
            # Получаем предсказание
            prediction = self.get_daily_prediction_for_sign(user_zodiac_sign)
            
            # Создаем контент уведомления
            notification_content = self.create_notification_content(prediction)
            
            # Показываем уведомление
            success = self.show_notification(
                title=notification_content['title'],
                content=notification_content['content'],
                icon_path=notification_content['icon']
            )
            
            if success:
                print(f"Уведомление отправлено для {user_zodiac_sign}")
            else:
                print(f"Не удалось отправить уведомление для {user_zodiac_sign}")
            
            return success
            
        except Exception as e:
            print(f"Ошибка отправки уведомления: {e}")
            return False
    
    def start_daily_scheduler(self, user_zodiac_sign: str):
        """Запустить планировщик ежедневных уведомлений"""
        if self.is_running:
            print("Планировщик уже запущен")
            return
        
        # Настраиваем расписание
        schedule.every().day.at(self.settings['time']).do(
            self.send_daily_notification, user_zodiac_sign
        )
        
        self.is_running = True
        
        def run_scheduler():
            while self.is_running:
                schedule.run_pending()
                time.sleep(60)  # Проверяем каждую минуту
        
        # Запускаем планировщик в отдельном потоке
        self.notification_thread = threading.Thread(target=run_scheduler, daemon=True)
        self.notification_thread.start()
        
        print(f"Планировщик уведомлений запущен. Время: {self.settings['time']}")
    
    def stop_daily_scheduler(self):
        """Остановить планировщик уведомлений"""
        self.is_running = False
        schedule.clear()
        print("Планировщик уведомлений остановлен")
    
    def update_settings(self, new_settings: Dict[str, Any]):
        """Обновить настройки уведомлений"""
        self.settings.update(new_settings)
        print(f"Настройки уведомлений обновлены: {self.settings}")
    
    def test_notification(self, user_zodiac_sign: str):
        """Тестовое уведомление"""
        print("Отправка тестового уведомления...")
        return self.send_daily_notification(user_zodiac_sign)
    
    def save_settings_to_file(self, file_path: str = "notification_settings.json"):
        """Сохранить настройки в файл"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
            print(f"Настройки сохранены в {file_path}")
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")
    
    def load_settings_from_file(self, file_path: str = "notification_settings.json"):
        """Загрузить настройки из файла"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.settings.update(json.load(f))
                print(f"Настройки загружены из {file_path}")
        except Exception as e:
            print(f"Ошибка загрузки настроек: {e}")


class MobileNotificationSystem:
    """Система уведомлений для мобильных платформ"""
    
    def __init__(self):
        self.fcm_available = False
        self.apns_available = False
        
        # Проверяем доступность сервисов
        self._check_mobile_services()
    
    def _check_mobile_services(self):
        """Проверить доступность мобильных сервисов уведомлений"""
        try:
            # Проверка Firebase Cloud Messaging
            import firebase_admin
            from firebase_admin import messaging
            self.fcm_available = True
        except ImportError:
            print("Firebase не установлен. Установите: pip install firebase-admin")
        
        try:
            # Проверка Apple Push Notifications
            import apns2
            self.apns_available = True
        except ImportError:
            print("APNS не установлен. Установите: pip install apns2")
    
    def send_android_notification(self, device_token: str, title: str, content: str):
        """Отправить уведомление на Android через FCM"""
        if not self.fcm_available:
            print("FCM недоступен")
            return False
        
        try:
            from firebase_admin import messaging
            
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=content
                ),
                token=device_token
            )
            
            response = messaging.send(message)
            print(f"Уведомление отправлено: {response}")
            return True
            
        except Exception as e:
            print(f"Ошибка отправки FCM уведомления: {e}")
            return False
    
    def send_ios_notification(self, device_token: str, title: str, content: str):
        """Отправить уведомление на iOS через APNS"""
        if not self.apns_available:
            print("APNS недоступен")
            return False
        
        try:
            from apns2 import APNsClient, Notification
            
            client = APNsClient()
            
            notification = Notification(
                device_token=device_token,
                alert=title,
                body=content,
                badge=1,
                sound='default'
            )
            
            client.send_notification(notification)
            print("Уведомление отправлено на iOS")
            return True
            
        except Exception as e:
            print(f"Ошибка отправки APNS уведомления: {e}")
            return False


def create_system_scheduler_script(user_zodiac_sign: str, script_path: str = "zodi_notifications.py"):
    """Создать скрипт для системного планировщика"""
    
    script_content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Автоматический скрипт уведомлений ZODI
Запускается системным планировщиком
"""

import sys
import os

# Добавляем путь к модулям ZODI
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from zodi_app.core.notification_system import NotificationSystem

def main():
    notification_system = NotificationSystem()
    
    # Загружаем настройки
    notification_system.load_settings_from_file()
    
    # Отправляем уведомление
    success = notification_system.send_daily_notification("{user_zodiac_sign}")
    
    if success:
        print("Уведомление ZODI отправлено успешно")
    else:
        print("Ошибка отправки уведомления ZODI")

if __name__ == "__main__":
    main()
'''
    
    try:
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        print(f"Скрипт планировщика создан: {script_path}")
        return script_path
    except Exception as e:
        print(f"Ошибка создания скрипта: {e}")
        return None


def setup_windows_task_scheduler(user_zodiac_sign: str, script_path: str):
    """Настроить планировщик задач Windows"""
    try:
        import subprocess
        
        # Создаем задачу в планировщике Windows
        task_name = "ZODI Daily Notifications"
        command = f'python "{script_path}"'
        
        # Создаем XML для задачи
        xml_content = f'''<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>2024-01-01T07:00:00</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
  </Triggers>
  <Actions>
    <Exec>
      <Command>python</Command>
      <Arguments>"{script_path}"</Arguments>
    </Exec>
  </Actions>
</Task>'''
        
        # Сохраняем XML
        xml_path = "zodi_task.xml"
        with open(xml_path, 'w', encoding='utf-16') as f:
            f.write(xml_content)
        
        # Импортируем задачу
        subprocess.run(['schtasks', '/create', '/tn', task_name, '/xml', xml_path], check=True)
        
        print(f"Задача Windows создана: {task_name}")
        print("Уведомления будут приходить каждый день в 7:00")
        
        return True
        
    except Exception as e:
        print(f"Ошибка настройки Windows планировщика: {e}")
        return False


def setup_macos_launchd(user_zodiac_sign: str, script_path: str):
    """Настроить Launchd для macOS"""
    try:
        plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.zodi.notifications</string>
    <key>ProgramArguments</key>
    <array>
        <string>python3</string>
        <string>{script_path}</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>7</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>'''
        
        plist_path = os.path.expanduser("~/Library/LaunchAgents/com.zodi.notifications.plist")
        
        with open(plist_path, 'w') as f:
            f.write(plist_content)
        
        # Загружаем задачу
        subprocess.run(['launchctl', 'load', plist_path], check=True)
        
        print(f"Launchd задача создана: {plist_path}")
        print("Уведомления будут приходить каждый день в 7:00")
        
        return True
        
    except Exception as e:
        print(f"Ошибка настройки macOS Launchd: {e}")
        return False


def setup_linux_cron(user_zodiac_sign: str, script_path: str):
    """Настроить Cron для Linux"""
    try:
        # Добавляем задачу в crontab
        cron_entry = f"0 7 * * * python3 {script_path}"
        
        # Получаем текущий crontab
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        current_crontab = result.stdout if result.returncode == 0 else ""
        
        # Добавляем новую задачу
        if "zodi_notifications.py" not in current_crontab:
            new_crontab = current_crontab + f"\n{cron_entry}\n"
            
            # Устанавливаем новый crontab
            subprocess.run(['crontab', '-'], input=new_crontab, text=True, check=True)
            
            print("Cron задача добавлена")
            print("Уведомления будут приходить каждый день в 7:00")
            
            return True
        else:
            print("Cron задача уже существует")
            return True
            
    except Exception as e:
        print(f"Ошибка настройки Linux Cron: {e}")
        return False


if __name__ == "__main__":
    # Пример использования
    notification_system = NotificationSystem()
    
    # Тестовое уведомление
    notification_system.test_notification("Скорпион")

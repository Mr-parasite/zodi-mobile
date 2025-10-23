#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZODI Mobile - Космические предсказания для мобильных устройств
"""

import os
import sys
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Импорты экранов
from ui.screens.splash_screen import SplashScreen
from ui.screens.input_screen import InputScreen
from ui.screens.results_screen import ResultsScreen
from ui.screens.predictions_screen import PredictionsScreen
from ui.screens.compatibility_screen import CompatibilityScreen
from ui.screens.profile_screen import ProfileScreen

# Импорты core модулей
from core.zodiac_calculator import get_zodiac_sign
from core.daily_manager import get_daily_general_prediction
from core.compatibility_calculator import CompatibilityCalculator
from core.user_profile import UserProfile
from core.notification_system import NotificationSystem

# Импорты утилит
from utils.storage import MobileStorage
from ui.themes.zodi_theme import ZodiTheme


class ZodiMobileApp(App):
    """Главное приложение ZODI Mobile"""
    
    def build(self):
        """Создание интерфейса приложения"""
        # Настройка темы
        self.theme = ZodiTheme()
        
        # Инициализация компонентов
        self.storage = MobileStorage()
        self.user_profile = UserProfile()
        self.compatibility_calculator = CompatibilityCalculator()
        self.notification_system = NotificationSystem()
        
        # Создание главного экрана
        self.main_screen = SplashScreen()
        
        # Настройка окна
        Window.clearcolor = self.theme.BACKGROUND_PRIMARY
        
        return self.main_screen
    
    def on_start(self):
        """Вызывается при запуске приложения"""
        # Загружаем профиль пользователя
        if self.user_profile.has_profile():
            profile_data = self.user_profile.get_profile()
            print(f"Профиль загружен: {profile_data}")
        
        # Настраиваем уведомления
        self.notification_system.load_settings_from_file()
        
        # Переход к главному экрану через 3 секунды
        Clock.schedule_once(self.goto_main_screen, 3)
    
    def goto_main_screen(self, dt):
        """Переход к главному экрану"""
        if self.user_profile.has_profile():
            # Если есть профиль, переходим к результатам
            self.root.clear_widgets()
            self.root.add_widget(ResultsScreen())
        else:
            # Если нет профиля, переходим к вводу
            self.root.clear_widgets()
            self.root.add_widget(InputScreen())
    
    def calculate_zodiac(self, day, month):
        """Вычислить знак зодиака"""
        try:
            zodiac_sign = get_zodiac_sign(int(day), int(month))
            return zodiac_sign
        except Exception as e:
            print(f"Ошибка вычисления знака зодиака: {e}")
            return None
    
    def get_daily_prediction(self, zodiac_sign):
        """Получить предсказание на сегодня"""
        try:
            prediction = get_daily_general_prediction(zodiac_sign)
            return prediction
        except Exception as e:
            print(f"Ошибка получения предсказания: {e}")
            return "Сегодня звезды приготовили для вас особые сюрпризы!"
    
    def get_detailed_predictions(self, zodiac_sign):
        """Получить детальные предсказания"""
        try:
            # Здесь будет логика получения детальных предсказаний
            return {
                'love': 'В любви вас ждут приятные моменты.',
                'career': 'Карьера развивается в положительном направлении.',
                'health': 'Здоровье требует внимания.',
                'finance': 'Финансы стабильны.',
                'advice': 'Слушайте свою интуицию.',
                'opportunities': 'Новые возможности на горизонте.',
                'warnings': 'Будьте осторожны с важными решениями.'
            }
        except Exception as e:
            print(f"Ошибка получения детальных предсказаний: {e}")
            return {}
    
    def calculate_compatibility(self, sign1, sign2, relationship_type):
        """Вычислить совместимость"""
        try:
            compatibility = self.compatibility_calculator.calculate_compatibility(
                sign1, sign2, relationship_type
            )
            return compatibility
        except Exception as e:
            print(f"Ошибка вычисления совместимости: {e}")
            return {'percentage': 50, 'description': 'Средняя совместимость'}
    
    def save_profile(self, profile_data):
        """Сохранить профиль пользователя"""
        try:
            self.user_profile.save_profile(profile_data)
            print("Профиль сохранен успешно")
            return True
        except Exception as e:
            print(f"Ошибка сохранения профиля: {e}")
            return False
    
    def setup_notifications(self):
        """Настроить уведомления"""
        try:
            if self.user_profile.has_profile():
                profile_data = self.user_profile.get_profile()
                zodiac_sign = profile_data.get('zodiac_sign', 'Скорпион')
                self.notification_system.start_daily_scheduler(zodiac_sign)
                print("Уведомления настроены")
        except Exception as e:
            print(f"Ошибка настройки уведомлений: {e}")
    
    def test_notification(self):
        """Тестовое уведомление"""
        try:
            if self.user_profile.has_profile():
                profile_data = self.user_profile.get_profile()
                zodiac_sign = profile_data.get('zodiac_sign', 'Скорпион')
                return self.notification_system.test_notification(zodiac_sign)
        except Exception as e:
            print(f"Ошибка тестового уведомления: {e}")
            return False


if __name__ == '__main__':
    ZodiMobileApp().run()

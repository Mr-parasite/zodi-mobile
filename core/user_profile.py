#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZODI - Система персонального профиля пользователя
Сохранение и загрузка данных пользователя с шифрованием
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

try:
    from .encryption import EncryptionManager
except ImportError:
    from encryption import EncryptionManager

class UserProfile:
    """Класс для управления персональным профилем пользователя"""
    
    def __init__(self):
        # Создаем директорию data если не существует
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        self.profile_file = os.path.join(data_dir, 'user_profile.json')
        self.encryption_manager = EncryptionManager()
        
        # Структура данных пользователя
        self.user_data = {
            'name': '',
            'birth_date': {
                'day': 0,
                'month': 0,
                'year': 0
            },
            'birth_place': '',
            'zodiac_sign': '',
            'element': '',
            'ruling_planet': '',
            'favorite_predictions': [],
            'compatibility_history': [],
            'settings': {
                'notifications': True,
                'theme': 'dark',
                'language': 'ru',
                'auto_save': True,
                'show_symbols': True,
                'detailed_predictions': True
            },
            'created_at': '',
            'last_updated': ''
        }
        
        # Загружаем существующий профиль или создаем новый
        self.load_profile()
    
    def load_profile(self) -> bool:
        """Загрузить профиль из файла"""
        try:
            if os.path.exists(self.profile_file):
                print(f"Загрузка профиля из {self.profile_file}")
                with open(self.profile_file, 'r', encoding='utf-8') as f:
                    encrypted_data = f.read()
                
                # Расшифровываем данные
                decrypted_data = self.encryption_manager.decrypt(encrypted_data)
                if decrypted_data:
                    self.user_data = json.loads(decrypted_data)
                    print("Профиль успешно загружен")
                    return True
                else:
                    print("Не удалось расшифровать профиль")
            else:
                print("Файл профиля не найден, создается новый")
        except Exception as e:
            print(f"Ошибка загрузки профиля: {e}")
        
        # Если загрузка не удалась, создаем новый профиль
        self._initialize_new_profile()
        return False
    
    def save_profile(self) -> bool:
        """Сохранить профиль в файл"""
        try:
            print("Сохранение профиля...")
            # Обновляем время последнего изменения
            self.user_data['last_updated'] = datetime.now().isoformat()
            
            # Шифруем данные
            json_data = json.dumps(self.user_data, ensure_ascii=False, indent=2)
            encrypted_data = self.encryption_manager.encrypt(json_data)
            
            if encrypted_data:
                # Создаем директорию если не существует
                os.makedirs(os.path.dirname(self.profile_file), exist_ok=True)
                
                with open(self.profile_file, 'w', encoding='utf-8') as f:
                    f.write(encrypted_data)
                print(f"Профиль сохранен в {self.profile_file}")
                return True
            else:
                print("Не удалось зашифровать данные профиля")
        except Exception as e:
            print(f"Ошибка сохранения профиля: {e}")
            import traceback
            traceback.print_exc()
        
        return False
    
    def _initialize_new_profile(self):
        """Инициализировать новый профиль"""
        self.user_data['created_at'] = datetime.now().isoformat()
        self.user_data['last_updated'] = datetime.now().isoformat()
    
    def set_personal_info(self, name: str, birth_day: int, birth_month: int, 
                         birth_year: int = 0, birth_place: str = ''):
        """Установить персональную информацию"""
        self.user_data['name'] = name
        self.user_data['birth_date'] = {
            'day': birth_day,
            'month': birth_month,
            'year': birth_year
        }
        self.user_data['birth_place'] = birth_place
        
        # Автоматически сохраняем если включена автозапись
        if self.user_data['settings']['auto_save']:
            self.save_profile()
    
    def set_zodiac_info(self, zodiac_sign: str, element: str = '', ruling_planet: str = ''):
        """Установить астрологическую информацию"""
        self.user_data['zodiac_sign'] = zodiac_sign
        self.user_data['element'] = element
        self.user_data['ruling_planet'] = ruling_planet
        
        # Автоматически сохраняем если включена автозапись
        if self.user_data['settings']['auto_save']:
            self.save_profile()
    
    def add_favorite_prediction(self, prediction_type: str, prediction_text: str):
        """Добавить предсказание в избранное"""
        favorite = {
            'type': prediction_type,
            'text': prediction_text,
            'date': datetime.now().isoformat()
        }
        
        # Ограничиваем количество избранных предсказаний
        if len(self.user_data['favorite_predictions']) >= 50:
            self.user_data['favorite_predictions'].pop(0)  # Удаляем самое старое
        
        self.user_data['favorite_predictions'].append(favorite)
        
        if self.user_data['settings']['auto_save']:
            self.save_profile()
    
    def add_compatibility_result(self, sign1: str, sign2: str, relationship_type: str, 
                               score: int, description: str):
        """Добавить результат совместимости в историю"""
        result = {
            'sign1': sign1,
            'sign2': sign2,
            'relationship_type': relationship_type,
            'score': score,
            'description': description,
            'date': datetime.now().isoformat()
        }
        
        # Ограничиваем количество записей в истории
        if len(self.user_data['compatibility_history']) >= 100:
            self.user_data['compatibility_history'].pop(0)  # Удаляем самую старую
        
        self.user_data['compatibility_history'].append(result)
        
        if self.user_data['settings']['auto_save']:
            self.save_profile()
    
    def update_setting(self, setting_name: str, value: Any):
        """Обновить настройку"""
        if setting_name in self.user_data['settings']:
            self.user_data['settings'][setting_name] = value
            
            if self.user_data['settings']['auto_save']:
                self.save_profile()
    
    def get_setting(self, setting_name: str, default_value: Any = None) -> Any:
        """Получить значение настройки"""
        return self.user_data['settings'].get(setting_name, default_value)
    
    def get_personal_info(self) -> Dict[str, Any]:
        """Получить персональную информацию"""
        return {
            'name': self.user_data['name'],
            'birth_date': self.user_data['birth_date'],
            'birth_place': self.user_data['birth_place']
        }
    
    def get_zodiac_info(self) -> Dict[str, str]:
        """Получить астрологическую информацию"""
        return {
            'zodiac_sign': self.user_data['zodiac_sign'],
            'element': self.user_data['element'],
            'ruling_planet': self.user_data['ruling_planet']
        }
    
    def get_favorite_predictions(self, limit: int = 10) -> list:
        """Получить избранные предсказания"""
        return self.user_data['favorite_predictions'][-limit:]
    
    def get_compatibility_history(self, limit: int = 10) -> list:
        """Получить историю совместимости"""
        return self.user_data['compatibility_history'][-limit:]
    
    def get_all_settings(self) -> Dict[str, Any]:
        """Получить все настройки"""
        return self.user_data['settings'].copy()
    
    def has_profile(self) -> bool:
        """Проверить, есть ли сохраненный профиль"""
        return bool(self.user_data['name'] or self.user_data['zodiac_sign'])
    
    def clear_profile(self):
        """Очистить профиль"""
        self._initialize_new_profile()
        self.user_data['name'] = ''
        self.user_data['birth_date'] = {'day': 0, 'month': 0, 'year': 0}
        self.user_data['birth_place'] = ''
        self.user_data['zodiac_sign'] = ''
        self.user_data['element'] = ''
        self.user_data['ruling_planet'] = ''
        self.user_data['favorite_predictions'] = []
        self.user_data['compatibility_history'] = []
        
        # Сохраняем очищенный профиль
        self.save_profile()
    
    def export_profile(self, file_path: str) -> bool:
        """Экспортировать профиль в файл"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.user_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Ошибка экспорта профиля: {e}")
            return False
    
    def import_profile(self, file_path: str) -> bool:
        """Импортировать профиль из файла"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_data = json.load(f)
            
            # Проверяем структуру данных
            if self._validate_profile_structure(imported_data):
                self.user_data = imported_data
                self.save_profile()
                return True
        except Exception as e:
            print(f"Ошибка импорта профиля: {e}")
        
        return False
    
    def _validate_profile_structure(self, data: Dict[str, Any]) -> bool:
        """Проверить структуру профиля"""
        required_fields = ['name', 'birth_date', 'zodiac_sign', 'settings']
        return all(field in data for field in required_fields)
    
    def get_profile_summary(self) -> Dict[str, Any]:
        """Получить краткую сводку профиля"""
        return {
            'name': self.user_data['name'],
            'zodiac_sign': self.user_data['zodiac_sign'],
            'element': self.user_data['element'],
            'favorites_count': len(self.user_data['favorite_predictions']),
            'compatibility_tests': len(self.user_data['compatibility_history']),
            'created_at': self.user_data['created_at'],
            'last_updated': self.user_data['last_updated']
        }

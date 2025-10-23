#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Мобильное хранилище для ZODI
"""

from kivy.storage.jsonstore import JsonStore
from kivy.app import App
import os


class MobileStorage:
    """Мобильное хранилище данных"""
    
    def __init__(self):
        app = App.get_running_app()
        data_dir = app.user_data_dir
        self.store = JsonStore(os.path.join(data_dir, 'zodi_data.json'))
    
    def save_profile(self, profile_data):
        """Сохранить профиль"""
        self.store.put('profile', **profile_data)
    
    def get_profile(self):
        """Получить профиль"""
        return self.store.get('profile') if self.store.exists('profile') else None
    
    def save_settings(self, settings):
        """Сохранить настройки"""
        self.store.put('settings', **settings)
    
    def get_settings(self):
        """Получить настройки"""
        return self.store.get('settings') if self.store.exists('settings') else {}

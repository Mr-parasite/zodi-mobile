#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Splash Screen для ZODI Mobile
"""

from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.clock import Clock


class SplashScreen(Widget):
    """Экран загрузки с анимацией"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_ui()
    
    def create_ui(self):
        """Создание интерфейса"""
        # Основной контейнер
        layout = BoxLayout(
            orientation='vertical',
            padding=50,
            spacing=20
        )
        
        # Логотип
        self.logo_label = Label(
            text='🔮 ZODI',
            font_size='48sp',
            color=(0.55, 0.36, 0.96, 1),  # #8b5cf6
            size_hint_y=0.3
        )
        layout.add_widget(self.logo_label)
        
        # Подзаголовок
        self.subtitle_label = Label(
            text='Космические предсказания',
            font_size='18sp',
            color=(0.65, 0.55, 0.98, 1),  # #a78bfa
            size_hint_y=0.1
        )
        layout.add_widget(self.subtitle_label)
        
        # Приветствие
        self.welcome_label = Label(
            text='',
            font_size='16sp',
            color=(0.77, 0.71, 0.99, 1),  # #c4b5fd
            size_hint_y=0.1
        )
        layout.add_widget(self.welcome_label)
        
        # Пустое пространство
        layout.add_widget(Label(size_hint_y=0.4))
        
        # Статус загрузки
        self.status_label = Label(
            text='Загрузка...',
            font_size='14sp',
            color=(1, 1, 1, 0.7),
            size_hint_y=0.1
        )
        layout.add_widget(self.status_label)
        
        self.add_widget(layout)
        
        # Запуск анимации
        self.start_animation()
    
    def start_animation(self):
        """Запуск анимации"""
        # Анимация логотипа
        anim = Animation(opacity=1, duration=1) + Animation(opacity=0.7, duration=0.5)
        anim.repeat = True
        anim.start(self.logo_label)
        
        # Анимация приветствия
        Clock.schedule_once(self.animate_welcome, 1.5)
        
        # Обновление статуса
        Clock.schedule_once(self.update_status, 2.5)
    
    def animate_welcome(self, dt):
        """Анимация приветственного текста"""
        welcome_text = "Добро пожаловать в ZODI"
        current_text = ""
        
        def type_animation(index=0):
            if index < len(welcome_text):
                current_text = welcome_text[:index + 1]
                self.welcome_label.text = current_text
                Clock.schedule_once(lambda dt: type_animation(index + 1), 0.1)
        
        type_animation()
    
    def update_status(self, dt):
        """Обновление статуса загрузки"""
        self.status_label.text = "Готово!"

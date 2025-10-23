#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Predictions Screen для ZODI Mobile
"""

from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class PredictionsScreen(Widget):
    """Экран детальных предсказаний"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_ui()
    
    def create_ui(self):
        """Создание интерфейса"""
        layout = BoxLayout(orientation='vertical', padding=20)
        
        title = Label(
            text='🌟 Детальные предсказания',
            font_size='24sp',
            color=(0.55, 0.36, 0.96, 1),
            size_hint_y=0.2
        )
        layout.add_widget(title)
        
        content = Label(
            text='Здесь будут детальные предсказания по категориям',
            font_size='16sp',
            color=(0.77, 0.71, 0.99, 1),
            size_hint_y=0.6
        )
        layout.add_widget(content)
        
        back_btn = Button(
            text='⬅️ Назад',
            font_size='14sp',
            size_hint_y=0.2,
            background_color=(0.8, 0.2, 0.2, 1)
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def go_back(self, instance):
        """Вернуться назад"""
        self.app.screen_manager.current = 'results'

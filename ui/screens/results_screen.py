#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Results Screen для ZODI Mobile
"""

from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView


class ResultsScreen(Widget):
    """Экран результатов"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_ui()
    
    def create_ui(self):
        """Создание интерфейса"""
        # Основной контейнер
        layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=20
        )
        
        # Заголовок
        title_label = Label(
            text='🔮 Ваш знак зодиака',
            font_size='24sp',
            color=(0.55, 0.36, 0.96, 1),
            size_hint_y=0.15
        )
        layout.add_widget(title_label)
        
        # Символ знака
        self.symbol_label = Label(
            text='♏',
            font_size='48sp',
            color=(0.55, 0.36, 0.96, 1),
            size_hint_y=0.2
        )
        layout.add_widget(self.symbol_label)
        
        # Название знака
        self.sign_label = Label(
            text='Скорпион',
            font_size='20sp',
            color=(0.65, 0.55, 0.98, 1),
            size_hint_y=0.1
        )
        layout.add_widget(self.sign_label)
        
        # Предсказание
        scroll = ScrollView()
        self.prediction_label = Label(
            text='Сегодня звезды приготовили для вас особые сюрпризы!',
            font_size='16sp',
            color=(0.77, 0.71, 0.99, 1),
            text_size=(None, None),
            halign='center',
            valign='middle'
        )
        scroll.add_widget(self.prediction_label)
        layout.add_widget(scroll)
        
        # Кнопки
        buttons_layout = BoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint_y=0.15
        )
        
        detailed_btn = Button(
            text='🌟 Подробно',
            font_size='14sp',
            background_color=(0.55, 0.36, 0.96, 1)
        )
        detailed_btn.bind(on_press=self.show_detailed)
        buttons_layout.add_widget(detailed_btn)
        
        compatibility_btn = Button(
            text='💑 Совместимость',
            font_size='14sp',
            background_color=(0.65, 0.55, 0.98, 1)
        )
        compatibility_btn.bind(on_press=self.show_compatibility)
        buttons_layout.add_widget(compatibility_btn)
        
        layout.add_widget(buttons_layout)
        
        # Кнопка назад
        back_btn = Button(
            text='⬅️ Назад',
            font_size='14sp',
            size_hint_y=0.1,
            background_color=(0.8, 0.2, 0.2, 1)
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def show_detailed(self, instance):
        """Показать детальные предсказания"""
        self.app.screen_manager.current = 'predictions'
    
    def show_compatibility(self, instance):
        """Показать совместимость"""
        self.app.screen_manager.current = 'compatibility'
    
    def go_back(self, instance):
        """Вернуться назад"""
        self.app.screen_manager.current = 'input'

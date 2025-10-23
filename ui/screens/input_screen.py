#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Input Screen для ZODI Mobile
"""

from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from datetime import datetime


class InputScreen(Widget):
    """Экран ввода даты рождения"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_ui()
    
    def create_ui(self):
        """Создание интерфейса"""
        # Основной контейнер
        layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=20,
            size_hint=(1, 1)
        )
        
        # Заголовок
        title_label = Label(
            text='🔮 ZODI',
            font_size='36sp',
            color=(0.55, 0.36, 0.96, 1),  # #8b5cf6
            size_hint_y=0.15,
            size_hint_x=1
        )
        layout.add_widget(title_label)
        
        # Подзаголовок
        subtitle_label = Label(
            text='Космические предсказания',
            font_size='16sp',
            color=(0.65, 0.55, 0.98, 1),  # #a78bfa
            size_hint_y=0.08,
            size_hint_x=1
        )
        layout.add_widget(subtitle_label)
        
        # Карточка ввода
        card = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=15,
            size_hint_y=0.5,
            size_hint_x=1
        )
        
        # Заголовок карточки
        card_title = Label(
            text='🌟 Введите дату своего рождения',
            font_size='18sp',
            color=(0.77, 0.71, 0.99, 1),  # #c4b5fd
            size_hint_y=0.15,
            size_hint_x=1
        )
        card.add_widget(card_title)
        
        # Поля ввода
        input_layout = GridLayout(cols=2, spacing=10, size_hint_y=0.4, size_hint_x=1)
        
        # День
        day_label = Label(
            text='📅 День:',
            font_size='14sp',
            color=(0.77, 0.71, 0.99, 1)
        )
        input_layout.add_widget(day_label)
        
        self.day_input = TextInput(
            hint_text='День (1-31)',
            multiline=False,
            font_size='16sp'
        )
        input_layout.add_widget(self.day_input)
        
        # Месяц
        month_label = Label(
            text='📆 Месяц:',
            font_size='14sp',
            color=(0.77, 0.71, 0.99, 1)
        )
        input_layout.add_widget(month_label)
        
        self.month_input = TextInput(
            hint_text='Месяц (1-12)',
            multiline=False,
            font_size='16sp'
        )
        input_layout.add_widget(self.month_input)
        
        card.add_widget(input_layout)
        
        # Кнопка определения
        self.determine_btn = Button(
            text='✨ Определить знак зодиака',
            font_size='16sp',
            size_hint_y=0.2,
            size_hint_x=1,
            background_color=(0.55, 0.36, 0.96, 1)  # #8b5cf6
        )
        self.determine_btn.bind(on_press=self.determine_zodiac)
        card.add_widget(self.determine_btn)
        
        layout.add_widget(card)
        
        # Пустое пространство
        layout.add_widget(Label(size_hint_y=0.2, size_hint_x=1))
        
        # Кнопка профиля
        profile_btn = Button(
            text='👤 Профиль',
            font_size='14sp',
            size_hint_y=0.1,
            size_hint_x=1,
            background_color=(0.65, 0.55, 0.98, 1)  # #a78bfa
        )
        profile_btn.bind(on_press=self.show_profile)
        layout.add_widget(profile_btn)
        
        self.add_widget(layout)
    
    def determine_zodiac(self, instance):
        """Определить знак зодиака"""
        try:
            day = int(self.day_input.text)
            month = int(self.month_input.text)
            
            if not (1 <= day <= 31 and 1 <= month <= 12):
                self.show_error("Неверная дата. Введите корректные значения.")
                return
            
            # Вычисляем знак зодиака
            zodiac_sign = self.app.calculate_zodiac(day, month)
            
            if zodiac_sign:
                # Сохраняем в профиль
                profile_data = {
                    'day': day,
                    'month': month,
                    'zodiac_sign': zodiac_sign
                }
                self.app.save_profile(profile_data)
                
                # Переходим к результатам
                self.app.screen_manager.current = 'results'
            else:
                self.show_error("Ошибка определения знака зодиака")
                
        except ValueError:
            self.show_error("Введите корректные числа")
        except Exception as e:
            self.show_error(f"Ошибка: {e}")
    
    def show_profile(self, instance):
        """Показать профиль"""
        self.app.screen_manager.current = 'profile'
    
    def show_error(self, message):
        """Показать ошибку"""
        popup = Popup(
            title='Ошибка',
            content=Label(text=message),
            size_hint=(0.8, 0.4)
        )
        popup.open()

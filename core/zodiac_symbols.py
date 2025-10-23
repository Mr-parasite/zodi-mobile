#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZODI - Статичные символы знаков зодиака с цветовыми эффектами
Unicode-символы с цветовыми схемами по элементам
"""

from typing import Dict, List, Tuple

class ZodiacSymbols:
    """Класс для работы с символами знаков зодиака"""
    
    def __init__(self):
        self.symbols = self._get_zodiac_symbols()
        self.elements = self._get_elements_mapping()
        self.planets = self._get_planets_mapping()
        self.element_colors = self._get_element_colors()
        self.glow_effects = self._get_glow_effects()
    
    def _get_zodiac_symbols(self) -> Dict[str, str]:
        """Получить Unicode-символы знаков зодиака"""
        return {
            "Овен": "♈",
            "Телец": "♉", 
            "Близнецы": "♊",
            "Рак": "♋",
            "Лев": "♌",
            "Дева": "♍",
            "Весы": "♎",
            "Скорпион": "♏",
            "Стрелец": "♐",
            "Козерог": "♑",
            "Водолей": "♒",
            "Рыбы": "♓"
        }
    
    def _get_elements_mapping(self) -> Dict[str, str]:
        """Получить соответствие знаков элементам"""
        return {
            "Овен": "Огонь", "Лев": "Огонь", "Стрелец": "Огонь",
            "Телец": "Земля", "Дева": "Земля", "Козерог": "Земля",
            "Близнецы": "Воздух", "Весы": "Воздух", "Водолей": "Воздух",
            "Рак": "Вода", "Скорпион": "Вода", "Рыбы": "Вода"
        }
    
    def _get_planets_mapping(self) -> Dict[str, str]:
        """Получить соответствие знаков планетам"""
        return {
            "Овен": "Марс", "Телец": "Венера", "Близнецы": "Меркурий",
            "Рак": "Луна", "Лев": "Солнце", "Дева": "Меркурий",
            "Весы": "Венера", "Скорпион": "Плутон", "Стрелец": "Юпитер",
            "Козерог": "Сатурн", "Водолей": "Уран", "Рыбы": "Нептун"
        }
    
    def _get_element_colors(self) -> Dict[str, Dict[str, str]]:
        """Получить цветовые схемы для элементов"""
        return {
            "Огонь": {
                "primary": "#ff6b35",      # Оранжево-красный
                "secondary": "#f7931e",    # Золотисто-оранжевый
                "accent": "#ff4757",       # Ярко-красный
                "glow": "#ff6b35"          # Свечение
            },
            "Земля": {
                "primary": "#2ed573",      # Зеленый
                "secondary": "#7bed9f",    # Светло-зеленый
                "accent": "#ffa502",       # Золотисто-коричневый
                "glow": "#2ed573"          # Свечение
            },
            "Воздух": {
                "primary": "#3742fa",      # Синий
                "secondary": "#5352ed",    # Светло-синий
                "accent": "#70a1ff",       # Голубой
                "glow": "#3742fa"          # Свечение
            },
            "Вода": {
                "primary": "#48dbfb",      # Бирюзовый
                "secondary": "#0fbcf9",    # Ярко-синий
                "accent": "#00d2d3",       # Циан
                "glow": "#48dbfb"          # Свечение
            }
        }
    
    def _get_glow_effects(self) -> Dict[str, List[str]]:
        """Получить эффекты свечения для элементов"""
        return {
            "Огонь": ["#ff6b35", "#ff4757", "#ffa502", "#ff6b35"],
            "Земля": ["#2ed573", "#7bed9f", "#ffa502", "#2ed573"],
            "Воздух": ["#3742fa", "#5352ed", "#70a1ff", "#3742fa"],
            "Вода": ["#48dbfb", "#0fbcf9", "#00d2d3", "#48dbfb"]
        }
    
    def get_symbol(self, sign: str) -> str:
        """Получить Unicode-символ знака"""
        return self.symbols.get(sign, "⭐")
    
    def get_styled_symbol(self, sign: str) -> Dict[str, any]:
        """Получить стилизованный символ с цветами и эффектами"""
        symbol = self.get_symbol(sign)
        element = self.elements.get(sign, "Неизвестно")
        colors = self.element_colors.get(element, self.element_colors["Огонь"])
        glow_colors = self.glow_effects.get(element, self.glow_effects["Огонь"])
        
        return {
            'symbol': symbol,
            'element': element,
            'colors': colors,
            'glow_colors': glow_colors,
            'glow_color': colors['glow']
        }
    
    def get_element_info(self, sign: str) -> Dict[str, str]:
        """Получить информацию об элементе знака"""
        element = self.elements.get(sign, "Неизвестно")
        planet = self.planets.get(sign, "Неизвестно")
        colors = self.element_colors.get(element, self.element_colors["Огонь"])
        
        return {
            'element': element,
            'planet': planet,
            'primary_color': colors['primary'],
            'secondary_color': colors['secondary'],
            'accent_color': colors['accent'],
            'glow_color': colors['glow']
        }
    
    def get_all_signs_with_symbols(self) -> Dict[str, str]:
        """Получить все знаки с их символами"""
        return self.symbols.copy()
    
    def get_signs_by_element(self, element: str) -> List[str]:
        """Получить знаки по элементу"""
        return [sign for sign, elem in self.elements.items() if elem == element]
    
    def get_element_colors_for_sign(self, sign: str) -> Dict[str, str]:
        """Получить цвета элемента для конкретного знака"""
        element = self.elements.get(sign, "Огонь")
        return self.element_colors.get(element, self.element_colors["Огонь"])
    
    def get_glow_animation_colors(self, sign: str) -> List[str]:
        """Получить цвета для анимации свечения"""
        element = self.elements.get(sign, "Огонь")
        return self.glow_effects.get(element, self.glow_effects["Огонь"])
    
    def get_symbol_with_size(self, sign: str, size: int = 80) -> Dict[str, any]:
        """Получить символ с указанным размером шрифта"""
        styled = self.get_styled_symbol(sign)
        return {
            **styled,
            'font_size': size
        }
    
    def get_compatibility_colors(self, sign1: str, sign2: str) -> Dict[str, str]:
        """Получить цвета для отображения совместимости двух знаков"""
        element1 = self.elements.get(sign1, "Огонь")
        element2 = self.elements.get(sign2, "Огонь")
        
        colors1 = self.element_colors.get(element1, self.element_colors["Огонь"])
        colors2 = self.element_colors.get(element2, self.element_colors["Огонь"])
        
        return {
            'sign1_color': colors1['primary'],
            'sign2_color': colors2['primary'],
            'blend_color': self._blend_colors(colors1['primary'], colors2['primary'])
        }
    
    def _blend_colors(self, color1: str, color2: str) -> str:
        """Смешать два цвета для создания промежуточного"""
        # Простое смешивание - возвращаем первый цвет
        # В реальном приложении можно реализовать более сложную логику
        return color1
    
    def get_element_description(self, element: str) -> str:
        """Получить описание элемента"""
        descriptions = {
            "Огонь": "Страстные, энергичные и инициативные",
            "Земля": "Практичные, надежные и стабильные", 
            "Воздух": "Интеллектуальные, общительные и гибкие",
            "Вода": "Эмоциональные, интуитивные и чувствительные"
        }
        return descriptions.get(element, "Неизвестный элемент")
    
    def get_sign_element_description(self, sign: str) -> str:
        """Получить описание элемента для конкретного знака"""
        element = self.elements.get(sign, "Огонь")
        return self.get_element_description(element)

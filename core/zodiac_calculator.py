#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Калькулятор знаков зодиака
"""

def get_zodiac_sign(day: int, month: int) -> str:
    """
    Определяет знак зодиака по дате рождения
    
    Args:
        day: День рождения (1-31)
        month: Месяц рождения (1-12)
    
    Returns:
        str: Название знака зодиака на русском языке
    """
    # Проверка валидности даты
    if not (1 <= day <= 31 and 1 <= month <= 12):
        return "Не определено"
    
    # Определение знака зодиака
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Овен"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Телец"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Близнецы"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Рак"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Лев"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Дева"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Весы"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Скорпион"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Стрелец"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Козерог"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Водолей"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return "Рыбы"
    else:
        return "Не определено"
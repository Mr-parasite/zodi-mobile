#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Расширенная база данных предсказаний с возможностью смешивания знаков
"""

import random
from datetime import datetime

# Импортируем полную базу данных из mega_predictions
from .mega_predictions import MEGA_PREDICTIONS

# Расширенные предсказания (10 вариантов для каждой категории)
ENHANCED_PREDICTIONS = MEGA_PREDICTIONS

# Функция для получения сезонных предсказаний
def get_seasonal_prediction(sign, category, season=None):
    """Получить сезонное предсказание"""
    if season is None:
        month = datetime.now().month
        if month in [12, 1, 2]:
            season = "зима"
        elif month in [3, 4, 5]:
            season = "весна"
        elif month in [6, 7, 8]:
            season = "лето"
        else:
            season = "осень"
    
    seasonal_modifiers = {
        "зима": "В холодное время года ваша внутренняя сила проявляется особенно ярко.",
        "весна": "Весенняя энергия пробуждает новые возможности и надежды.",
        "лето": "Летнее солнце дарит энергию для активных действий и достижений.",
        "осень": "Осенняя мудрость помогает в принятии важных решений."
    }
    
    base_prediction = get_random_prediction(sign, category)
    seasonal_context = seasonal_modifiers.get(season, "")
    
    return f"{seasonal_context} {base_prediction}"

# Функция для получения предсказаний на основе настроения
def get_mood_based_prediction(sign, category, mood="нейтральное"):
    """Получить предсказание на основе настроения"""
    mood_modifiers = {
        "позитивное": "Ваше оптимистичное настроение привлекает положительные события.",
        "творческое": "Творческая энергия открывает новые горизонты для самовыражения.",
        "романтическое": "Романтическое настроение создает благоприятную атмосферу для любви.",
        "деловое": "Деловая хватка поможет в достижении профессиональных целей.",
        "медитативное": "Внутреннее спокойствие помогает в принятии мудрых решений.",
        "авантюрное": "Дух приключений ведет к новым открытиям и возможностям.",
        "семейное": "Семейные ценности и забота о близких приносят глубокое удовлетворение.",
        "нейтральное": "Сбалансированное состояние души создает благоприятные условия для роста."
    }
    
    base_prediction = get_random_prediction(sign, category)
    mood_context = mood_modifiers.get(mood, mood_modifiers["нейтральное"])
    
    return f"{mood_context} {base_prediction}"

def get_random_prediction(sign, category):
    """Получить случайное предсказание для знака зодиака и категории с универсальными предсказаниями"""
    # 70% вероятность получить предсказание своего знака, 30% - универсальное предсказание
    if random.random() < 0.7:
        # Обычное предсказание для своего знака
        if sign in ENHANCED_PREDICTIONS and category in ENHANCED_PREDICTIONS[sign]:
            predictions = ENHANCED_PREDICTIONS[sign][category]
            return random.choice(predictions)
    else:
        # Универсальное предсказание
        from .universal_predictions import get_universal_prediction
        return get_universal_prediction(category)
    
    # Fallback - обычное предсказание
    if sign in ENHANCED_PREDICTIONS and category in ENHANCED_PREDICTIONS[sign]:
        predictions = ENHANCED_PREDICTIONS[sign][category]
        return random.choice(predictions)
    return "Звезды готовят для вас удивительные возможности!"

def get_daily_horoscope(sign):
    """Получить ежедневное предсказание"""
    return get_random_prediction(sign, "general")

def get_love_prediction(sign):
    """Получить предсказание о любви"""
    return get_random_prediction(sign, "love")

def get_career_prediction(sign):
    """Получить предсказание о карьере"""
    return get_random_prediction(sign, "career")

def get_finance_prediction(sign):
    """Получить предсказание о финансах"""
    return get_random_prediction(sign, "finance")

def get_health_prediction(sign):
    """Получить предсказание о здоровье"""
    return get_random_prediction(sign, "health")

def get_advice_prediction(sign):
    """Получить совет"""
    return get_random_prediction(sign, "advice")

def get_opportunities_prediction(sign):
    """Получить предсказание о возможностях"""
    return get_random_prediction(sign, "opportunities")

# Функция для получения предсказания с возможностью смешивания знаков
def get_enhanced_prediction(sign, category, mix_signs=False, source_sign=None, season=None, mood=None):
    """Получить расширенное предсказание с дополнительными опциями"""
    
    # Если включено смешивание знаков и указан исходный знак
    if mix_signs and source_sign and source_sign != sign:
        return get_mixed_prediction(sign, source_sign, category)
    
    # Если указан сезон
    if season:
        return get_seasonal_prediction(sign, category, season)
    
    # Если указано настроение
    if mood:
        return get_mood_based_prediction(sign, category, mood)
    
    # Обычное предсказание
    return get_random_prediction(sign, category)
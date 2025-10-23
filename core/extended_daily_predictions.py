#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZODI - Расширенные ежедневные предсказания
7 категорий предсказаний для каждого знака зодиака
"""

import json
import os
import random
from datetime import datetime
from typing import Dict, List

class ExtendedDailyPredictions:
    """Класс для расширенных ежедневных предсказаний с 7 категориями"""
    
    def __init__(self, zodiac_sign: str):
        self.zodiac_sign = zodiac_sign
        self.categories = {
            'love': "💖 Личная жизнь",
            'career': "💼 Карьера", 
            'finance': "💰 Финансы",
            'health': "🏥 Здоровье",
            'growth': "🎯 Личностный рост",
            'energy': "🌙 Энергетика дня",
            'warnings': "⚠️ Предостережения"
        }
        self.predictions_db = self._load_predictions_database()
    
    def _load_predictions_database(self) -> Dict:
        """Загрузить базу данных предсказаний"""
        # Сначала пробуем качественную базу данных (приоритет №1)
        db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'extended_predictions_quality.json')
        
        try:
            with open(db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Качественная база имеет структуру с metadata и predictions
                if 'predictions' in data:
                    return data['predictions']
                return data
        except FileNotFoundError:
            # Если качественная база не найдена, пробуем объединенную базу данных (приоритет №2)
            db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'extended_predictions_unified.json')
        
        try:
            with open(db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Объединенная база имеет структуру с metadata и predictions
                if 'predictions' in data:
                    return data['predictions']
                return data
        except FileNotFoundError:
            # Если объединенная база не найдена, пробуем полную мега-базу данных для всех знаков
            db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'extended_predictions_mega_all.json')
            try:
                with open(db_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except FileNotFoundError:
                # Если полная мега-база не найдена, пробуем мега-базу данных
                db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'extended_predictions_mega_complete.json')
                try:
                    with open(db_path, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except FileNotFoundError:
                    # Если мега-база не найдена, пробуем полную базу данных
                    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'extended_predictions_complete.json')
                    try:
                        with open(db_path, 'r', encoding='utf-8') as f:
                            return json.load(f)
                    except FileNotFoundError:
                        # Если полная база не найдена, пробуем основную
                        db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'extended_predictions_db.json')
                        try:
                            with open(db_path, 'r', encoding='utf-8') as f:
                                return json.load(f)
                        except FileNotFoundError:
                            # Если база данных не найдена, создать базовую структуру
                            return self._create_fallback_predictions()
    
    def _create_fallback_predictions(self) -> Dict:
        """Создать базовые предсказания если база данных недоступна"""
        return {
            self.zodiac_sign: {
                'love': [f"Ваша личная жизнь для {self.zodiac_sign} сегодня..."],
                'career': [f"Карьерные перспективы для {self.zodiac_sign}..."],
                'finance': [f"Финансовые возможности для {self.zodiac_sign}..."],
                'health': [f"Здоровье и энергия для {self.zodiac_sign}..."],
                'growth': [f"Личностный рост для {self.zodiac_sign}..."],
                'energy': [f"Энергетика дня для {self.zodiac_sign}..."],
                'warnings': [f"Предостережения для {self.zodiac_sign}..."]
            }
        }
    
    def get_detailed_predictions(self) -> Dict[str, str]:
        """Получить расширенные предсказания по всем категориям"""
        predictions = {}
        
        if self.zodiac_sign in self.predictions_db:
            sign_data = self.predictions_db[self.zodiac_sign]
            
            for category_key, category_name in self.categories.items():
                if category_key in sign_data and sign_data[category_key]:
                    # Выбираем случайное предсказание из списка
                    prediction_list = sign_data[category_key]
                    selected_prediction = random.choice(prediction_list)
                    predictions[category_key] = selected_prediction
                else:
                    # Fallback предсказание
                    predictions[category_key] = f"Предсказание для категории {category_name} временно недоступно."
        else:
            # Fallback для неизвестного знака
            for category_key, category_name in self.categories.items():
                predictions[category_key] = f"Предсказание для {category_name} для {self.zodiac_sign} будет доступно в ближайшее время."
        
        return predictions
    
    def get_category_prediction(self, category: str) -> str:
        """Получить предсказание для конкретной категории"""
        all_predictions = self.get_detailed_predictions()
        return all_predictions.get(category, "Предсказание недоступно.")
    
    def get_categories_info(self) -> Dict[str, str]:
        """Получить информацию о всех категориях"""
        return self.categories
    
    def get_random_prediction(self) -> str:
        """Получить случайное предсказание из любой категории"""
        all_predictions = self.get_detailed_predictions()
        if all_predictions:
            category = random.choice(list(all_predictions.keys()))
            return f"{self.categories[category]}: {all_predictions[category]}"
        return "Предсказания временно недоступны."

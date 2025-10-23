#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZODI - Калькулятор совместимости знаков зодиака
Анализ совместимости с учетом элементов, планет и типов отношений
"""

import json
import os
from typing import Dict, List, Tuple, Literal

class CompatibilityCalculator:
    """Класс для расчета совместимости знаков зодиака"""
    
    def __init__(self):
        self.compatibility_matrix = self._load_compatibility_matrix()
        self.elements = self._get_elements_mapping()
        self.planets = self._get_planets_mapping()
        self.relationship_types = {
            'romantic': 'Романтические отношения',
            'friendship': 'Дружба',
            'business': 'Деловые отношения',
            'family': 'Семейные отношения'
        }
    
    def _load_compatibility_matrix(self) -> Dict:
        """Загрузить матрицу совместимости"""
        db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'compatibility_matrix.json')
        
        try:
            with open(db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Если база данных не найдена, создать базовую матрицу
            return self._create_fallback_matrix()
    
    def _create_fallback_matrix(self) -> Dict:
        """Создать базовую матрицу совместимости"""
        signs = ["Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева", 
                "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"]
        
        matrix = {}
        for sign1 in signs:
            matrix[sign1] = {}
            for sign2 in signs:
                if sign1 == sign2:
                    matrix[sign1][sign2] = 85  # Высокая совместимость с собой
                else:
                    # Базовая совместимость
                    matrix[sign1][sign2] = 60
        
        return {"base_compatibility": matrix}
    
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
    
    def calculate_love_compatibility(self, sign1: str, sign2: str) -> int:
        """Рассчитать романтическую совместимость (40% веса)"""
        base = self._get_base_compatibility_score(sign1, sign2)
        element_bonus = self._analyze_elements(sign1, sign2)['bonus']
        planet_bonus = self._analyze_planets(sign1, sign2)['bonus']
        return min(100, max(0, base + element_bonus + planet_bonus + 5))
    
    def calculate_friendship_compatibility(self, sign1: str, sign2: str) -> int:
        """Рассчитать дружескую совместимость (25% веса)"""
        base = self._get_base_compatibility_score(sign1, sign2)
        element_bonus = self._analyze_elements(sign1, sign2)['bonus']
        return min(100, max(0, base + element_bonus + 10))
    
    def calculate_business_compatibility(self, sign1: str, sign2: str) -> int:
        """Рассчитать деловую совместимость (20% веса)"""
        base = self._get_base_compatibility_score(sign1, sign2)
        # Деловая совместимость меньше зависит от элементов
        return min(100, max(0, base + 5))
    
    def calculate_intellectual_compatibility(self, sign1: str, sign2: str) -> int:
        """Рассчитать интеллектуальную совместимость (15% веса)"""
        element1 = self.elements.get(sign1, "Неизвестно")
        element2 = self.elements.get(sign2, "Неизвестно")
        
        # Воздушные знаки более интеллектуальны
        base = self._get_base_compatibility_score(sign1, sign2)
        bonus = 0
        if element1 == "Воздух" or element2 == "Воздух":
            bonus = 10
        if element1 == element2:
            bonus += 5
        
        return min(100, max(0, base + bonus))
    
    def calculate_compatibility(self, sign1: str, sign2: str, 
                               relationship_type: Literal['romantic', 'friendship', 'business', 'family'] = 'romantic') -> Dict:
        """Рассчитать совместимость между двумя знаками"""
        
        # Многоуровневый анализ
        love_score = self.calculate_love_compatibility(sign1, sign2)
        friendship_score = self.calculate_friendship_compatibility(sign1, sign2)
        business_score = self.calculate_business_compatibility(sign1, sign2)
        intellectual_score = self.calculate_intellectual_compatibility(sign1, sign2)
        
        # Взвешенный итоговый балл
        final_score = int(
            love_score * 0.40 +
            friendship_score * 0.25 +
            business_score * 0.20 +
            intellectual_score * 0.15
        )
        
        # Базовый балл совместимости
        base_score = self._get_base_compatibility_score(sign1, sign2)
        
        # Корректировки по типу отношений
        relationship_adjustment = self._get_relationship_adjustment(sign1, sign2, relationship_type)
        
        # Анализ элементов
        element_analysis = self._analyze_elements(sign1, sign2)
        
        # Анализ планет
        planet_analysis = self._analyze_planets(sign1, sign2)
        
        # Итоговый балл
        final_score = min(100, max(0, base_score + relationship_adjustment + element_analysis['bonus']))
        
        # Генерация описания и рекомендаций
        description = self._generate_compatibility_description(sign1, sign2, final_score, relationship_type)
        strengths = self._get_relationship_strengths(sign1, sign2, relationship_type)
        challenges = self._get_relationship_challenges(sign1, sign2, relationship_type)
        recommendations = self._get_recommendations(sign1, sign2, relationship_type, final_score)
        
        return {
            'score': final_score,
            'love_score': love_score,
            'friendship_score': friendship_score,
            'business_score': business_score,
            'intellectual_score': intellectual_score,
            'description': description,
            'strengths': strengths,
            'challenges': challenges,
            'element_analysis': element_analysis,
            'planet_influence': planet_analysis,
            'recommendations': recommendations,
            'relationship_type': self.relationship_types[relationship_type]
        }
    
    def _get_base_compatibility_score(self, sign1: str, sign2: str) -> int:
        """Получить базовый балл совместимости"""
        if 'base_compatibility' in self.compatibility_matrix:
            return self.compatibility_matrix['base_compatibility'].get(sign1, {}).get(sign2, 50)
        return 50
    
    def _get_relationship_adjustment(self, sign1: str, sign2: str, relationship_type: str) -> int:
        """Получить корректировку по типу отношений"""
        adjustments = {
            'romantic': 0,      # Базовые настройки
            'friendship': 5,    # Дружба обычно легче
            'business': -5,     # Деловые отношения могут быть сложнее
            'family': 10        # Семейные узы сильнее
        }
        return adjustments.get(relationship_type, 0)
    
    def _analyze_elements(self, sign1: str, sign2: str) -> Dict:
        """Анализ совместимости элементов"""
        element1 = self.elements.get(sign1, "Неизвестно")
        element2 = self.elements.get(sign2, "Неизвестно")
        
        if element1 == element2:
            return {
                'compatibility': 'Отличная',
                'description': f'Оба знака принадлежат к элементу {element1}. Глубокое понимание и схожие подходы к жизни.',
                'bonus': 15
            }
        
        # Совместимые элементы
        compatible_pairs = [
            ('Огонь', 'Воздух'), ('Воздух', 'Огонь'),
            ('Земля', 'Вода'), ('Вода', 'Земля')
        ]
        
        if (element1, element2) in compatible_pairs:
            return {
                'compatibility': 'Хорошая',
                'description': f'Элементы {element1} и {element2} хорошо дополняют друг друга.',
                'bonus': 10
            }
        
        # Несовместимые элементы
        incompatible_pairs = [
            ('Огонь', 'Вода'), ('Вода', 'Огонь'),
            ('Земля', 'Воздух'), ('Воздух', 'Земля')
        ]
        
        if (element1, element2) in incompatible_pairs:
            return {
                'compatibility': 'Сложная',
                'description': f'Элементы {element1} и {element2} могут конфликтовать, но различия могут быть источником роста.',
                'bonus': -5
            }
        
        return {
            'compatibility': 'Нейтральная',
            'description': f'Элементы {element1} и {element2} нейтральны друг к другу.',
            'bonus': 0
        }
    
    def _analyze_planets(self, sign1: str, sign2: str) -> Dict:
        """Анализ влияния планет"""
        planet1 = self.planets.get(sign1, "Неизвестно")
        planet2 = self.planets.get(sign2, "Неизвестно")
        
        # Совместимые планеты
        compatible_planets = [
            ('Солнце', 'Луна'), ('Луна', 'Солнце'),
            ('Меркурий', 'Венера'), ('Венера', 'Меркурий'),
            ('Марс', 'Юпитер'), ('Юпитер', 'Марс')
        ]
        
        if (planet1, planet2) in compatible_planets:
            return {
                'influence': 'Гармоничное',
                'description': f'Планеты {planet1} и {planet2} создают гармоничное взаимодействие.',
                'bonus': 5
            }
        
        return {
            'influence': 'Нейтральное',
            'description': f'Планеты {planet1} и {planet2} взаимодействуют нейтрально.',
            'bonus': 0
        }
    
    def _generate_compatibility_description(self, sign1: str, sign2: str, score: int, relationship_type: str) -> str:
        """Генерировать описание совместимости"""
        if score >= 80:
            return f"Отличная совместимость! {sign1} и {sign2} создают идеальную пару для {self.relationship_types[relationship_type].lower()}."
        elif score >= 60:
            return f"Хорошая совместимость. {sign1} и {sign2} могут успешно строить отношения при взаимном понимании."
        elif score >= 40:
            return f"Умеренная совместимость. {sign1} и {sign2} потребуют усилий для гармоничных отношений."
        else:
            return f"Сложная совместимость. {sign1} и {sign2} могут столкнуться с трудностями, но различия могут стать источником роста."
    
    def _get_relationship_strengths(self, sign1: str, sign2: str, relationship_type: str) -> List[str]:
        """Получить сильные стороны отношений"""
        strengths_db = {
            'romantic': [
                "Глубокое эмоциональное понимание",
                "Страстная связь",
                "Взаимное уважение и поддержка",
                "Общие жизненные ценности"
            ],
            'friendship': [
                "Взаимное доверие",
                "Общие интересы и хобби",
                "Поддержка в трудные моменты",
                "Веселое времяпрепровождение"
            ],
            'business': [
                "Дополняющие навыки",
                "Эффективное разделение обязанностей",
                "Взаимное уважение к компетенциям",
                "Общие деловые цели"
            ],
            'family': [
                "Семейные традиции и ценности",
                "Взаимная поддержка",
                "Глубокое понимание семейной динамики",
                "Общие воспоминания и опыт"
            ]
        }
        return strengths_db.get(relationship_type, ["Взаимное уважение", "Общие интересы"])
    
    def _get_relationship_challenges(self, sign1: str, sign2: str, relationship_type: str) -> List[str]:
        """Получить вызовы в отношениях"""
        challenges_db = {
            'romantic': [
                "Различия в выражении эмоций",
                "Разные подходы к конфликтам",
                "Различные потребности в личном пространстве",
                "Разные темпы развития отношений"
            ],
            'friendship': [
                "Различия в социальных предпочтениях",
                "Разные подходы к планированию времени",
                "Различные уровни активности",
                "Разные способы решения проблем"
            ],
            'business': [
                "Различия в рабочих стилях",
                "Разные подходы к принятию решений",
                "Различные приоритеты в работе",
                "Разные способы коммуникации"
            ],
            'family': [
                "Различия в семейных традициях",
                "Разные подходы к воспитанию",
                "Различные взгляды на семейные роли",
                "Разные способы выражения заботы"
            ]
        }
        return challenges_db.get(relationship_type, ["Различия в характерах", "Разные подходы к жизни"])
    
    def _get_recommendations(self, sign1: str, sign2: str, relationship_type: str, score: int) -> List[str]:
        """Получить рекомендации для улучшения отношений"""
        if score >= 80:
            return [
                "Продолжайте развивать существующую гармонию",
                "Ищите новые способы укрепления связи",
                "Помогайте друг другу в личностном росте"
            ]
        elif score >= 60:
            return [
                "Уделяйте время открытому общению",
                "Ищите компромиссы в спорных вопросах",
                "Цените различия как источник роста"
            ]
        else:
            return [
                "Проявляйте терпение и понимание",
                "Ищите общие интересы и цели",
                "Рассмотрите возможность профессиональной помощи"
            ]
    
    def get_all_signs(self) -> List[str]:
        """Получить список всех знаков зодиака"""
        return list(self.elements.keys())
    
    def get_sign_element(self, sign: str) -> str:
        """Получить элемент знака"""
        return self.elements.get(sign, "Неизвестно")
    
    def get_sign_planet(self, sign: str) -> str:
        """Получить планету знака"""
        return self.planets.get(sign, "Неизвестно")

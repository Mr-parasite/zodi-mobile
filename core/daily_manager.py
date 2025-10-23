#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Механизм ежедневной фиксации предсказаний.

Задачи:
- Один набор из 12 уникальных общих предсказаний на день
- Консистентность в течение суток (до 00:00)
- Детерминированная генерация по ключу даты
"""

from __future__ import annotations

import json
import os
import hashlib
import random
from datetime import datetime
from typing import Dict, List


DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
CACHE_PATH = os.path.join(DATA_DIR, 'daily_predictions.json')


ALL_SIGNS_ORDER = [
    "Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева",
    "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы",
]


class DailyPredictionManager:
    """Генерирует и кэширует уникальные ежедневные предсказания."""

    def __init__(self) -> None:
        self.today_key = datetime.now().date().isoformat()
        self.cache: Dict[str, Dict[str, str]] = self._load_cache()

    # ---------------------------- public API ----------------------------
    def get_general_for_sign(self, sign: str) -> str:
        """Вернуть фиксированное на день общее предсказание для знака."""
        day_bucket = self._ensure_today_bucket()
        if sign in day_bucket:
            return day_bucket[sign]
        # Если по каким-то причинам нет записи — дозаполним аккуратно
        self._generate_for_missing(day_bucket)
        self._save_cache()
        return day_bucket.get(sign, "Предсказание временно недоступно.")

    # --------------------------- core logic ----------------------------
    def _ensure_today_bucket(self) -> Dict[str, str]:
        if self.today_key not in self.cache:
            self.cache = {self.today_key: self._generate_full_day()}
            self._save_cache()
        return self.cache[self.today_key]

    def _generate_full_day(self) -> Dict[str, str]:
        """Сгенерировать 12 уникальных предсказаний на текущий день."""
        rng = self._rng_for_today()

        # Импорт внутри, чтобы избежать ранних тяжелых импортов при запуске
        from . import structured_predictions as sp  # type: ignore

        # Собираем кандидатов: персональные general + часть универсальных
        universal = list(sp.UNIVERSAL_PREDICTIONS["predictions"]["general"])  # type: ignore
        # Перемешаем универсальные детерминированно
        rng.shuffle(universal)

        # Подготовим карты кандидатов по знакам
        candidates: Dict[str, List[str]] = {}

        def sign_general_pool(sign_name: str) -> List[str]:
            # Извлекаем структуру для конкретного знака через словарь в sp.get_prediction
            # Прямого словаря нет — но данные лежат в модулях; используем ту же логику, что в sp.get_prediction
            from .remaining_zodiac_predictions import (
                VIRGO_PREDICTIONS, LIBRA_PREDICTIONS, SCORPIO_PREDICTIONS,
                SAGITTARIUS_PREDICTIONS, CAPRICORN_PREDICTIONS, AQUARIUS_PREDICTIONS,
                PISCES_PREDICTIONS,
            )
            sign_map = {
                "Овен": sp.ARIES_PREDICTIONS,
                "Телец": sp.TAURUS_PREDICTIONS,
                "Близнецы": sp.GEMINI_PREDICTIONS,
                "Рак": sp.CANCER_PREDICTIONS,
                "Лев": sp.LEO_PREDICTIONS,
                "Дева": VIRGO_PREDICTIONS,
                "Весы": LIBRA_PREDICTIONS,
                "Скорпион": SCORPIO_PREDICTIONS,
                "Стрелец": SAGITTARIUS_PREDICTIONS,
                "Козерог": CAPRICORN_PREDICTIONS,
                "Водолей": AQUARIUS_PREDICTIONS,
                "Рыбы": PISCES_PREDICTIONS,
            }
            personal = list(sign_map[sign_name]["predictions"]["general"])  # type: ignore
            return personal

        for s in ALL_SIGNS_ORDER:
            pool = sign_general_pool(s)
            rng.shuffle(pool)
            # Добавим часть универсальных в хвост пула, чтобы при нехватке персональных было из чего выбрать
            mixed = pool + universal
            candidates[s] = mixed

        picked: Dict[str, str] = {}
        used: set[str] = set()

        # Проходим по знакам в фиксированном порядке и выбираем первый ещё не использованный текст
        for s in ALL_SIGNS_ORDER:
            for text in candidates[s]:
                if text not in used:
                    picked[s] = text
                    used.add(text)
                    break
            if s not in picked:
                # На крайний случай (почти невозможен при богатой базе) — генерируем стабильный псевдо‑вариант
                picked[s] = f"День приносит новые возможности для {s.lower()}. Сохраняйте уверенность и спокойствие."

        return picked

    def _generate_for_missing(self, day_bucket: Dict[str, str]) -> None:
        rng = self._rng_for_today()
        from . import structured_predictions as sp
        universal = list(sp.UNIVERSAL_PREDICTIONS["predictions"]["general"])  # type: ignore
        rng.shuffle(universal)
        used = set(day_bucket.values())
        for s in ALL_SIGNS_ORDER:
            if s in day_bucket:
                continue
            # fallback — найдём любой уникальный универсальный
            choice = next((t for t in universal if t not in used), universal[0] if universal else "" )
            day_bucket[s] = choice or f"Сегодня благоприятный день для {s.lower()}"
            used.add(day_bucket[s])

    # --------------------------- persistence ---------------------------
    def _load_cache(self) -> Dict[str, Dict[str, str]]:
        try:
            with open(CACHE_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict) and 'date' in data and 'predictions' in data:
                    return {data['date']: data['predictions']}
                return data  # поддержка будущих форматов
        except FileNotFoundError:
            # создаём каталог при первой записи
            os.makedirs(DATA_DIR, exist_ok=True)
            return {}

    def _save_cache(self) -> None:
        os.makedirs(DATA_DIR, exist_ok=True)
        payload = {
            'date': self.today_key,
            'predictions': self.cache.get(self.today_key, {}),
        }
        with open(CACHE_PATH, 'w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    # ----------------------------- utils -------------------------------
    def _rng_for_today(self) -> random.Random:
        # Стабильный seed по дате через md5, чтобы тип seed был числом
        h = hashlib.md5(self.today_key.encode('utf-8')).hexdigest()[:8]
        seed = int(h, 16)
        return random.Random(seed)


_manager_singleton: DailyPredictionManager | None = None


def get_daily_general_prediction(sign: str) -> str:
    """Функция-обёртка для удобного импорта."""
    global _manager_singleton
    if _manager_singleton is None:
        _manager_singleton = DailyPredictionManager()
    return _manager_singleton.get_general_for_sign(sign)



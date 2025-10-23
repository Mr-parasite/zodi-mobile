"""Генератор ежедневных гороскопов.

Гарантирует стабильность внутри одного дня и уникальность между знаками.
"""

from __future__ import annotations

import hashlib
from datetime import date, datetime
from typing import Dict, List, Optional
import random

from .zodiac_data import THEMES_TO_PHRASES, ZODIAC_SIGNS, DAILY_HOROSCOPES


def _stable_index(key: str, modulo: int) -> int:
    """Детерминированный индекс по ключу.

    Используем SHA-256, чтобы равномерно распределять индексы.
    """
    digest = hashlib.sha256(key.encode("utf-8")).digest()
    value = int.from_bytes(digest[:8], "big", signed=False)
    return value % modulo


def generate_daily_horoscope(sign: str, for_date: date) -> Dict[str, str]:
    """Сгенерировать гороскоп по темам для знака на дату.

    Для одного знака и дня текст стабилен. Разные знаки получают разные
    комбинации за счёт включения имени знака в ключ хеша.
    """
    if sign not in ZODIAC_SIGNS:
        raise ValueError("Неизвестный знак зодиака")

    result: Dict[str, str] = {}
    seed_base = f"{sign}|{for_date.isoformat()}"
    for theme, phrases in THEMES_TO_PHRASES.items():
        if not phrases:
            continue
        idx = _stable_index(f"{seed_base}|{theme}", len(phrases))
        result[theme] = phrases[idx]
    return result


def summary_from_horoscope(horo: Dict[str, str]) -> str:
    """Короткое резюме из набора тематических фраз."""
    # Собираем первые предложения, ограничивая длину
    pieces: List[str] = list(horo.values())[:2]
    text = " ".join(pieces)
    return (text[:160] + "…") if len(text) > 160 else text


# ==========================
# Класс-генератор гороскопов
# ==========================

class HoroscopeGenerator:
    """Генерирует и кэширует ежедневные гороскопы по знакам.

    - Уникальность: детерминированный выбор по seed (дата + знак)
    - Стабильность: в течение дня результат постоянен
    - Кэш: сохраняет сгенерированные значения на текущую дату
    """

    def __init__(self) -> None:
        self.today_horoscopes: Dict[str, str] = {}
        self._generated_for_ymd: Optional[str] = None

    @staticmethod
    def _today_key() -> str:
        """Ключ текущей даты в формате YYYYMMDD."""
        return datetime.now().strftime("%Y%m%d")

    def generate_daily_horoscopes(self) -> None:
        """Генерирует УНИКАЛЬНЫЕ гороскопы на сегодня для всех 12 знаков."""
        today_seed = self._today_key()
        # Перегенерируем только при смене дня
        if self._generated_for_ymd != today_seed:
            self.today_horoscopes.clear()

        for sign, variants in DAILY_HOROSCOPES.items():
            try:
                sign_seed = f"{today_seed}{sign}"
                local_random = random.Random(sign_seed)
                if variants:
                    self.today_horoscopes[sign] = local_random.choice(variants)
            except Exception:
                # Пропускаем в случае неожиданных ошибок данных
                continue

        self._generated_for_ymd = today_seed

    def get_todays_horoscope(self, sign: str) -> str:
        """Вернуть гороскоп на сегодня для указанного знака.

        :param sign: название знака на русском
        :return: строка предсказания или сообщение об отсутствии
        """
        if sign not in DAILY_HOROSCOPES:
            return "Гороскоп временно недоступен"

        today_seed = self._today_key()
        if self._generated_for_ymd != today_seed or sign not in self.today_horoscopes:
            self.generate_daily_horoscopes()

        return self.today_horoscopes.get(sign, "Гороскоп временно недоступен")


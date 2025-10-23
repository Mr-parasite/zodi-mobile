# ZODI Mobile - Космические предсказания

Мобильная версия приложения ZODI для Android и iOS.

## Возможности

- 🔮 Определение знака зодиака по дате рождения
- 🌟 Ежедневные предсказания
- 💑 Калькулятор совместимости
- 👤 Профиль пользователя
- 🔔 Уведомления
- 📱 Адаптивный дизайн

## Установка и запуск

### Локальное тестирование

```bash
# Установка зависимостей
pip install kivy kivymd plyer schedule

# Запуск приложения
python main.py
```

### Сборка для Android

```bash
# Установка buildozer
pip install buildozer

# Сборка APK
buildozer android debug

# Установка на устройство
buildozer android deploy run
```

### Сборка для iOS (только на macOS)

```bash
# Установка kivy-ios
pip install kivy-ios

# Создание проекта
toolchain create zodi .

# Открыть в Xcode
open zodi-ios/zodi.xcodeproj
```

## Структура проекта

```
zodi_mobile/
├── main.py                 # Главный файл
├── buildozer.spec         # Конфигурация Android
├── requirements.txt        # Зависимости
├── core/                  # Бизнес-логика
├── ui/                    # Интерфейс
│   ├── screens/           # Экраны
│   └── themes/           # Темы
├── data/                  # База данных
├── assets/               # Ресурсы
└── utils/                # Утилиты
```

## Технические требования

- Python 3.8+
- Kivy 2.2.1+
- KivyMD 1.1.1+
- Android 5.0+ (API 21+)
- iOS 11.0+

## Разработка

### Добавление новых экранов

1. Создайте файл в `ui/screens/`
2. Наследуйтесь от `Screen`
3. Добавьте экран в `main.py`
 
### Настройка темы

Измените цвета в `ui/themes/zodi_theme.py`

### Добавление анимаций

Используйте Kivy Animation API в экранах

## Лицензия

MIT License

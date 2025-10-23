# Руководство по настройке WSL для сборки APK ZODI

## Проблема
```
WSL2 не поддерживается текущей конфигурацией компьютера.
Включите дополнительный компонент "Платформа виртуальной машины" и включите виртуализацию в BIOS.
```

## Решение

### Шаг 1: Включение виртуализации в BIOS

1. **Перезагрузите компьютер** и войдите в BIOS/UEFI
2. **Найдите настройки виртуализации** (обычно в разделе Advanced или CPU)
3. **Включите следующие опции:**
   - Intel: `Intel Virtualization Technology (VT-x)` = **Enabled**
   - Intel: `Intel VT-d` = **Enabled** (если есть)
   - AMD: `AMD-V` = **Enabled**
   - AMD: `SVM Mode` = **Enabled**
4. **Сохраните настройки** и перезагрузитесь

### Шаг 2: Включение компонентов Windows

Откройте **PowerShell как администратор** и выполните:

```powershell
# Включение компонента "Платформа виртуальной машины"
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# Включение компонента "Платформа виртуальной машины"
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Перезагрузка
Restart-Computer
```

### Шаг 3: Установка WSL

После перезагрузки:

```powershell
# Установка WSL
wsl --install

# Или если уже установлен
wsl --update
wsl --set-default-version 2
```

### Шаг 4: Установка Ubuntu

```powershell
# Установка Ubuntu
wsl --install -d Ubuntu
```

## Альтернативные решения

### Вариант 2: Использование Docker Desktop

Если WSL не работает, можно использовать Docker:

1. **Установите Docker Desktop**
2. **Создайте Dockerfile для сборки APK:**

```dockerfile
FROM ubuntu:20.04

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    python3 python3-pip git \
    openjdk-8-jdk \
    android-sdk \
    build-essential

# Установка buildozer
RUN pip3 install buildozer

# Копирование проекта
COPY . /app
WORKDIR /app

# Сборка APK
CMD ["buildozer", "android", "debug"]
```

### Вариант 3: GitHub Actions (рекомендуется)

Создайте автоматическую сборку APK в облаке:

1. **Создайте файл `.github/workflows/build-apk.yml`:**

```yaml
name: Build ZODI APK

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    
    - name: Install dependencies
      run: |
        pip install buildozer
        sudo apt-get update
        sudo apt-get install -y openjdk-8-jdk
    
    - name: Build APK
      run: |
        cd zodi_mobile
        buildozer android debug
    
    - name: Upload APK
      uses: actions/upload-artifact@v2
      with:
        name: zodi-apk
        path: zodi_mobile/bin/*.apk
```

### Вариант 4: Использование облачных сервисов

- **GitHub Codespaces** - полноценная среда разработки в браузере
- **Replit** - онлайн IDE с поддержкой Android сборки
- **Gitpod** - облачная среда разработки

## Проверка установки

После настройки WSL:

```bash
# Проверка версии WSL
wsl --version

# Проверка установленных дистрибутивов
wsl --list --verbose

# Вход в Ubuntu
wsl -d Ubuntu
```

## Сборка APK в WSL

```bash
# В WSL Ubuntu
sudo apt update
sudo apt install python3-pip
pip3 install buildozer

# Переход в проект
cd /mnt/c/Users/administrator/Zodi/zodi_mobile

# Сборка APK
buildozer android debug
```

## Устранение неполадок

### Если виртуализация не поддерживается:
- Используйте **GitHub Actions** для сборки APK
- Или **Docker Desktop** с Linux контейнером

### Если WSL работает, но buildozer не устанавливается:
```bash
# Обновление пакетов
sudo apt update && sudo apt upgrade

# Установка дополнительных зависимостей
sudo apt install python3-dev python3-setuptools
pip3 install --upgrade pip
pip3 install buildozer
```

### Если APK не собирается:
```bash
# Очистка кэша
buildozer android clean

# Пересборка
buildozer android debug
```

## Результат

После успешной настройки вы сможете:
- ✅ Собирать APK файлы для Android
- ✅ Тестировать приложение на эмуляторе
- ✅ Устанавливать APK на реальные устройства
- ✅ Публиковать в Google Play Store

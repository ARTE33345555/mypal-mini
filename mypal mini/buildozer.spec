[app]

# Название
title = Mini MyPal
package.name = minimypal
package.domain = org.mypal

# Версия
version = 0.1

# Исходники
source.dir = .
source.include_exts = py,png,jpg,kv,json

# Требования (ВАЖНО!)
requirements = python3,kivy,pyjnius,requests,qrcode,pillow

# Ориентация
orientation = portrait

# Полный экран
fullscreen = 0

# Иконка
icon.filename = icon.png

# Разрешения
android.permissions = INTERNET

# Android SDK
android.api = 33
android.minapi = 21
android.ndk = 25b

# Архитектуры (ускоряет сборку)
android.archs = arm64-v8a, armeabi-v7a

# WebView стабильность
android.gradle_dependencies = androidx.webkit:webkit:1.6.0

# Не сохраняем бэкапы
android.allow_backup = False

# Логи
log_level = 2


[buildozer]

log_level = 2
warn_on_root = 1
[app]
title = ZODI
package.name = zodi
package.domain = com.zodi
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,ttf
version = 1.0.0
requirements = python3,kivy==2.2.1,kivymd==1.1.1,plyer,schedule

[buildozer]
log_level = 2
warn_on_root = 1

[android]
api = 33
minapi = 21
ndk = 25b
arch = arm64-v8a
permissions = INTERNET, WRITE_EXTERNAL_STORAGE, VIBRATE, WAKE_LOCK

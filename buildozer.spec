[app]

title = Watermark Maker
package.name = watermarkapp
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# OpenCV directly Android-supported binary compile karta hai
requirements = python3,kivy,opencv

orientation = portrait
fullscreen = 0

android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, READ_MEDIA_VIDEO

android.api = 33
android.minapi = 24
android.ndk = 25c
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1

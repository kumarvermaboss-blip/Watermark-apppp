[app]

# Application metadata
title = Watermark Maker
package.name = watermarkapp
package.domain = org.test

# Source settings
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Minimum C-extension dependencies (FFmpeg handle karega video processing)
requirements = python3,kivy,pillow,ffpyplayer

# App settings
orientation = portrait
fullscreen = 0

# Android Permissions
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, READ_MEDIA_VIDEO

# API Settings
android.api = 33
android.minapi = 24
android.ndk = 25c
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1

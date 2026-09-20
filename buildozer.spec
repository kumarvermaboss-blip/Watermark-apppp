[app]
title = Watermark Maker
package.name = watermarkapp
package.domain = org.test

source.dir =.
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# ffmpeg-kit ke liye pyjnius zaruri hai
requirements = python3,kivy,pillow,android,pyjnius

orientation = portrait
fullscreen = 0

# API 33 ke liye sirf yehi permission
android.permissions = READ_MEDIA_VIDEO
android.api = 33
android.minapi = 24
android.ndk = 25c
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a
android.bootstrap = sdl2

# Ye line sab se important hai, isi se native ffmpeg ayega
android.gradle_dependencies = com.arthenica:ffmpeg-kit-full:4.5.LTS

[buildozer]
log_level = 2
warn_on_root = 1
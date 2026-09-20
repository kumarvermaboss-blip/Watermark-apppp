[app]

title = Watermark Maker
package.name = watermarkapp
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Only pure python dependencies required
requirements = python3,kivy,pillow,android

orientation = portrait
fullscreen = 0

# Android permissions (API 33 compatibility)
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, READ_MEDIA_VIDEO

android.api = 33
android.minapi = 24
android.ndk = 25c
android.accept_sdk_license = True

# Supporting common architectures
android.archs = arm64-v8a, armeabi-v7a

# Gradle dependency for FFmpeg Native Binary
android.gradle_dependencies = com.arthenica:ffmpeg-kit-full:4.5.LTS

[buildozer]
log_level = 2
warn_on_root = 1

[app]

# Application metadata
title = Watermark Maker
package.name = watermarkapp
package.domain = org.test

# Source code settings
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Requirements (numpy version tag removed to prevent git checkout error)
requirements = python3,kivy,numpy,pillow,moviepy,decorator,tqdm,proglog

# App display & orientations
orientation = portrait
fullscreen = 0

# Android Permissions
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, READ_MEDIA_VIDEO

# Android SDK & NDK settings (minapi 24 is required for numpy compilation)
android.api = 33
android.minapi = 24
android.ndk = 25c
android.accept_sdk_license = True
android.archs = arm64-v8a

# Force python-for-android to use master branch for updated build recipes
p4a.branch = master

[buildozer]

log_level = 2
warn_on_root = 1

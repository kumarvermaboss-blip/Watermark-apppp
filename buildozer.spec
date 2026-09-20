[app]

title = Watermark Maker
package.name = watermarkapp
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

requirements = python3,kivy,pillow,android

orientation = portrait
fullscreen = 0

android.permissions = READ_MEDIA_VIDEO, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

android.api = 33
android.minapi = 24
android.ndk = 25c
android.accept_sdk_license = True
android.archs = arm64-v8a
android.bootstrap = sdl2

android.gradle_dependencies = com.arthenica:ffmpeg-kit-full:4.5.LTS

p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1

[app]

# (str) Title of your application
title = Watermark Maker

# (str) Package name
package.name = watermarkapp

# (str) Package domain
package.domain = org.test

# (str) Source code directory
source.dir = .

# (list) Source files
source.include_exts = py,png,jpg,kv,atlas

# (str) Application version
version = 0.1

# (list) Application requirements
requirements = python3,kivy,pillow,moviepy,decorator,tqdm,proglog

# (str) Supported orientation
orientation = portrait

# (bool) Fullscreen
fullscreen = 0

# (list) Permissions for Android 11+ and Media Access
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, READ_MEDIA_VIDEO

# (int) Target Android API
android.api = 33

# (int) Minimum API supported
android.minapi = 21

# (str) Android NDK version
android.ndk = 25c

# (bool) Automatically accept SDK license
android.accept_sdk_license = True

# (str) Target Architecture
android.archs = arm64-v8a

[buildozer]

# (int) Log level
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1

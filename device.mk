#
# Copyright (C) 2020 The LineageOS Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

DEVICE_PATH := device/blackberry/luna

# Vendor blobs
$(call inherit-product, vendor/blackberry/luna/luna-vendor.mk)

# Set Shipping API level
PRODUCT_SHIPPING_API_LEVEL := 27

# Overlays
DEVICE_PACKAGE_OVERLAYS += \
    $(LOCAL_PATH)/overlay

# AAPT
PRODUCT_AAPT_CONFIG := normal
PRODUCT_AAPT_PREF_CONFIG := xxhdpi

# Audio configs
PRODUCT_COPY_FILES += \
    $(call find-copy-subdir-files,*,$(DEVICE_PATH)/configs/audio/,$(TARGET_COPY_OUT_VENDOR)/etc)

# Boot Animation
TARGET_SCREEN_HEIGHT := 1620
TARGET_SCREEN_WIDTH := 1080

# Camera shims
PRODUCT_PACKAGES += \
    libskia_shim \
    libjnigraphics_shim \
    libandroid_shim

# Dalvik
$(call inherit-product, frameworks/native/build/phone-xhdpi-4096-dalvik-heap.mk)

# Device settings
PRODUCT_PACKAGES += \
    DeviceSettings

# GMS
PRODUCT_GMS_CLIENTID_BASE := android-blackberry

# Goodix/fingerprint sensor shims
PRODUCT_PACKAGES += \
    libbinder_shim.vendor \
    libfakelogprint \
    libhidl_shim_full

# Tell common.mk to skip its default media profiles
TARGET_USES_CUSTOM_MEDIA_PROFILES := true

# Inherit from BlackBerry sdm660-common
$(call inherit-product, device/blackberry/sdm660-common/common.mk)

# Add custom luna-specific media profile
PRODUCT_COPY_FILES += \
    $(DEVICE_PATH)/media/media_profiles_V1_0.xml:$(TARGET_COPY_OUT_VENDOR)/etc/media_profiles_V1_0.xml

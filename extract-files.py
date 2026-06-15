#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

import extract_utils.tools
extract_utils.tools.DEFAULT_PATCHELF_VERSION = '0_9'

namespace_imports = [
    'device/blackberry/sdm660-common',
    'hardware/qcom-caf/msm8998',
    'hardware/qcom-caf/wlan',
    'vendor/blackberry/sdm660-common',
]

blob_fixups: blob_fixups_user_type =        {
    # Protobuf for audio and goodix
    ('vendor/lib/libwebrtc_audio_preprocessing.so',
     'vendor/lib64/libwebrtc_audio_preprocessing.so'
     ): blob_fixup()
        .replace_needed('libprotobuf-cpp-lite.so', 'libprotobuf-cpp-lite-v29.so'),

    ('vendor/lib64/hw/gxfingerprint.default.so',
     'vendor/lib64/libgf_ca.so',
     'vendor/lib64/libgf_hal.so',
     'vendor/lib64/libvendor.goodix.hardware.fingerprint@1.0.so',
     'vendor/lib64/libvendor.goodix.hardware.fingerprint@1.0-service.so',
     'vendor/lib64/libgoodixfingerprintd_binder.so',
     'vendor/lib64/hw/fingerprint.gf3206.so'
        ): blob_fixup()
        .replace_needed('libprotobuf-cpp-lite.so', 'libprotobuf-cpp-lite-v29.so')
        .remove_needed('libandroid_runtime.so')
        .remove_needed('libkeystore_binder.so')
        .remove_needed('ld-android.so')
        .remove_needed('libbacktrace.so')
        .remove_needed('libunwind.so')
        .remove_needed('libkeystore_binder.so')
        .remove_needed('libsoftkeymasterdevice.so')
        .remove_needed('libsoftkeymaster.so')
        .remove_needed('libkeymaster_messages.so')
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so')
        .add_needed('libhidlbase.so')
        .add_needed('libbinder_shim.so')
        .binary_regex_replace(b'/system/etc/firmware', b'/vendor/firmware\x00\x00\x00\x00'),
    ('vendor/lib/libarcsoft_dualcam_refocus.so',
     'vendor/lib/libdualcameraddm.so',
     'vendor/lib64/libdualcameraddm.so',
     'vendor/lib/libmmcamera_hdr_gb_lib.so'
     'vendor/lib/libarcsoft_dualcam_refocus.so',
     'vendor/lib/libarcsoft_low_light_shot',
     'vendor/lib/libarcsoft_nighthawk.so',
     'vendor/lib/liboptizoom.so',
     'vendor/lib64/liboptizoom.so',
     'vendor/lib/libchromaflash.so',
     'vendor/lib64/libchromaflash.so',
     'vendor/lib/libseemore.so',
     'vendor/lib64/libseemore.so'
     'vendor/lib/libvideobokeh.so',
     'vendor/lib64/libvideobokeh.so',
     'vendor/lib/libVDSuperPhotoAPI.so',
     'vendor/lib/libcamera_imgproc.so',
     'vendor/lib/libubifocus.so'): blob_fixup()
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
    'vendor/lib/libmmcamera_trueportrait_lib.so': blob_fixup()
        .remove_needed('libtrueportrait.so'),
    'vendor/lib/libmmcamera_llvd.so': blob_fixup()
        .remove_needed('libllvd_smore.so'),
    # camera.sdm660.so — OREO HAL, libskia no longer in vendor
    'vendor/lib/hw/camera.sdm660.so': blob_fixup()
        .replace_needed('libskia.so', 'libskia_shim.so'),
    # libjnigraphics and libandroid not available in vendor
    'vendor/lib/libcamera_imgproc.so': blob_fixup()
        .remove_needed('libjnigraphics.so'),
    'vendor/lib/libopencv_java3.so': blob_fixup()
        .replace_needed('libjnigraphics.so', 'libjnigraphics_shim.so'),
    'vendor/lib/libVDSuperPhotoAPI.so': blob_fixup()
        .replace_needed('libjnigraphics.so', 'libjnigraphics_shim.so')
        .remove_needed('libandroid.so'),
    'vendor/lib/libVDBeautyShotAPI.so': blob_fixup()
        .replace_needed('libjnigraphics.so', 'libjnigraphics_shim.so')
        .replace_needed('libandroid.so', 'libandroid_shim.so'),
    # Added helper to resolve symbols from libc
    'vendor/lib/libmmcamera_interface.so': blob_fixup()
        .add_needed('libandroid_shim.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'luna',
    'blackberry',
    namespace_imports=namespace_imports,
    blob_fixups=blob_fixups,
)

if __name__ == '__main__':
    utils = ExtractUtils.device_with_common(
        module, 'sdm660-common', module.vendor
    )
    utils.run()

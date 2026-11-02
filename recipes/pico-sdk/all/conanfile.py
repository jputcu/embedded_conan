import os

from conan import ConanFile
from conan.tools.files import copy, get, save

# The SDK's own toolchain file per core: its flags reach every package built for that core
TOOLCHAINS = {
    "cortex-m0plus": "pico_arm_cortex_m0plus_gcc.cmake",
    "cortex-m33": "pico_arm_cortex_m33_gcc.cmake",
}


class PicoSdkConan(ConanFile):
    name = "pico-sdk"
    description = "The Raspberry Pi Pico SDK as sources, without its submodules (tinyusb, cyw43-driver, lwip, btstack, mbedtls)"
    license = "BSD-3-Clause"
    homepage = "https://github.com/raspberrypi/pico-sdk"
    package_type = "header-library"  # nothing is compiled here, see package_info()
    no_copy_source = True

    def source(self):
        # url and sha256: a download that changed upstream fails instead of slipping in
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def package(self):
        copy(self, "*", self.source_folder, os.path.join(self.package_folder, "sdk"))
        # pico_sdk_init() puts sdk/cmake on the module path for Platform/PICO.cmake; a project
        # that is not an SDK one (a library) only gets the toolchain file, so the wrapper does it
        for core, toolchain in TOOLCHAINS.items():
            save(self, os.path.join(self.package_folder, "toolchain", f"{core}.cmake"),
                 'list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/../sdk/cmake")\n'
                 f'include("${{CMAKE_CURRENT_LIST_DIR}}/../sdk/cmake/preload/toolchains/{toolchain}")\n')

    def package_id(self):
        self.info.clear()  # the same sources for every board and host

    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.bindirs = []
        sdk = os.path.join(self.package_folder, "sdk")
        self.buildenv_info.define_path("PICO_SDK_PATH", sdk)
        # As a profile's tool_requires: the SDK's toolchain for every CMake package of that core,
        # so libraries built outside the SDK get its compiler flags and follow its upgrades
        if self.settings_target is not None and str(self.settings_target.arch) in TOOLCHAINS:
            toolchain = os.path.join(self.package_folder, "toolchain", f"{self.settings_target.arch}.cmake")
            self.conf_info.append("tools.cmake.cmaketoolchain:user_toolchain", toolchain)
            self.conf_info.define("tools.cmake.cmaketoolchain:system_name", "PICO")

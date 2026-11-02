import os

from conan import ConanFile
from conan.tools.files import copy, get


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

    def package_id(self):
        self.info.clear()  # the same sources for every board and host

    def package_info(self):
        # The SDK loads before project(), so a CMake module from find_package() comes too late:
        # consumers pass self.dependencies["pico-sdk"].package_folder + "/sdk" as PICO_SDK_PATH
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.bindirs = []
        self.buildenv_info.define_path("PICO_SDK_PATH", os.path.join(self.package_folder, "sdk"))

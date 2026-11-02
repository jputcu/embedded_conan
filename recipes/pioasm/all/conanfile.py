import os

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import get
from conan.tools.layout import basic_layout


class PioasmConan(ConanFile):
    name = "pioasm"
    description = "Raspberry Pi's assembler for PIO programs: .pio files to C headers"
    license = "BSD-3-Clause"
    homepage = "https://github.com/raspberrypi/pico-sdk/tree/master/tools/pioasm"
    package_type = "application"
    settings = "os", "arch"

    def layout(self):
        basic_layout(self)

    def validate(self):
        if str(self.settings.arch) not in self.conan_data["sources"][self.version].get(str(self.settings.os), {}):
            raise ConanInvalidConfiguration(f"No prebuilt pioasm for {self.settings.os} {self.settings.arch}")

    def package(self):
        # url and sha256: a download that changed upstream fails instead of slipping in.
        # Everything is in pioasm/: the binary and its CMake config
        get(self, **self.conan_data["sources"][self.version][str(self.settings.os)][str(self.settings.arch)],
            destination=self.package_folder)

    def package_info(self):
        # Consumers point the SDK at it with pioasm_DIR = <package_folder>/pioasm
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.bindirs = ["pioasm"]
        self.cpp_info.builddirs = ["pioasm"]
        self.cpp_info.set_property("cmake_find_mode", "none")  # the SDK uses pioasm's own config

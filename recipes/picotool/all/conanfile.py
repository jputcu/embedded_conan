import os

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import get
from conan.tools.layout import basic_layout


class PicotoolConan(ConanFile):
    name = "picotool"
    description = "Raspberry Pi's tool for RP2040/RP2350 binaries and devices: UF2 output, signing, flashing"
    license = "BSD-3-Clause"
    homepage = "https://github.com/raspberrypi/picotool"
    package_type = "application"
    settings = "os", "arch"

    def layout(self):
        basic_layout(self)

    def validate(self):
        if str(self.settings.arch) not in self.conan_data["sources"][self.version].get(str(self.settings.os), {}):
            raise ConanInvalidConfiguration(f"No prebuilt picotool for {self.settings.os} {self.settings.arch}")

    def package(self):
        # url and sha256: a download that changed upstream fails instead of slipping in.
        # Everything is in picotool/: the binary finds its data files next to itself
        get(self, **self.conan_data["sources"][self.version][str(self.settings.os)][str(self.settings.arch)],
            destination=self.package_folder)

    def package_info(self):
        # On Linux the binary needs the system libusb-1.0 (Debian: libusb-1.0-0).
        # Consumers point the SDK at it with picotool_DIR = <package_folder>/picotool
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.bindirs = ["picotool"]
        self.cpp_info.builddirs = ["picotool"]
        self.cpp_info.set_property("cmake_find_mode", "none")  # the SDK uses picotool's own config

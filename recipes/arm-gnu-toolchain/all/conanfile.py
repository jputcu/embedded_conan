import os

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import get
from conan.tools.layout import basic_layout


class ArmGnuToolchainConan(ConanFile):
    name = "arm-gnu-toolchain"
    description = "Arm's prebuilt GNU toolchain for bare-metal Arm (arm-none-eabi): gcc, binutils, newlib, gdb"
    license = ("GPL-3.0-or-later", "LGPL-3.0-or-later", "BSD-3-Clause")
    homepage = "https://gitlab.arm.com/tooling/gnu-toolchains-for-arm"
    package_type = "application"
    settings = "os", "arch"

    def layout(self):
        basic_layout(self)

    def validate(self):
        if str(self.settings.arch) not in self.conan_data["sources"][self.version].get(str(self.settings.os), {}):
            raise ConanInvalidConfiguration(f"No prebuilt arm-none-eabi toolchain for {self.settings.os} {self.settings.arch}")

    def package(self):
        # url and sha256: a download that changed upstream fails instead of slipping in
        get(self, **self.conan_data["sources"][self.version][str(self.settings.os)][str(self.settings.arch)],
            strip_root=True, destination=self.package_folder)

    def package_info(self):
        suffix = ".exe" if self.settings.os == "Windows" else ""
        toolchain = os.path.join(self.package_folder, "bin", "arm-none-eabi")
        self.conf_info.define("tools.build:compiler_executables", {
            "c": f"{toolchain}-gcc{suffix}",
            "cpp": f"{toolchain}-g++{suffix}",
            "asm": f"{toolchain}-gcc{suffix}",
        })
        # The Pico SDK's toolchain file looks here before the PATH
        self.buildenv_info.define_path("PICO_TOOLCHAIN_PATH", self.package_folder)

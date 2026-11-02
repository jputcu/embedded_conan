import os

from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout


class BlinkRecipe(ConanFile):
    name = "blink"
    version = "1.0"
    package_type = "application"

    settings = "os", "compiler", "build_type", "arch"

    exports_sources = "CMakeLists.txt", "src/*"

    def requirements(self):
        self.requires("pico-sdk/2.3.1")

    def layout(self):
        self.folders.build_folder_vars = ["settings.arch"]
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        # The SDK loads before project(), so these must be cache variables
        pico_sdk = os.path.join(self.dependencies["pico-sdk"].package_folder, "sdk").replace("\\", "/")
        tc.cache_variables["PICO_SDK_PATH"] = pico_sdk
        tc.cache_variables["PICO_PLATFORM"] = "rp2040"
        tc.cache_variables["PICO_BOARD"] = "pico"
        # The SDK's toolchain file, and the system name it sets, which Conan would replace
        tc.blocks["user_toolchain"].values["paths"] = [
            f"{pico_sdk}/cmake/preload/toolchains/pico_arm_cortex_m0plus_gcc.cmake"]
        tc.blocks["generic_system"].values["cmake_system_name"] = "PICO"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

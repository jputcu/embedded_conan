import os

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout


# Per core: the SDK's platform and a board with an LED on PICO_DEFAULT_LED_PIN
PLATFORMS = {
    "cortex-m0plus": ("rp2040", "pico"),
    "cortex-m33": ("rp2350-arm-s", "pico2"),
}


class BlinkRecipe(ConanFile):
    name = "blink"
    version = "1.0"
    package_type = "application"

    settings = "os", "compiler", "build_type", "arch"

    exports_sources = "CMakeLists.txt", "src/*"

    def build_requirements(self):
        self.tool_requires("picotool/2.3.1")

    def validate(self):
        if str(self.settings.arch) not in PLATFORMS:
            raise ConanInvalidConfiguration(f"No Pico board for arch {self.settings.arch}")

    def layout(self):
        self.folders.build_folder_vars = ["settings.arch"]
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        # The SDK and its toolchain come from the profile's tool_requires; it loads before
        # project(), so these must be cache variables
        pico_sdk = os.path.join(self.dependencies.build["pico-sdk"].package_folder, "sdk").replace("\\", "/")
        tc.cache_variables["PICO_SDK_PATH"] = pico_sdk
        platform, board = PLATFORMS[str(self.settings.arch)]
        tc.cache_variables["PICO_PLATFORM"] = platform
        tc.cache_variables["PICO_BOARD"] = board
        # The packaged picotool for the UF2, instead of the SDK downloading and building one
        tc.cache_variables["picotool_DIR"] = os.path.join(
            self.dependencies.build["picotool"].package_folder, "picotool").replace("\\", "/")
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

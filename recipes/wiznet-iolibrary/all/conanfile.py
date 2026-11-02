import os

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.files import copy, get


class WiznetIoLibraryConan(ConanFile):
    name = "wiznet-iolibrary"
    description = "WIZnet's ioLibrary Ethernet driver (socket API) for one W5x00/W6x00 chip"
    license = "MIT"
    homepage = "https://github.com/Wiznet/ioLibrary_Driver"
    package_type = "static-library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "chip": ["W5100", "W5100S", "W5200", "W5300", "W5500", "W6100", "W6300"],
        # socket(), connect(), ... prefixed, so they cannot meet the C library's BSD socket names
        "prefixed_exports": [True, False],
    }
    default_options = {"chip": "W6100", "prefixed_exports": True}
    exports_sources = "CMakeLists.txt"

    def configure(self):
        self.settings.rm_safe("compiler.libcxx")  # C only
        self.settings.rm_safe("compiler.cppstd")

    def layout(self):
        cmake_layout(self)

    def source(self):
        # url and sha256: a download that changed upstream fails instead of slipping in
        get(self, **self.conan_data["sources"][self.version], strip_root=True, destination="iolibrary")

    def generate(self):
        tc = CMakeToolchain(self)
        tc.cache_variables["IOLIBRARY_SOURCE_DIR"] = os.path.join(self.source_folder, "iolibrary").replace("\\", "/")
        tc.cache_variables["WIZCHIP"] = str(self.options.chip)
        tc.cache_variables["WIZCHIP_PREFIXED_EXPORTS"] = bool(self.options.prefixed_exports)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "license.txt", os.path.join(self.source_folder, "iolibrary"),
             os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["wiznet-iolibrary"]
        # The chip's header includes wizchip_conf.h from the folder above it
        self.cpp_info.includedirs = [os.path.join("include", "Ethernet"),
                                     os.path.join("include", "Ethernet", str(self.options.chip))]
        self.cpp_info.defines = [f"_WIZCHIP_={self.options.chip}"]
        if self.options.prefixed_exports:
            self.cpp_info.defines.append("WIZCHIP_PREFIXED_EXPORTS=1")
        self.cpp_info.set_property("cmake_target_name", "wiznet-iolibrary::wiznet-iolibrary")

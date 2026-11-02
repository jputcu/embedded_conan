Description
===========
Conan recipes for embedded development: cross toolchains, the AVR C++ standard library, the
Raspberry Pi Pico SDK and its tools, and portable sources such as the FreeRTOS kernel.

Recipes
-------

| Recipe | Versions | What |
|--------|----------|------|
| [`microchipavrgcc`](https://www.microchip.com/en-us/tools-resources/develop/microchip-studio/gcc-compilers) | 3.7.0, 4.0.0 | Microchip's prebuilt AVR toolchain (avr-gcc 7, 15) |
| [`zakkembleavrgcc`](https://github.com/ZakKemble/avr-gcc-build) | 8.1.0 ... 16.1.0 | Zak Kemble's prebuilt avr-gcc builds |
| [`ctngavrgcc`](https://crosstool-ng.github.io) | 16.2.0 | avr-gcc with a freestanding libstdc++, built from source by crosstool-ng |
| [`avr-libstdcpp`](https://github.com/modm-io/avr-libstdcpp) | 1.0.1 | A C++ standard library for AVR (modm-io), header-only |
| [`arm-gnu-toolchain`](https://gitlab.arm.com/tooling/gnu-toolchains-for-arm) | 15.3.rel2 | Arm's prebuilt bare-metal toolchain (arm-none-eabi) |
| [`pico-sdk`](https://github.com/raspberrypi/pico-sdk) | 2.3.1 | Raspberry Pi Pico SDK as sources (no submodules); its toolchain and flags for RP2040/RP2350 |
| [`picotool`](https://github.com/raspberrypi/picotool) | 2.3.1 | Raspberry Pi's prebuilt picotool: UF2 output, signing, flashing |
| [`pioasm`](https://github.com/raspberrypi/pico-sdk/tree/master/tools/pioasm) | 2.3.1 | Raspberry Pi's prebuilt PIO assembler |
| [`freertos-kernel`](https://github.com/FreeRTOS/FreeRTOS-Kernel) | 11.3.1, 11.3.2 | FreeRTOS kernel as sources, built by the application with its own config and port |
| [`wiznet-iolibrary`](https://github.com/Wiznet/ioLibrary_Driver) | cci.20261008 | WIZnet's ioLibrary Ethernet driver for one W5x00/W6x00 chip |

Install toolchain and C++ standard library
------------------------------------------

This repository is origanized to allow it to be used as a local conan index.

~~~~
$ git clone https://github.com/jputcu/embedded_conan.git
$ conan remote add embedded ./embedded_conan
$ conan search "*" -r embedded
Found 22 pkg/version recipes matching * in embedded
...
~~~~

The correct packages will be installed as dependency by the profile.


### Compile GNU C++ cross compiler from source

`ctngavrgcc` builds avr-gcc with a freestanding libstdc++ through crosstool-ng (Linux
only, about an hour). The component versions are in `recipes/ctngavrgcc/all/defconfigs`.

~~~~
$ conan create recipes/ctngavrgcc/all --version 16.2.0 --build-require
~~~~

Provide the conan settings
------------------------------

Install `conan/settings_user.yml` into `~/.conan2/`: it declares the AVR MCU, the `cortex-m0plus`
and `cortex-m33` archs and `compiler.lto`.

Compile the example project
---------------------------
The example builds `MinSizeRel` with LTO and `-g` from the profile, so the image is optimized
and the ELF still has the symbols for `avr-gdb`. A `Debug` build (`-O0`) is not shown:
on AVR it rarely fits and breaks `<util/delay.h>`.

~~~~
$ cd examples/avr/blink
$ conan build . -pr:h ../profiles/arduino_uno --build missing
...
$ file build/atmega328p/MinSizeRel/blink.elf
build/atmega328p/MinSizeRel/blink.elf: ELF 32-bit LSB executable, Atmel AVR 8-bit, version 1 (SYSV), statically linked, with debug_info, not stripped
~~~~

Advanced editors, like Clion, can use `cmake presets`:
~~~~
$ conan install . -pr:h ../profiles/arduino_uno --build missing
...
$ cmake --list-presets
Available configure presets:

  "conan-atmega328p-minsizerel" - 'conan-atmega328p-minsizerel' config
~~~~

Or by hand, in the toolchain's environment:
~~~~
$ source build/atmega328p/MinSizeRel/generators/conanbuild.sh
$ cmake --preset conan-atmega328p-minsizerel
...
$ cmake --build --preset conan-atmega328p-minsizerel --verbose
...
$ source build/atmega328p/MinSizeRel/generators/deactivate_conanbuild.sh
Restoring environment
~~~~

Run correct gdb
---------------
Since conan-2.23 we can easily call the correct gdb:
~~~~
$ conan run "avr-gdb --version" -pr ../profiles/arduino_uno
Installing and building dependencies, this might take a while...
GNU gdb (AVR_8_bit_GNU_Toolchain_4.0.0_52) 16.3
...
~~~~

Compile the Pico example
------------------------
One blink for the Raspberry Pi Pico (RP2040) and Pico 2 (RP2350, ARM secure mode): the profile's
arch picks the SDK platform and board. The compiler is Arm's `arm-gnu-toolchain` and `pico-sdk` comes
as sources, without its submodules (no USB, no wireless); both from this index and pinned. The
profiles take them as `tool_requires`: the SDK's toolchain file then configures every CMake package
built with them, so a library gets the SDK's compiler flags too.

~~~~
$ cd examples/pico/blink
$ conan build . -pr:h ../profiles/pico --build missing
...
$ conan build . -pr:h ../profiles/pico2 --build missing
...
$ ls build/*/Release/blink.uf2
build/cortex-m0plus/Release/blink.uf2  build/cortex-m33/Release/blink.uf2
~~~~

The build types follow the SDK: `Release` (`-O3`, the SDK adds `-g`) by default, and `Debug`
(`-Og`, still small enough to step through with a debug probe) with `-s build_type=Debug`.

The UF2 comes from the `picotool` package (Raspberry Pi's prebuilt binary; on Linux it needs the
system `libusb-1.0`). Hold BOOTSEL while plugging in the board and copy `blink.uf2` to the drive
that appears.

Potential
=========

Other compiler
--------------
* Arduino AVR toolchain
* PlatformIO AVR toolchain
* https://github.com/modm-io/avr-gcc
* https://blog.zakkemble.net/avr-gcc-builds/
* Build AVR toolchain from source
* crosstool-ng, more specifically: https://github.com/crosstool-ng/crosstool-ng/issues/2234

Offer HALs
----------
* TODO

AVR friendly libraries
----------------------
From ConanCenter, at the versions used on AVR:

* `etl/20.48.1`: [ETL](https://github.com/ETLCPP/etl), containers and algorithms without heap
* `arduinojson/6.21.4`: [ArduinoJson](https://arduinojson.org), ConanCenter's newest 6.x; version 7 dropped
  the fixed-size `StaticJsonDocument` and allocates from the heap by default

AVR architecture
----------------
Conan settings have the MCU specified as arch, this means no reuse between other atmegas.
Perhaps we can use the `arch` there.


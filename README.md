Description
===========
Conan recipes for embedded development: cross toolchains, the AVR C++ standard library and
portable sources such as the FreeRTOS kernel.

Install toolchain and C++ standard library
------------------------------------------

This repository is origanized to allow it to be used as a local conan index.

~~~~
$ git clone https://github.com/jputcu/embedded_conan.git
$ conan remote add embedded ./embedded_conan
$ conan search "*" -r embedded
Found 17 pkg/version recipes matching * in embedded
embedded
  avr-libstdcpp
    avr-libstdcpp/1.0.1
  ctngavrgcc
    ctngavrgcc/16.2.0
  freertos-kernel
    freertos-kernel/11.3.1
    freertos-kernel/11.3.2
  microchipavrgcc
    microchipavrgcc/3.7.0
    microchipavrgcc/4.0.0
  zakkembleavrgcc
    zakkembleavrgcc/8.1.0
    ...
    zakkembleavrgcc/16.1.0
~~~~

The correct packages will be installed as dependency by the profile.


### Compile GNU C++ cross compiler from source

`ctngavrgcc` builds avr-gcc with a freestanding libstdc++ through crosstool-ng (Linux
only, about an hour). The component versions are in `recipes/ctngavrgcc/all/defconfigs`.

~~~~
$ conan create recipes/ctngavrgcc/all --version 16.2.0 --build-require
~~~~

Provide the conan AVR settings
------------------------------

Install `conan/settings_user.yml` into `~/.conan2/`: it declares the MCU and `compiler.lto`.

Compile the example project
---------------------------
The example builds like our firmware: `MinSizeRel` with LTO and `-g` from the profile, so the
image is optimized and the ELF still has the symbols for `avr-gdb`. A `Debug` build (`-O0`) is not shown:
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
* ETL
* ArduinoJson

AVR architecture
----------------
Conan settings have the MCU specified as arch, this means no reuse between other atmegas.
Perhaps we can use the `arch` there.


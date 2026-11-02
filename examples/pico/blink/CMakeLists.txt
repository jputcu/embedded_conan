cmake_minimum_required(VERSION 3.25)

include(${PICO_SDK_PATH}/external/pico_sdk_import.cmake)
project(blink C CXX ASM)
pico_sdk_init()

add_executable(blink src/main.cpp)
target_link_libraries(blink PRIVATE pico_stdlib)
target_compile_options(blink PRIVATE -Wall -Wextra)
pico_add_uf2_output(blink)
pico_add_bin_output(blink)
pico_add_hex_output(blink)

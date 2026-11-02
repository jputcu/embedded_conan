cmake_minimum_required(VERSION 3.15)
project(test_package C)

find_package(wiznet-iolibrary REQUIRED CONFIG)
add_library(test_package STATIC test_package.c)
target_link_libraries(test_package PRIVATE wiznet-iolibrary::wiznet-iolibrary)

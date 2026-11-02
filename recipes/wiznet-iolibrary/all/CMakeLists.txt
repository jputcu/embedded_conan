cmake_minimum_required(VERSION 3.15)
project(wiznet_iolibrary C)

# Upstream has no build files: the Ethernet driver for one chip, as WIZnet's examples build it
set(ETH ${IOLIBRARY_SOURCE_DIR}/Ethernet)
string(TOLOWER ${WIZCHIP} chip_file)
add_library(wiznet-iolibrary STATIC ${ETH}/socket.c ${ETH}/wizchip_conf.c ${ETH}/${WIZCHIP}/${chip_file}.c)
target_include_directories(wiznet-iolibrary PRIVATE ${ETH} ${ETH}/${WIZCHIP})
target_compile_definitions(wiznet-iolibrary PUBLIC _WIZCHIP_=${WIZCHIP}
        $<$<BOOL:${WIZCHIP_PREFIXED_EXPORTS}>:WIZCHIP_PREFIXED_EXPORTS=1>)
# Third-party code: its warnings must not fail a -Werror build
set_target_properties(wiznet-iolibrary PROPERTIES COMPILE_WARNING_AS_ERROR OFF)

install(TARGETS wiznet-iolibrary ARCHIVE DESTINATION lib)
# Upstream's layout: wizchip_conf.h includes ./<chip>/<chip>.h and ../Application/Application.h
install(FILES ${ETH}/socket.h ${ETH}/wizchip_conf.h DESTINATION include/Ethernet)
install(FILES ${ETH}/${WIZCHIP}/${chip_file}.h DESTINATION include/Ethernet/${WIZCHIP})
install(FILES ${IOLIBRARY_SOURCE_DIR}/Application/Application.h DESTINATION include/Application)

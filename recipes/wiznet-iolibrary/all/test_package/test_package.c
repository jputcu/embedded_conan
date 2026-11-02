#include "socket.h"

// socket() is wizchip_socket() with WIZCHIP_PREFIXED_EXPORTS, as the package defines it
int8_t open_socket(void) { return socket(0, Sn_MR_TCP, 5000, 0); }

#include "pico/stdlib.h"

int main() {
  gpio_init(PICO_DEFAULT_LED_PIN);
  gpio_set_dir(PICO_DEFAULT_LED_PIN, GPIO_OUT);
  while (true) {
    gpio_xor_mask(1u << PICO_DEFAULT_LED_PIN);
    sleep_ms(500);
  }
}

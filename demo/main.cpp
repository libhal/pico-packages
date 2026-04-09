#include <cstdio>

#include "hardware/gpio.h"
#include "pico/stdio.h"
#include "pico/time.h"

int
main()
{
  gpio_set_function(46, gpio_function_t::GPIO_FUNC_SIO);
  gpio_set_dir(46, GPIO_OUT);
  stdio_init_all();
  while (true) {
    gpio_put(46, true);
    printf("On!\n");
    sleep_ms(500);
    gpio_put(46, false);
    printf("Off!\n");
    sleep_ms(500);
  }
}

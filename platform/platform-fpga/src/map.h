#if defined(__BOARD_zynqmp__)
# define GPIO_RESET_BASE_ADDR 0x80010000
# define JTAG_BASE_ADDR       0x80011000
#elif defined(__BOARD_zynq__)
# define GPIO_RESET_BASE_ADDR 0x41200000
# define JTAG_BASE_ADDR       0x43c00000
#else
# error unsupported BOARD
#endif

void init_map();
void resetn(int val);
void finish_map();

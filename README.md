## PRM Software

```
.
├── apps                 # platform-independent applications
│   ├── axi-loader       # loader to loader image and reset for the RISC-V subsystem
│   ├── dbg              # simple external debugger for RISC-V subsystem
│   ├── pardctl          # control plane access tools
│   ├── rbb-server       # unused
│   └── stab             # control plane statistic table dumper
├── common               # platform-independent codes shared by `apps`
├── Makefile.app
├── Makefile.check
├── Makefile.compile
├── Makefile.lib
├── misc
│   ├── dtb              # DTB for RISC-V subsystem
│   ├── linux-config     # Linux config for PS of zynq and zynqmp
│   └── scripts
├── platform             # platform-dependent code
│   ├── platform-emu
│   └── platform-fpga
└── README.md            # this file
```

jtag硬件以上层次的软件都放在本目录下, 包括jtag驱动, DTM驱动, 控制平面访问等. 目录组织类似AM, 分3部分:
* `platform/` - 包括平台相关的代码, 如jtag访问方式, 平台初始化等工作.
目前平台包括`emu`和`fpga`, 其中`emu`用于仿真, `fpga`用于上板
* `apps/` - 平台无关的应用
* `common/` - 平台无关但可以被`apps`共享的代码

注意:
* 将本目录拷贝到ARM核上编译, 即可得到ARM上运行的可执行文件
* 关于DTM, jtag等模块的关系, 请查阅riscv debug specification

This directory contains functions above the jtag hardware,
including jtag driver, DTM driver, control plane accessing.
* `platform/` - platform-dependent code, including jtag accessing, platform initialization.
Currently, there are two platforms. `emu` is used for running over emulation, and `fpga` is used for running over FPGA
* `apps/` - platform-independent applications
* `common/` - platform-independent codes shared by `apps`

NOTE:
* Copying this directory to the ARM system and compile will get the ARM executables
* For details about the relationship between DTM and jtag, please refer to riscv debug specification

## Compile

在`apps/xxx`目录下运行`make`, 默认将程序编译到`emu`平台, 编译结果位于`apps/xxx/build/xxx-emu`.
可以通过`make PLATFORM=fpga`将程序编译到`fpga-zynqmp`平台.
若使用`zynq`的FPGA, 需要手动指定`BOARD`参数: `make PLATFORM=fpga BOARD=zynq`.

Running `make` under `apps/[app name]/` will compile the application to `emu` platform by default.
Executable will be generated as `apps/[app name]/build/[app name]-emu`.
To compile the application to zynqmp FPGA platform, run `make PLATFORM=fpga` under the application directory.
If you use a zynq FPGA, a `BOARD` argument should be specified: `make PLATFORM=fpga BOARD=zynq`.

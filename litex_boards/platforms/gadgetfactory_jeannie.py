# This file is Copyright (c) 2019 Tom Keddie <git@bronwenandtom.com>
# License: BSD

# Fomu Hacker board:
# - Design files: https://github.com/im-tomu/fomu-hardware/tree/master/hacker/releases/v0.0-19-g154fecc

from litex.build.generic_platform import *
from litex.build.lattice import LatticePlatform
from litex.build.lattice.programmer import IceStormProgrammer

# IOs ----------------------------------------------------------------------------------------------

_io = [
    # Clk / Rst
    ("clk48", 0, Pins("20"), IOStandard("LVCMOS33")),

    # Leds
    ("user_led_n", 0, Pins("41"), IOStandard("LVCMOS33")),
    ("rgb_led", 0,
        Subsignal("r", Pins("41")),
        Subsignal("g", Pins("40")),
        Subsignal("b", Pins("39")),
        IOStandard("LVCMOS33"),
    ),

    # Serial 
    ("serial", 0,
        Subsignal("rx", Pins("21")),
        Subsignal("tx", Pins("28"), Misc("PULLUP")),
        IOStandard("LVCMOS33")
    ),  # (Serial0 on CM4 bus)

    ("serial", 1,
        Subsignal("rx", Pins("2")),
        Subsignal("tx", Pins("13"), Misc("PULLUP")),
        IOStandard("LVCMOS33")
    ),  # (Serial5 on CM4 bus)

    # USB
    ("usb", 0,
        Subsignal("d_p", Pins("32")),
        Subsignal("d_n", Pins("31")),
        Subsignal("pullup",   Pins("34")),
        # Subsignal("pulldown", Pins("36")),
        IOStandard("LVCMOS33")
    ),

    # SPIFlash
    ("spiflash", 0,
        Subsignal("cs_n", Pins("16"), IOStandard("LVCMOS33")),
        Subsignal("clk",  Pins("15"), IOStandard("LVCMOS33")),
        Subsignal("miso", Pins("17"), IOStandard("LVCMOS33")),
        Subsignal("mosi", Pins("14"), IOStandard("LVCMOS33")),
    ),

    ("spiflash4x", 0,
        Subsignal("cs_n", Pins("16"), IOStandard("LVCMOS33")),
        Subsignal("clk",  Pins("15"), IOStandard("LVCMOS33")),
        Subsignal("dq",   Pins("14 17"), IOStandard("LVCMOS33")),
    ),

    # I2C
    ("i2c", 0,
        Subsignal("scl", Pins("35"), IOStandard("LVCMOS18")),
        Subsignal("sda", Pins("34"), IOStandard("LVCMOS18")),
    ),  # (i2c0 on CM4 bus)

    ("i2c", 1,
        Subsignal("scl", Pins("37"), IOStandard("LVCMOS18")),
        Subsignal("sda", Pins("36"), IOStandard("LVCMOS18")),
    ),  # (i2c1 on CM4 bus)

    ("i2c", 2,
        Subsignal("scl", Pins("19"), IOStandard("LVCMOS18")),
        Subsignal("sda", Pins("44"), IOStandard("LVCMOS18")),
    ),  # (i2c6 on CM4 bus)

    # SPI
    ("spi", 0,
        Subsignal("cs", Pins("38"), IOStandard("LVCMOS18")),
        Subsignal("clk", Pins("18"), IOStandard("LVCMOS18")),
        Subsignal("miso", Pins("46"), IOStandard("LVCMOS18")),
        Subsignal("mosi", Pins("47"), IOStandard("LVCMOS18")),
    ),  # (SPI4 on CM4 bus)

    ("spi", 1,
        Subsignal("cs", Pins("12"), IOStandard("LVCMOS18")),
        Subsignal("clk", Pins("10"), IOStandard("LVCMOS18")),
        Subsignal("miso", Pins("6"), IOStandard("LVCMOS18")),
        Subsignal("mosi", Pins("11"), IOStandard("LVCMOS18")),
    ),  # (SPI6 on CM4 bus)

    # HDMI
    ("hdmi_out", 0,
        Subsignal("clk_p",       Pins("26"), IOStandard("TMDS_33")),
        Subsignal("clk_n",       Pins("27"), IOStandard("TMDS_33")),
        Subsignal("data0_p",     Pins("23"), IOStandard("TMDS_33")),
        Subsignal("data0_n",     Pins("25"), IOStandard("TMDS_33")),
        Subsignal("data1_p",     Pins("4"), IOStandard("TMDS_33")),
        Subsignal("data1_n",     Pins("3"), IOStandard("TMDS_33")),
        Subsignal("data2_p",     Pins("48"), IOStandard("TMDS_33")),
        Subsignal("data2_n",     Pins("45"), IOStandard("TMDS_33")),
    ),
]

# Connectors ---------------------------------------------------------------------------------------

_connectors = [
    ("touch_pins", "43 42 9 19"),
    ("gpio", "43 42 9"),
]

# Platform -----------------------------------------------------------------------------------------

class Platform(LatticePlatform):
    default_clk_name   = "clk48"
    default_clk_period = 1e9/48e6

    def __init__(self):
        LatticePlatform.__init__(self, "ice40-up5k-sg48", _io, _connectors, toolchain="icestorm")

    def create_programmer(self):
        return IceStormProgrammer()

    def do_finalize(self, fragment):
        LatticePlatform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk48", loose=True), 1e9/48e6)

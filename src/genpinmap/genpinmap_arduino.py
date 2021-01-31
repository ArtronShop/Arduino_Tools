import argparse
import datetime
import json
import re
import subprocess
import sys
import textwrap
from argparse import RawTextHelpFormatter
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from xml.dom.minidom import parse, Node

mcu_list = []  # 'name'
io_list = []  # 'PIN','name'
alt_list = []  # 'PIN','name'
dualpad_list = []  # 'PIN','name'
remap_list = []  # 'PIN','name'
adclist = []  # 'PIN','name','ADCSignal'
daclist = []  # 'PIN','name','DACSignal'
i2cscl_list = []  # 'PIN','name','I2CSCLSignal'
i2csda_list = []  # 'PIN','name','I2CSDASignal'
tim_list = []  # 'PIN','name','TIMSignal'
uarttx_list = []  # 'PIN','name','UARTtx'
uartrx_list = []  # 'PIN','name','UARTrx'
uartcts_list = []  # 'PIN','name','UARTcts'
uartrts_list = []  # 'PIN','name','UARTrts'
spimosi_list = []  # 'PIN','name','SPIMOSI'
spimiso_list = []  # 'PIN','name','SPIMISO'
spissel_list = []  # 'PIN','name','SPISSEL'
spisclk_list = []  # 'PIN','name','SPISCLK'
cantd_list = []  # 'PIN','name','CANTD'
canrd_list = []  # 'PIN','name','CANRD'
eth_list = []  # 'PIN','name','ETH'
quadspidata0_list = []  # 'PIN','name','QUADSPIDATA0'
quadspidata1_list = []  # 'PIN','name','QUADSPIDATA1'
quadspidata2_list = []  # 'PIN','name','QUADSPIDATA2'
quadspidata3_list = []  # 'PIN','name','QUADSPIDATA3'
quadspisclk_list = []  # 'PIN','name','QUADSPISCLK'
quadspissel_list = []  # 'PIN','name','QUADSPISSEL'
syswkup_list = []  # 'PIN','name','SYSWKUP'
usb_list = []  # 'PIN','name','USB'
usb_otgfs_list = []  # 'PIN','name','USB'
usb_otghs_list = []  # 'PIN','name','USB'
sd_list = []  # 'PIN','name','SD'

# format
# Peripheral
start_elem_fmt = "  {{{:{width}}"
end_array_fmt = """  {{NC,{0:{w1}}NP,{0:{w2}}0}}
}};
#endif
"""


# GPIO file parsing
def find_gpio_file():
    res = "ERROR"
    itemlist = xml_mcu.getElementsByTagName("IP")
    for s in itemlist:
        if "GPIO" in s.attributes["Name"].value:
            res = s.attributes["Version"].value
            break
    return res


def get_gpio_af_num(pintofind, iptofind):
    if "STM32F10" in mcu_file.stem:
        return get_gpio_af_numF1(pintofind, iptofind)
    # DBG print ('pin to find ' + pintofind)
    i = 0
    mygpioaf = ""
    for n in xml_gpio.documentElement.childNodes:
        i += 1
        j = 0
        if n.nodeType != Node.ELEMENT_NODE:
            continue
        for firstlevel in n.attributes.items():
            # if 'PB7' in firstlevel:
            if pintofind != firstlevel[1]:
                continue
            # DBG print (i , firstlevel)
            # n = pin node found
            for m in n.childNodes:
                j += 1
                k = 0
                if m.nodeType != Node.ELEMENT_NODE:
                    continue
                for secondlevel in m.attributes.items():
                    k += 1
                    # if 'I2C1_SDA' in secondlevel:
                    if iptofind not in secondlevel:
                        continue
                    # DBG print (i, j,  m.attributes.items())
                    # m = IP node found
                    for p in m.childNodes:
                        if p.nodeType != Node.ELEMENT_NODE:
                            continue
                        # p node of 'Specific parameter'
                        # DBG print (i,j,k,p.attributes.items())
                        for myc in p.childNodes:
                            # DBG print (myc)
                            if myc.nodeType != Node.ELEMENT_NODE:
                                continue
                            # myc = node of ALTERNATE
                            for mygpioaflist in myc.childNodes:
                                if mygpioaflist.data not in mygpioaf:
                                    if mygpioaf != "":
                                        mygpioaf += " "
                                    mygpioaf += mygpioaflist.data
                                # print (mygpioaf)
    if mygpioaf == "":
        mygpioaf = "GPIO_AF_NONE"
    return mygpioaf


def get_gpio_af_numF1(pintofind, iptofind):
    # print ('pin to find ' + pintofind + ' ip to find ' + iptofind)
    i = 0
    mygpioaf = ""
    for n in xml_gpio.documentElement.childNodes:
        i += 1
        j = 0
        if n.nodeType != Node.ELEMENT_NODE:
            continue
        for firstlevel in n.attributes.items():
            # print ('firstlevel ' , firstlevel)
            #                if 'PB7' in firstlevel:
            if pintofind != firstlevel[1]:
                continue
            # print ('firstlevel ' , i , firstlevel)
            # n = pin node found
            for m in n.childNodes:
                j += 1
                k = 0
                if m.nodeType != Node.ELEMENT_NODE:
                    continue
                for secondlevel in m.attributes.items():
                    # print ('secondlevel ' , i, j, k , secondlevel)
                    k += 1
                    # if 'I2C1_SDA' in secondlevel:
                    if iptofind not in secondlevel:
                        continue
                    # m = IP node found
                    # print (i, j,  m.attributes.items())
                    for p in m.childNodes:
                        # p node 'RemapBlock'
                        if (
                            p.nodeType == Node.ELEMENT_NODE
                            and p.hasChildNodes() is False
                        ):
                            if mygpioaf != "":
                                mygpioaf += " "
                            mygpioaf += "AFIO_NONE"
                        else:
                            for s in p.childNodes:
                                if s.nodeType != Node.ELEMENT_NODE:
                                    continue
                                # s node 'Specific parameter'
                                # print (i,j,k,p.attributes.items())
                                for myc in s.childNodes:
                                    # DBG print (myc)
                                    if myc.nodeType != Node.ELEMENT_NODE:
                                        continue
                                    # myc = AF value
                                    for mygpioaflist in myc.childNodes:
                                        if mygpioaf != "":
                                            mygpioaf += " "
                                        mygpioaf += mygpioaflist.data.replace(
                                            "__HAL_", ""
                                        ).replace("_REMAP", "")
                                        # print mygpioaf
    if mygpioaf == "":
        mygpioaf = "AFIO_NONE"
    return mygpioaf


# Storage
# Store pin I/O
def store_pin(pin, name, dest_list):
    if pin in [p[0] for p in dest_list]:
        return
    p = [pin, name]
    if p not in dest_list:
        dest_list.append(p)


# Store ADC list
def store_adc(pin, name, signal):
    if "IN" in signal:
        adclist.append([pin, name, signal])


# Store DAC list
def store_dac(pin, name, signal):
    daclist.append([pin, name, signal])


# Store I2C list
def store_i2c(pin, name, signal):
    # is it SDA or SCL ?
    if "_SCL" in signal:
        i2cscl_list.append([pin, name, signal])
    if "_SDA" in signal:
        i2csda_list.append([pin, name, signal])


# Store timers
def store_tim(pin, name, signal):
    if "_CH" in signal:
        tim_list.append([pin, name, signal])


# Store Uart pins
def store_uart(pin, name, signal):
    if "_TX" in signal:
        uarttx_list.append([pin, name, signal])
    if "_RX" in signal:
        uartrx_list.append([pin, name, signal])
    if "_CTS" in signal:
        uartcts_list.append([pin, name, signal])
    if "_RTS" in signal:
        uartrts_list.append([pin, name, signal])


# Store SPI pins
def store_spi(pin, name, signal):
    if "_MISO" in signal:
        spimiso_list.append([pin, name, signal])
    if "_MOSI" in signal:
        spimosi_list.append([pin, name, signal])
    if "_SCK" in signal:
        spisclk_list.append([pin, name, signal])
    if "_NSS" in signal:
        spissel_list.append([pin, name, signal])


# Store CAN pins
def store_can(pin, name, signal):
    if "_RX" in signal:
        canrd_list.append([pin, name, signal])
    if "_TX" in signal:
        cantd_list.append([pin, name, signal])


# Store ETH list
def store_eth(pin, name, signal):
    eth_list.append([pin, name, signal])


# Store QSPI pins
def store_qspi(pin, name, signal):
    if "_IO0" in signal:
        quadspidata0_list.append([pin, name, signal])
    if "_IO1" in signal:
        quadspidata1_list.append([pin, name, signal])
    if "_IO2" in signal:
        quadspidata2_list.append([pin, name, signal])
    if "_IO3" in signal:
        quadspidata3_list.append([pin, name, signal])
    if "_CLK" in signal:
        quadspisclk_list.append([pin, name, signal])
    if "_NCS" in signal:
        quadspissel_list.append([pin, name, signal])


# Store SYS pins
def store_sys(pin, name, signal):
    if "_WKUP" in signal:
        signal = signal.replace("PWR", "SYS")
        syswkup_list.append([pin, name, signal])


# Store USB pins
def store_usb(pin, name, signal):
    if "OTG" not in signal:
        usb_list.append([pin, name, signal])
    if signal.startswith("USB_OTG_FS"):
        usb_otgfs_list.append([pin, name, signal])
    if signal.startswith("USB_OTG_HS"):
        usb_otghs_list.append([pin, name, signal])


# Store SD pins
def store_sd(pin, name, signal):
    sd_list.append([pin, name, signal])


# PeripheralPins.cpp generation
def adc_pinmap():
    adc_pins_list = []
    winst = []
    wpin = []
    # For STM32L47xxx/48xxx, it is necessary to configure
    # the GPIOx_ASCR register
    if re.match("STM32L4[78]+", mcu_file.stem):
        mode = "STM_MODE_ANALOG_ADC_CONTROL"
    else:
        mode = "STM_MODE_ANALOG"
    for p in adclist:
        # inst
        a = p[2].split("_")
        inst = a[0]
        if not inst[-1].isdigit():
            inst += "1"  # single ADC for this product
        winst.append(len(inst))
        wpin.append(len(p[0]))
        # chan
        chan = re.sub("IN[N|P]?", "", a[1])
        adc_pins_list.append(
            {
                "pin": p[0],
                "inst": inst,
                "mode": mode,
                "pull": "GPIO_NOPULL",
                "af": "0",
                "chan": chan,
                "inv": "0",
                "cmt": p[2],
            }
        )
    return dict(
        name="ADC",
        hal="ADC",
        aname="ADC",
        data="ext",
        wpin=max(wpin) + 1,
        winst=max(winst) + 1,
        list=adc_pins_list,
    )


def dac_pinmap():
    dac_pins_list = []
    winst = [0]
    wpin = [0]
    mode = "STM_MODE_ANALOG"
    for p in daclist:
        # 2nd element is the DAC signal
        if p[2][3] == "_":  # 1 DAC in this chip
            inst = "1"
            chan = p[2][7]
        else:
            inst = p[2][3]
            chan = p[2][8]
        winst.append(len(inst))
        wpin.append(len(p[0]))
        dac_pins_list.append(
            {
                "pin": p[0],
                "inst": "DAC" + inst,
                "mode": mode,
                "pull": "GPIO_NOPULL",
                "af": "0",
                "chan": chan,
                "inv": "0",
                "cmt": p[2],
            }
        )
    return dict(
        name="DAC",
        hal="DAC",
        aname="DAC",
        data="ext",
        wpin=max(wpin) + 1,
        winst=max(winst) + 4,
        list=dac_pins_list,
    )


def i2c_pinmap(lst):
    i2c_pins_list = []
    winst = []
    wpin = []
    mode = "STM_MODE_AF_OD"
    if lst == i2csda_list:
        aname = "I2C_SDA"
    else:
        aname = "I2C_SCL"
    for p in lst:
        result = get_gpio_af_num(p[1], p[2])
        # 2nd element is the I2C XXX signal
        b = p[2].split("_")[0]
        inst = b[: len(b) - 1] + b[len(b) - 1]
        winst.append(len(inst))
        wpin.append(len(p[0]))
        r = result.split(" ")
        for af in r:
            i2c_pins_list.append(
                {
                    "pin": p[0],
                    "inst": inst,
                    "mode": mode,
                    "pull": "GPIO_NOPULL",
                    "af": af,
                }
            )
    return dict(
        name="I2C",
        hal="I2C",
        aname=aname,
        data="",
        wpin=max(wpin) + 1,
        winst=max(winst) + 1,
        list=i2c_pins_list,
    )


def tim_pinmap():
    tim_pins_list = []
    winst = []
    wpin = []
    mode = "STM_MODE_AF_PP"
    for p in tim_list:
        result = get_gpio_af_num(p[1], p[2])
        # 2nd element is the TIM signal
        a = p[2].split("_")
        inst = a[0]
        if not inst[-1].isdigit():
            inst += "1"
        winst.append(len(inst))
        wpin.append(len(p[0]))
        chan = a[1].replace("CH", "")
        if chan.endswith("N"):
            inv = "1"
            chan = chan.strip("N")
        else:
            inv = "0"
        r = result.split(" ")
        for af in r:
            tim_pins_list.append(
                {
                    "pin": p[0],
                    "inst": inst,
                    "mode": mode,
                    "pull": "GPIO_PULLUP",
                    "af": af,
                    "chan": chan,
                    "inv": inv,
                    "cmt": p[2],
                }
            )
    return dict(
        name="TIM",
        hal="TIM",
        aname="TIM",
        data="ext",
        wpin=max(wpin) + 1,
        winst=max(winst) + 1,
        list=tim_pins_list,
    )


def uart_pinmap(lst):
    uart_pins_list = []
    winst = []
    wpin = []
    mode = "STM_MODE_AF_PP"
    if lst == uarttx_list:
        aname = "UART_TX"
    elif lst == uartrx_list:
        aname = "UART_RX"
    elif lst == uartrts_list:
        aname = "UART_RTS"
    else:
        aname = "UART_CTS"
    for p in lst:
        result = get_gpio_af_num(p[1], p[2])
        # 2nd element is the UART_XX signal
        inst = p[2].split("_")[0]
        winst.append(len(inst))
        wpin.append(len(p[0]))
        if "STM32F10" in mcu_file.stem and lst == uartrx_list:
            mode = "STM_MODE_INPUT"
        else:
            mode = "STM_MODE_AF_PP"
        r = result.split(" ")
        for af in r:
            uart_pins_list.append(
                {
                    "pin": p[0],
                    "inst": inst,
                    "mode": mode,
                    "pull": "GPIO_PULLUP",
                    "af": af,
                }
            )
    return dict(
        name="UART",
        hal="UART",
        aname=aname,
        data="",
        wpin=max(wpin) + 1,
        winst=max(winst) + 1,
        list=uart_pins_list,
    )


def spi_pinmap(lst):
    spi_pins_list = []
    winst = []
    wpin = []
    if lst == spimosi_list:
        aname = "SPI_MOSI"
    elif lst == spimiso_list:
        aname = "SPI_MISO"
    elif lst == spisclk_list:
        aname = "SPI_SCLK"
    else:
        aname = "SPI_SSEL"
    for p in lst:
        result = get_gpio_af_num(p[1], p[2])
        # 2nd element is the SPI_XXXX signal
        inst = p[2].split("_")[0]
        winst.append(len(inst))
        wpin.append(len(p[0]))
        r = result.split(" ")
        for af in r:
            spi_pins_list.append(
                {
                    "pin": p[0],
                    "inst": inst,
                    "mode": "STM_MODE_AF_PP",
                    "pull": "GPIO_PULLUP",
                    "af": af,
                }
            )
    return dict(
        name="SPI",
        hal="SPI",
        aname=aname,
        data="",
        wpin=max(wpin) + 1,
        winst=max(winst) + 1,
        list=spi_pins_list,
    )


def can_pinmap(lst):
    can_pins_list = []
    winst = [0]
    wpin = [0]
    if canrd_list and "FDCAN" in canrd_list[0][2]:
        name = "FDCAN"
    else:
        name = "CAN"
    if lst == canrd_list:
        aname = "CAN_RD"
    else:
        aname = "CAN_TD"
    for p in lst:
        result = get_gpio_af_num(p[1], p[2])
        # 2nd element is the (FD)CAN_XX signal
        inst = p[2].split("_")[0]
        if not inst[-1].isdigit():
            inst += "1"
        winst.append(len(inst))
        wpin.append(len(p[0]))
        if "STM32F10" in mcu_file.stem and lst == canrd_list:
            mode = "STM_MODE_INPUT"
        else:
            mode = "STM_MODE_AF_PP"
        r = result.split(" ")
        for af in r:
            can_pins_list.append(
                {
                    "pin": p[0],
                    "inst": inst,
                    "mode": mode,
                    "pull": "GPIO_NOPULL",
                    "af": af,
                }
            )
    return dict(
        name=name,
        hal=name,
        aname=aname,
        data="",
        wpin=max(wpin) + 1,
        winst=max(winst) + 1,
        list=can_pins_list,
    )


def eth_pinmap():
    eth_pins_list = []
    wpin = [0]
    inst = "ETH"
    for p in eth_list:
        # Note: Some pins are duplicated with only a different signal
        # Now considered as an ALTX pins even ifsame AF
        af = get_gpio_af_num(p[1], p[2])
        wpin.append(len(p[0]))
        eth_pins_list.append(
            {
                "pin": p[0],
                "inst": inst,
                "mode": "STM_MODE_AF_PP",
                "pull": "GPIO_PULLUP",
                "af": af,
                "cmt": p[2],
            }
        )
    return dict(
        name="ETHERNET",
        hal="ETH",
        aname="Ethernet",
        data="",
        wpin=max(wpin) + 1,
        winst=4,
        list=eth_pins_list,
    )


def qspi_pinmap(lst):
    qspi_pins_list = []
    winst = [0]
    wpin = [0]
    name = "QUADSPI"
    hal = "QSPI"
    ospi_regex = r"OCTOSPI(?:M_P)?(\d).*"

    if quadspidata0_list and "OCTOSPI" in quadspidata0_list[0][2]:
        name = "OCTOSPI"
        hal = "OSPI"
    if lst == quadspidata0_list:
        aname = name + "_DATA0"
    elif lst == quadspidata1_list:
        aname = name + "_DATA1"
    elif lst == quadspidata2_list:
        aname = name + "_DATA2"
    elif lst == quadspidata3_list:
        aname = name + "_DATA3"
    elif lst == quadspisclk_list:
        aname = name + "_SCLK"
    else:
        aname = name + "_SSEL"
    for p in lst:
        af = get_gpio_af_num(p[1], p[2])
        # 2nd element is the XXXXSPI_YYYY signal
        instm = re.match(ospi_regex, p[2])
        if instm:
            if "1" in instm.group(1):
                inst = "OCTOSPI1"
            elif "2" in instm.group(1):
                inst = "OCTOSPI2"
        else:
            inst = "QUADSPI"
        winst.append(len(inst))
        wpin.append(len(p[0]))
        qspi_pins_list.append(
            {
                "pin": p[0],
                "inst": inst,
                "mode": "STM_MODE_AF_PP",
                "pull": "GPIO_PULLUP",
                "af": af,
                "cmt": p[2],
            }
        )
    return dict(
        name=name,
        hal=hal,
        aname=aname,
        data="",
        wpin=max(wpin) + 1,
        winst=max(winst) + 1,
        list=qspi_pins_list,
    )


def usb_pinmap(lst):
    usb_pins_list = []
    wpin = [0]
    use_hs_in_fs = False
    nb_loop = 1

    if lst == usb_otgfs_list:
        inst = "USB_OTG_FS"
    elif lst == usb_otghs_list:
        inst = "USB_OTG_HS"
        nb_loop = 2
    else:
        inst = "USB"
    for nb in range(nb_loop):
        for p in lst:
            hsinfs = 0
            result = get_gpio_af_num(p[1], p[2])
            if lst == usb_otghs_list:
                hsinfs = 3
                if nb == 0:
                    if "ULPI" in p[2]:
                        continue
                    elif not use_hs_in_fs:
                        hsinfs = 1
                        use_hs_in_fs = True
                else:
                    if "ULPI" not in p[2]:
                        continue
                    elif use_hs_in_fs:
                        hsinfs = 2
                        use_hs_in_fs = False

            # 2nd element is the USB_XXXX signal
            if not p[2].startswith("USB_D") and "VBUS" not in p[2]:
                if "ID" not in p[2]:
                    mode = "STM_MODE_AF_PP"
                    pull = "GPIO_PULLUP"
                else:
                    # ID pin: AF_PP + PULLUP
                    mode = "STM_MODE_AF_OD"
                    pull = "GPIO_PULLUP"
            else:
                # USB_DM/DP and VBUS: INPUT + NOPULL
                mode = "STM_MODE_INPUT"
                pull = "GPIO_NOPULL"
            wpin.append(len(p[0]))
            r = result.split(" ")
            for af in r:
                usb_pins_list.append(
                    {
                        "hsinfs": hsinfs,
                        "pin": p[0],
                        "inst": inst,
                        "mode": mode,
                        "pull": pull,
                        "af": af,
                        "cmt": p[2],
                    }
                )
    return dict(
        name="USB",
        hal=["PCD", "HCD"],
        aname=inst,
        data="",
        wpin=max(wpin) + 1,
        winst=len(inst) + 1,
        list=usb_pins_list,
    )


def sd_pinmap():
    sd_pins_list = []
    winst = [0]
    wpin = [0]
    mode = "STM_MODE_AF_PP"

    for p in sd_list:
        af = get_gpio_af_num(p[1], p[2])
        # 2nd element is the SD signal
        a = p[2].split("_")
        inst = a[0]
        if a[1].startswith("C") or a[1].endswith("DIR"):
            pull = "GPIO_NOPULL"
        else:
            pull = "GPIO_PULLUP"
        winst.append(len(inst))
        wpin.append(len(p[0]))
        sd_pins_list.append(
            {
                "pin": p[0],
                "inst": inst,
                "mode": mode,
                "pull": pull,
                "af": af,
                "cmt": p[2],
            }
        )
    return dict(
        name="SD",
        hal="SD",
        aname="SD",
        data="",
        wpin=max(wpin) + 1,
        winst=max(winst) + 1,
        list=sd_pins_list,
    )


def print_peripheral():
    # Print specific PinNames in header file
    periph_c_template = j2_env.get_template(
        periph_c_filename,
    )

    if usb_list:
        usb_pinmmap = [usb_pinmap(usb_list)]
    elif usb_otgfs_list:
        usb_pinmmap = (usb_pinmap(usb_otgfs_list), usb_pinmap(usb_otghs_list))
    else:
        usb_pinmmap = [usb_pinmap(usb_otghs_list)]

    periph_c_file.write(
        periph_c_template.render(
            year=datetime.datetime.now().year,
            mcu_file=mcu_file.name,
            db_release=db_release,
            peripherals_list=(
                [adc_pinmap()],
                [dac_pinmap()],
                (i2c_pinmap(i2csda_list), i2c_pinmap(i2cscl_list)),
                [tim_pinmap()],
                (
                    uart_pinmap(uarttx_list),
                    uart_pinmap(uartrx_list),
                    uart_pinmap(uartrts_list),
                    uart_pinmap(uartcts_list),
                ),
                (
                    spi_pinmap(spimosi_list),
                    spi_pinmap(spimiso_list),
                    spi_pinmap(spisclk_list),
                    spi_pinmap(spissel_list),
                ),
                (can_pinmap(canrd_list), can_pinmap(cantd_list)),
                [eth_pinmap()],
                (
                    qspi_pinmap(quadspidata0_list),
                    qspi_pinmap(quadspidata1_list),
                    qspi_pinmap(quadspidata2_list),
                    qspi_pinmap(quadspidata3_list),
                    qspi_pinmap(quadspisclk_list),
                    qspi_pinmap(quadspissel_list),
                ),
                usb_pinmmap,
                [sd_pinmap()],
            ),
        )
    )


# PinNamesVar.h generation
def manage_syswkup():
    syswkup_pins_list = []
    if len(syswkup_list) != 0:
        # H7xx and F446 start from 0, inc by 1
        inc = 0
        if syswkup_list[0][2].replace("SYS_WKUP", "") == "0":
            inc = 1
        # Fill list with missing SYS_WKUPx set to NC
        i = 0
        while i < 8:
            num = 0
            if len(syswkup_list) > i:
                n = syswkup_list[i][2].replace("SYS_WKUP", "")
                if len(n) != 0:
                    num = int(n) if inc == 1 else int(n) - 1
            x = i if inc == 1 else i + 1
            if num != i:
                syswkup_list.insert(i, ["NC", "NC_" + str(x), "SYS_WKUP" + str(x)])
            i += 1
        for p in syswkup_list:
            num = p[2].replace("SYS_WKUP", "")
            if (inc == 1) and (p[0] != "NC"):
                cmt = " /* " + p[2] + " */"
            else:
                cmt = ""
            syswkup_pins_list.append([p[0], cmt])

    return syswkup_pins_list


def print_pinamevar():
    # Print specific PinNames in header file
    pinvar_h_template = j2_env.get_template(pinvar_h_filename)

    dualpad_pins_list = []
    for p in dualpad_list:
        dualpad_pins_list.append({"name": p[0], "base": p[0].split("_C")[0]})

    remap_pins_list = []
    for p in remap_list:
        remap_pins_list.append({"name": p[0], "base": p[0].split("_R")[0]})

    alt_pins_list = []
    waltpin = [0]
    for p in alt_list:
        if "_ALT" in p[0]:
            waltpin.append(len(p[0]))
            alt_pins_list.append(
                {"name": p[0], "base": p[0].split("_A")[0], "num": p[0].split("_")[-1]}
            )

    syswkup_pins_list = manage_syswkup()

    usb_pins_list = []
    wusbpin = [0]
    if usb_list or usb_otgfs_list or usb_otghs_list:
        for p in usb_list + usb_otgfs_list + usb_otghs_list:
            wusbpin.append(len(p[2]))
            usb_pins_list.append({"name": p[2], "pn": p[0]})
    sorted_usb_pins_list = sorted(usb_pins_list, key=lambda i: i["name"])

    pinvar_h_file.write(
        pinvar_h_template.render(
            dualpad_pins_list=dualpad_pins_list,
            remap_pins_list=remap_pins_list,
            waltpin=max(waltpin),
            alt_pins_list=alt_pins_list,
            syswkup_pins_list=syswkup_pins_list,
            wusbpin=max(wusbpin),
            usb_pins_list=sorted_usb_pins_list,
        )
    )


# Variant files generation
def spi_pins_variant():
    ss_pin = ss1_pin = ss2_pin = ss3_pin = mosi_pin = miso_pin = sck_pin = "PYn"

    # Iterate to find match instance if any
    for mosi in spimosi_list:
        mosi_inst = mosi[2].split("_", 1)[0]
        for miso in spimiso_list:
            miso_inst = miso[2].split("_", 1)[0]
            if mosi_inst == miso_inst:
                for sck in spisclk_list:
                    sck_inst = sck[2].split("_", 1)[0]
                    if mosi_inst == sck_inst:
                        miso_pin = miso[0].replace("_", "", 1)
                        mosi_pin = mosi[0].replace("_", "", 1)
                        sck_pin = sck[0].replace("_", "", 1)
                        break
                else:
                    continue
                break
        else:
            continue

        # Try to find hw ssel
        for ss in spissel_list:
            ss_inst = ss[2].split("_", 1)[0]
            if mosi_inst == ss_inst:
                if "PYn" == ss_pin:
                    ss_pin = ss[0].replace("_", "", 1)
                elif "PYn" == ss1_pin:
                    ss1_pin = ss[0].replace("_", "", 1)
                elif "PYn" == ss2_pin:
                    ss2_pin = ss[0].replace("_", "", 1)
                elif "PYn" == ss3_pin:
                    ss3_pin = ss[0].replace("_", "", 1)
                    break
        break
    else:
        print("No SPI found!")
    return dict(
        ss=ss_pin,
        ss1=ss1_pin,
        ss2=ss2_pin,
        ss3=ss3_pin,
        mosi=mosi_pin,
        miso=miso_pin,
        sck=sck_pin,
    )


def i2c_pins_variant():
    sda_pin = scl_pin = "PYn"
    # Iterate to find match instance if any
    for sda in i2csda_list:
        sda_inst = sda[2].split("_", 1)[0]
        for scl in i2cscl_list:
            scl_inst = scl[2].split("_", 1)[0]
            if sda_inst == scl_inst:
                sda_pin = sda[0].replace("_", "", 1)
                scl_pin = scl[0].replace("_", "", 1)
                break
        else:
            continue
        break
    else:
        print("No I2C found!")
    return dict(sda=sda_pin, scl=scl_pin)


def serial_pins_variant():
    # Manage (LP)U(S)ART pins
    if uarttx_list:
        # Default if no rx pin
        serialtx_pin = uarttx_list[0][0].replace("_", "")
        serial_inst = uarttx_list[0][2].split("_", 1)[0]
        # Half duplex
        serialrx_pin = serialtx_pin
        if uartrx_list:
            # Iterate to find match instance if any
            for uarttx in uarttx_list:
                serialtx_inst = uarttx[2].split("_", 1)[0]
                for uartrx in uartrx_list:
                    serialrx_inst = uartrx[2].split("_", 1)[0]
                    if serialtx_inst == serialrx_inst:
                        serialtx_pin = uarttx[0].replace("_", "", 1)
                        serialrx_pin = uartrx[0].replace("_", "", 1)
                        serial_inst = serialtx_inst
                        break
                else:
                    continue
                break
        end_num_regex = r".*(\d+)$"
        serialnum = re.match(end_num_regex, serial_inst)
        if serialnum:
            serialnum = serialnum.group(1)
            if serial_inst.startswith("LP"):
                serialnum = "10" + serialnum
        else:
            print("No serial instance number found!")
            serialnum = "-1"
    else:
        serialtx_pin = serialtx_pin = "PYn"
        serialnum = "-1"
        print("No serial found!")
    return dict(instance=serialnum, rx=serialrx_pin, tx=serialtx_pin)


def timer_variant():
    # Choice is based on the fact Tone and Servo do not need output nor compare
    # capabilities, and thus select timer instance which have the less outputs/compare
    # capabilities:
    # - TIM6/TIM7/TIM18 because they have no output and no compare capabilities
    # - TIM10/TIM11/TIM13/TIM14 only 1 compare channel no complementary
    # - TIM16/TIM17 generally only 1 compare channel (with complementary)
    # - TIM9/TIM12/TIM21/TIM22 2 compare channels (no complementary)
    # - TIM15  generally 2 compare channel (with potentially complementary)
    # - TIM3/TIM4/TIM19 up to 4 channels
    # - TIM2/TIM5 (most of the time) the only 32bit timer. Could be reserved
    # for further 32bit support
    # - TIM1/TIM8/TIM20 they are the most advanced/complete timers

    tim_inst_order = [
        "TIM6",
        "TIM7",
        "TIM18",
        "TIM10",
        "TIM11",
        "TIM13",
        "TIM14",
        "TIM16",
        "TIM17",
        "TIM9",
        "TIM12",
        "TIM21",
        "TIM22",
        "TIM15",
        "TIM3",
        "TIM4",
        "TIM19",
        "TIM2",
        "TIM5",
        "TIM1",
        "TIM8",
        "TIM20",
    ]
    tim_inst_list = []
    tim_regex = r"^(TIM\d+)$"
    tone = servo = "TIMx"
    itemlist = xml_mcu.getElementsByTagName("IP")
    # Collect all TIMx instance
    for s in itemlist:
        inst = re.match(tim_regex, s.attributes["InstanceName"].value)
        if inst:
            tim_inst_list.append(inst.group(1))
    if tim_inst_list:
        for pref in tim_inst_order:
            if pref in tim_inst_list:
                if tone == "TIMx":
                    tone = pref
                elif servo == "TIMx":
                    servo = pref
                    break
        else:
            print("Not all TIM instance found!")
    return dict(tone=tone, servo=servo)


def print_variant():
    variant_h_template = j2_env.get_template(variant_h_filename)
    variant_cpp_template = j2_env.get_template(variant_cpp_filename)

    # Default pins definition
    num_digital_pins = len(io_list) + len(dualpad_list) + len(remap_list)
    num_dualpad_pins = len(dualpad_list)
    num_remap_pins = len(remap_list)

    # SPI definition
    spi_pins = spi_pins_variant()

    # I2C definition
    i2c_pins = i2c_pins_variant()

    # Serial definition
    serial = serial_pins_variant()

    # Timers definition
    timer = timer_variant()

    # Manage all pins number, PinName and analog pins
    analog_index = 0
    pins_number_list = []
    analog_pins_list = []
    pinnames_list = []
    idx_sum = len(io_list)
    for idx, io in enumerate(io_list):
        pyn = io[0].replace("_", "", 1)
        if [item for item in adclist if item[0] == io[0]]:
            ax = "A{}".format(analog_index)
            pins_number_list.append({"name": pyn, "val": ax})
            analog_pins_list.append({"val": idx, "ax": ax, "pyn": pyn})
            analog_index += 1
        else:
            pins_number_list.append({"name": pyn, "val": idx})
        pinnames_list.append(io[0])

    for idx, io in enumerate(dualpad_list):
        pyn = io[0].replace("_", "", 1)
        if [item for item in adclist if item[0] == io[0]]:
            ax = "A{}".format(analog_index)
            pins_number_list.append({"name": pyn, "val": ax})
            analog_pins_list.append({"val": idx + idx_sum, "ax": ax, "pyn": pyn})
            analog_index += 1
        else:
            pins_number_list.append({"name": pyn, "val": idx + idx_sum})
        pinnames_list.append(io[0])
    idx_sum += len(dualpad_list)
    for idx, io in enumerate(remap_list):
        pyn = io[0].replace("_", "", 1)
        if [item for item in adclist if item[0] == io[0]]:
            ax = "A{}".format(analog_index)
            pins_number_list.append({"name": pyn, "val": ax})
            analog_pins_list.append({"val": idx + idx_sum, "ax": ax, "pyn": pyn})
            analog_index += 1
        else:
            pins_number_list.append({"name": pyn, "val": idx + idx_sum})
        pinnames_list.append(io[0])
    alt_pins_list = []
    waltpin = [0]
    for p in alt_list:
        if "_ALT" in p[0]:
            pyn = p[0].replace("_", "", 1)
            waltpin.append(len(pyn))
            alt_pins_list.append(
                {"name": pyn, "base": pyn.split("_A")[0], "num": pyn.split("_")[-1]}
            )

    # Define extra HAL modules
    hal_modules_list = []
    if daclist:
        hal_modules_list.append("HAL_DAC_MODULE_ENABLED")
    if eth_list:
        hal_modules_list.append("HAL_ETH_MODULE_ENABLED")
    if quadspidata0_list:
        if "OCTOSPI" in quadspidata0_list[0][2]:
            hal_modules_list.append("HAL_OSPI_MODULE_ENABLED")
        else:
            hal_modules_list.append("HAL_QSPI_MODULE_ENABLED")
    if sd_list:
        hal_modules_list.append("HAL_SD_MODULE_ENABLED")

    mcu_serie = re.match(r"STM32([FGHLW][\dBL]|MP[\d])", mcu_file.stem)
    if not mcu_serie:
        print("No serie match found!")
        exit(1)
    mcu_serie = mcu_serie.group(1).lower()

    variant_h_file.write(
        variant_h_template.render(
            year=datetime.datetime.now().year,
            pins_number_list=pins_number_list,
            alt_pins_list=alt_pins_list,
            waltpin=max(waltpin),
            num_digital_pins=num_digital_pins,
            num_dualpad_pins=num_dualpad_pins,
            num_remap_pins=num_remap_pins,
            num_analog_inputs=len(analog_pins_list),
            spi_pins=spi_pins,
            i2c_pins=i2c_pins,
            timer=timer,
            serial=serial,
            hal_modules_list=hal_modules_list,
        )
    )

    variant_cpp_file.write(
        variant_cpp_template.render(
            year=datetime.datetime.now().year,
            pinnames_list=pinnames_list,
            analog_pins_list=analog_pins_list,
            mcu_serie=mcu_serie,
        )
    )


# List management
tokenize = re.compile(r"(\d+)|(\D+)").findall


def natural_sortkey(list_2_elem):
    return tuple(int(num) if num else alpha for num, alpha in tokenize(list_2_elem[0]))


def natural_sortkey2(list_2_elem):
    return tuple(int(num) if num else alpha for num, alpha in tokenize(list_2_elem[2]))


def sort_my_lists():
    io_list.sort(key=natural_sortkey)
    dualpad_list.sort(key=natural_sortkey)
    remap_list.sort(key=natural_sortkey)
    adclist.sort(key=natural_sortkey)
    daclist.sort(key=natural_sortkey)
    i2cscl_list.sort(key=natural_sortkey)
    i2csda_list.sort(key=natural_sortkey)
    tim_list.sort(key=natural_sortkey2)
    tim_list.sort(key=natural_sortkey)
    uarttx_list.sort(key=natural_sortkey)
    uartrx_list.sort(key=natural_sortkey)
    uartcts_list.sort(key=natural_sortkey)
    uartrts_list.sort(key=natural_sortkey)
    spimosi_list.sort(key=natural_sortkey)
    spimiso_list.sort(key=natural_sortkey)
    spissel_list.sort(key=natural_sortkey)
    spisclk_list.sort(key=natural_sortkey)
    cantd_list.sort(key=natural_sortkey)
    canrd_list.sort(key=natural_sortkey)
    eth_list.sort(key=natural_sortkey)
    quadspidata0_list.sort(key=natural_sortkey)
    quadspidata1_list.sort(key=natural_sortkey)
    quadspidata2_list.sort(key=natural_sortkey)
    quadspidata3_list.sort(key=natural_sortkey)
    quadspisclk_list.sort(key=natural_sortkey)
    quadspissel_list.sort(key=natural_sortkey)
    syswkup_list.sort(key=natural_sortkey2)
    usb_list.sort(key=natural_sortkey)
    usb_otgfs_list.sort(key=natural_sortkey)
    usb_otghs_list.sort(key=natural_sortkey)
    sd_list.sort(key=natural_sortkey)


def clean_all_lists():
    del io_list[:]
    del alt_list[:]
    del dualpad_list[:]
    del remap_list[:]
    del adclist[:]
    del daclist[:]
    del i2cscl_list[:]
    del i2csda_list[:]
    del tim_list[:]
    del uarttx_list[:]
    del uartrx_list[:]
    del uartcts_list[:]
    del uartrts_list[:]
    del spimosi_list[:]
    del spimiso_list[:]
    del spissel_list[:]
    del spisclk_list[:]
    del cantd_list[:]
    del canrd_list[:]
    del eth_list[:]
    del quadspidata0_list[:]
    del quadspidata1_list[:]
    del quadspidata2_list[:]
    del quadspidata3_list[:]
    del quadspisclk_list[:]
    del quadspissel_list[:]
    del syswkup_list[:]
    del usb_list[:]
    del usb_otgfs_list[:]
    del usb_otghs_list[:]
    del sd_list[:]


def manage_alternate():
    update_alternate(adclist)
    update_alternate(daclist)
    update_alternate(i2cscl_list)
    update_alternate(i2csda_list)
    update_alternate(tim_list)
    update_alternate(uarttx_list)
    update_alternate(uartrx_list)
    update_alternate(uartcts_list)
    update_alternate(uartrts_list)
    update_alternate(spimosi_list)
    update_alternate(spimiso_list)
    update_alternate(spissel_list)
    update_alternate(spisclk_list)
    update_alternate(cantd_list)
    update_alternate(canrd_list)
    update_alternate(eth_list)
    update_alternate(quadspidata0_list)
    update_alternate(quadspidata1_list)
    update_alternate(quadspidata2_list)
    update_alternate(quadspidata3_list)
    update_alternate(quadspisclk_list)
    update_alternate(quadspissel_list)
    update_alternate(syswkup_list)
    update_alternate(usb_list)
    update_alternate(usb_otgfs_list)
    update_alternate_usb_otg_hs()
    update_alternate(sd_list)

    alt_list.sort(key=natural_sortkey)


def update_alternate(lst):
    prev_p = ""
    alt_index = 1
    for index, p in enumerate(lst):
        if p[0] == prev_p:
            p[0] += "_ALT%d" % alt_index
            lst[index] = p
            store_pin(p[0], p[1], alt_list)
            alt_index += 1
        else:
            prev_p = p[0]
            alt_index = 1


def update_alternate_usb_otg_hs():
    prev_p = ""
    alt_index = 1
    for nb in range(2):
        for index, p in enumerate(usb_otghs_list):
            if nb == 0:
                if "ULPI" in p[2]:
                    continue
            else:
                if "ULPI" not in p[2]:
                    continue
            if p[0] == prev_p:
                p[0] += "_ALT%d" % alt_index
                usb_otghs_list[index] = p
                store_pin(p[0], p[1], alt_list)
                alt_index += 1
            else:
                prev_p = p[0]
                alt_index = 1


def parse_pins():
    print(" * Getting pins per Ips...")
    pinregex = r"^(P[A-Z][0-9][0-5]?[_]?[C]?)|^(ANA[0-9])"
    itemlist = xml_mcu.getElementsByTagName("Pin")
    for s in itemlist:
        m = re.match(pinregex, s.attributes["Name"].value)
        if m:
            if m.group(1) is not None:
                # pin formatted P<port>_<number>: PF_O
                pin = m.group(0)[:2] + "_" + m.group(0)[2:]
            else:
                # pin formatted ANA_<number>: ANA_1
                pin = m.group(0)[:3] + "_" + m.group(0)[3:]
            name = s.attributes["Name"].value.strip()  # full name: "PF0 / OSC_IN"
            if s.attributes["Type"].value in ["I/O", "MonoIO"]:
                if pin.endswith("_C"):
                    store_pin(pin, name, dualpad_list)
                elif (
                    "Variant" in s.attributes
                    and "REMAP" in s.attributes["Variant"].value
                ):
                    pin += "_R"
                    store_pin(pin, name, remap_list)
                else:
                    store_pin(pin, name, io_list)
            else:
                continue
            siglist = s.getElementsByTagName("Signal")
            for a in siglist:
                sig = a.attributes["Name"].value.strip()
                if sig.startswith("ADC"):
                    store_adc(pin, name, sig)
                elif all(["DAC" in sig, "_OUT" in sig]):
                    store_dac(pin, name, sig)
                elif re.match("^I2C", sig) is not None:  # ignore FMPI2C
                    store_i2c(pin, name, sig)
                elif re.match("^TIM", sig) is not None:  # ignore HRTIM
                    store_tim(pin, name, sig)
                elif re.match("^(LPU|US|U)ART", sig) is not None:
                    store_uart(pin, name, sig)
                elif "SPI" in sig:
                    if "QUADSPI" in sig or "OCTOSPI" in sig:
                        store_qspi(pin, name, sig)
                    else:
                        store_spi(pin, name, sig)
                elif "CAN" in sig:
                    store_can(pin, name, sig)
                elif "ETH" in sig:
                    store_eth(pin, name, sig)
                elif "SYS_" in sig or "PWR_" in sig:
                    store_sys(pin, name, sig)
                elif "USB" in sig:
                    store_usb(pin, name, sig)
                elif re.match("^SD(IO|MMC)", sig) is not None:
                    store_sd(pin, name, sig)


# Config management
def create_config():
    # Create a Json file for a better path management
    try:
        print("Please set your configuration in '{}' file".format(config_filename))
        config_file = open(config_filename, "w", newline="\n")
        if sys.platform.startswith("win32"):
            print("Platform is Windows")
            cubemxdir = Path(
                r"C:\Program Files\STMicroelectronics\STM32Cube\STM32CubeMX"
            )
        elif sys.platform.startswith("linux"):
            print("Platform is Linux")
            cubemxdir = Path.home() / "STM32CubeMX"
        elif sys.platform.startswith("darwin"):
            print("Platform is Mac OSX")
            cubemxdir = Path(
                "/Applications/STMicroelectronics/STM32CubeMX.app/Contents/Resources"
            )
        else:
            print("Platform unknown")
            cubemxdir = "<Set CubeMX install directory>"
        config_file.write(
            json.dumps(
                {
                    "CUBEMX_DIRECTORY": str(cubemxdir),
                    "REPO_LOCAL_PATH": str(repo_local_path),
                },
                indent=2,
            )
        )
        config_file.close()
    except IOError:
        print("Failed to open " + config_filename)
    exit(1)


def check_config():
    global cubemxdir
    global repo_local_path
    global repo_path

    if config_filename.is_file():
        try:
            config_file = open(config_filename, "r")
            config = json.load(config_file)
            config_file.close()

            conf = config["REPO_LOCAL_PATH"]
            if conf:
                if conf != "":
                    repo_local_path = Path(conf)
                    repo_path = repo_local_path / repo_name
            conf = config["CUBEMX_DIRECTORY"]
            if conf:
                cubemxdir = Path(conf)
        except IOError:
            print("Failed to open " + config_filename)
    else:
        create_config()


def manage_repo():
    global db_release
    repo_local_path.mkdir(parents=True, exist_ok=True)

    print("Updating " + repo_name + "...")
    try:
        if not args.skip:
            if repo_path.is_dir():
                # Get new tags from the remote
                git_cmds = [
                    ["git", "-C", repo_path, "clean", "-fdx"],
                    ["git", "-C", repo_path, "fetch"],
                    ["git", "-C", repo_path, "reset", "--hard", "origin/master"],
                ]
            else:
                # Clone it as it does not exists yet
                git_cmds = [["git", "-C", repo_local_path, "clone", gh_url]]

            for cmd in git_cmds:
                subprocess.check_output(cmd).decode("utf-8")
        if repo_path.is_dir():
            # Get tag
            sha1_id = (
                subprocess.check_output(
                    ["git", "-C", repo_path, "rev-list", "--tags", "--max-count=1"]
                )
                .decode("utf-8")
                .strip()
            )
            version_tag = (
                subprocess.check_output(
                    ["git", "-C", repo_path, "describe", "--tags", sha1_id]
                )
                .decode("utf-8")
                .strip()
            )
            subprocess.check_output(
                ["git", "-C", repo_path, "checkout", version_tag],
                stderr=subprocess.DEVNULL,
            )
            db_release = version_tag
            return True
    except subprocess.CalledProcessError as e:
        print("Command {} failed with error code {}".format(e.cmd, e.returncode))
    return False


# main
cur_dir = Path.cwd()
templates_dir = cur_dir / "templates"
periph_c_filename = "PeripheralPins.c"
pinvar_h_filename = "PinNamesVar.h"
config_filename = Path("config.json")
variant_h_filename = "variant.h"
variant_cpp_filename = "variant.cpp"
repo_local_path = cur_dir / "repo"
gh_url = "https://github.com/STMicroelectronics/STM32_open_pin_data"
repo_name = gh_url.rsplit("/", 1)[-1]
repo_path = repo_local_path / repo_name
db_release = "Unknown"

check_config()

# By default, generate for all mcu xml files description
parser = argparse.ArgumentParser(
    description=textwrap.dedent(
        """\
By default, generate {}, {}, {} and {}
for all xml files description available in STM32CubeMX internal database.
Internal database path must be defined in {}.
It can be the one from STM32CubeMX directory if defined:
\t{}
or the one from GitHub:
\t{}

""".format(
            periph_c_filename,
            pinvar_h_filename,
            variant_cpp_filename,
            variant_h_filename,
            config_filename,
            cubemxdir,
            gh_url,
        )
    ),
    epilog=textwrap.dedent(
        """\
After files generation, review them carefully and please report any issue to GitHub:
\thttps://github.com/stm32duino/Arduino_Tools/issues\n
Once generated, you can comment a line if the pin should not be used
(overlaid with some HW on the board, for instance) and update all undefined pins
in variant."""
    ),
    formatter_class=RawTextHelpFormatter,
)
group = parser.add_mutually_exclusive_group()
group.add_argument(
    "-l",
    "--list",
    help="list available xml files description in STM32CubeMX",
    action="store_true",
)
group.add_argument(
    "-m",
    "--mcu",
    metavar="xml",
    help=textwrap.dedent(
        """\
Generate {}, {}, {} and {}
for specified mcu xml file description in STM32CubeMX.
This xml file can contain non alpha characters in its name,
you should call it with double quotes""".format(
            periph_c_filename,
            pinvar_h_filename,
            variant_cpp_filename,
            variant_h_filename,
        )
    ),
)

parser.add_argument(
    "-c",
    "--cube",
    help=textwrap.dedent(
        """\
Use STM32CubeMX internal database. Default use GitHub {} repository.
""".format(
            repo_name
        )
    ),
    action="store_true",
)
parser.add_argument(
    "-s",
    "--skip",
    help="Skip {} clone/fetch".format(repo_name),
    action="store_true",
)
args = parser.parse_args()

# Using GitHub repo is the preferred way, CubeMX used as a fallback
fallback = False
if not args.cube:
    if manage_repo():
        dirMCU = repo_path / "mcu"
        dirIP = dirMCU / "IP"
    else:
        fallback = True
if fallback or args.cube:
    if not (cubemxdir.is_dir()):
        print(
            """
Cube Mx seems not to be installed or not at the specified location.

Please check the value set for 'CUBEMX_DIRECTORY' in '{}' file.""".format(
                config_filename
            )
        )
        quit()

    dirMCU = cubemxdir / "db" / "mcu"
    dirIP = dirMCU / "IP"
    version_file = cubemxdir / "db" / "package.xml"
    if version_file.is_file():
        xml_file = parse(str(version_file))
        PackDescription_item = xml_file.getElementsByTagName("PackDescription")
        for item in PackDescription_item:
            db_release = item.attributes["Release"].value

# Process DB release
release_regex = r".*(\d+.\d+.\d+)$"
release_match = re.match(release_regex, db_release)
if release_match:
    db_release = release_match.group(1)
print("CubeMX DB release {}\n".format(db_release))

if args.mcu:
    # Check input file exists
    if not ((dirMCU / args.mcu).is_file()):
        print("\n" + args.mcu + " file not found")
        print("\nCheck in " + dirMCU + " the correct name of this file")
        print("\nYou may use double quotes for file containing special characters")
        quit()
    mcu_list.append(dirMCU / args.mcu)
else:
    mcu_list = dirMCU.glob("STM32*.xml")

if args.list:
    print("Available xml files description:")
    for f in mcu_list:
        print(f.name)
    quit()

# Create the jinja2 environment.
j2_env = Environment(
    loader=FileSystemLoader(templates_dir), trim_blocks=True, lstrip_blocks=True
)

for mcu_file in mcu_list:
    print("Generating files for '{}'...".format(mcu_file.name))
    if "MP1" in mcu_file.name:
        mcu_dir = "STM32MP1xx"
    else:
        mcu_dir = mcu_file.name[:7] + "xx"
    out_path = cur_dir / "Arduino" / mcu_dir / mcu_file.stem
    periph_c_filepath = out_path / periph_c_filename
    pinvar_h_filepath = out_path / pinvar_h_filename
    variant_cpp_filepath = out_path / variant_cpp_filename
    variant_h_filepath = out_path / variant_h_filename
    out_path.mkdir(parents=True, exist_ok=True)

    # open output file
    periph_c_filepath.unlink(missing_ok=True)
    periph_c_file = open(periph_c_filepath, "w", newline="\n")
    pinvar_h_filepath.unlink(missing_ok=True)
    pinvar_h_file = open(pinvar_h_filepath, "w", newline="\n")
    variant_cpp_filepath.unlink(missing_ok=True)
    variant_cpp_file = open(variant_cpp_filepath, "w", newline="\n")
    variant_h_filepath.unlink(missing_ok=True)
    variant_h_file = open(variant_h_filepath, "w", newline="\n")

    # open input file
    xml_mcu = parse(str(mcu_file))
    gpiofile = find_gpio_file()
    if gpiofile == "ERROR":
        print("Could not find GPIO file")
        quit()
    xml_gpio = parse(str(dirIP / ("GPIO-" + gpiofile + "_Modes.xml")))

    parse_pins()
    sort_my_lists()
    manage_alternate()
    print_peripheral()
    print_pinamevar()
    print_variant()

    print(
        "* Total I/O pins found: {}".format(
            len(io_list) + len(alt_list) + len(dualpad_list) + len(remap_list)
        )
    )
    print("   - {} I/O pins".format(len(io_list)))
    if len(dualpad_list):
        print("   - {} dual pad".format(len(dualpad_list)))
    if len(remap_list):
        print("   - {} remap pins".format(len(remap_list)))
    print("   - {} ALT I/O pins".format(len(alt_list)))

    # for io in io_list:
    #     print(io[0] + ", " + io[1])

    clean_all_lists()

    periph_c_file.close()
    pinvar_h_file.close()
    variant_h_file.close()
    variant_cpp_file.close()

/*
 *******************************************************************************
 * Copyright (c) 2021, STMicroelectronics
 * All rights reserved.
 *
 * This software component is licensed by ST under BSD 3-Clause license,
 * the "License"; You may not use this file except in compliance with the
 * License. You may obtain a copy of the License at:
 *                        opensource.org/licenses/BSD-3-Clause
 *
 *******************************************************************************
 */

#ifndef _VARIANT_ARDUINO_STM32_
#define _VARIANT_ARDUINO_STM32_
#ifdef __cplusplus
extern "C" {
#endif // __cplusplus

/*----------------------------------------------------------------------------
 *        STM32 pins number
 *----------------------------------------------------------------------------*/
#define PA0                     A0
#define PA1                     A1
#define PA2                     A2
#define PA3                     A3
#define PA4                     A4
#define PA5                     A5
#define PA6                     A6
#define PA7                     A7
#define PA8                     8
#define PA9                     9
#define PA10                    10
#define PA11                    11
#define PA12                    12
#define PA13                    13
#define PA14                    14
#define PA15                    15
#define PB0                     A8
#define PB1                     A9
#define PB2                     A10
#define PB3                     19
#define PB4                     20
#define PB5                     21
#define PB6                     22
#define PB7                     23
#define PB8                     24
#define PB9                     25
#define PB10                    26
#define PB11                    A11
#define PB12                    A12
#define PB13                    A13
#define PB14                    A14
#define PB15                    A15
#define PC0                     A16
#define PC1                     A17
#define PC2                     A18
#define PC3                     A19
#define PC4                     A20
#define PC5                     A21
#define PC6                     38
#define PC7                     39
#define PC8                     40
#define PC9                     41
#define PC10                    42
#define PC11                    43
#define PC12                    44
#define PC13                    45
#define PC14                    46
#define PC15                    47
#define PD0                     48
#define PD1                     49
#define PD2                     50
#define PD3                     51
#define PD4                     52
#define PD7                     53
#define PD9                     A22
#define PD10                    A23
#define PD11                    A24
#define PD12                    A25
#define PD13                    A26
#define PD14                    A27
#define PD15                    60
#define PE0                     61
#define PE1                     62
#define PE2                     63
#define PE3                     64
#define PE4                     65
#define PE5                     66
#define PE6                     67
#define PE7                     A28
#define PE8                     A29
#define PE11                    A30
#define PE12                    A31
#define PF0                     72
#define PF1                     73
#define PF2                     A32
#define PF6                     75
#define PF9                     76
#define PF10                    77

// Alternate pins number
#define PA1_ALT1                (PA1  | ALT1)
#define PA2_ALT1                (PA2  | ALT1)
#define PA3_ALT1                (PA3  | ALT1)
#define PA4_ALT1                (PA4  | ALT1)
#define PA6_ALT1                (PA6  | ALT1)
#define PA7_ALT1                (PA7  | ALT1)
#define PA7_ALT2                (PA7  | ALT2)
#define PA7_ALT3                (PA7  | ALT3)
#define PA9_ALT1                (PA9  | ALT1)
#define PA10_ALT1               (PA10 | ALT1)
#define PA11_ALT1               (PA11 | ALT1)
#define PA11_ALT2               (PA11 | ALT2)
#define PA12_ALT1               (PA12 | ALT1)
#define PA12_ALT2               (PA12 | ALT2)
#define PA13_ALT1               (PA13 | ALT1)
#define PA15_ALT1               (PA15 | ALT1)
#define PB0_ALT1                (PB0  | ALT1)
#define PB0_ALT2                (PB0  | ALT2)
#define PB1_ALT1                (PB1  | ALT1)
#define PB1_ALT2                (PB1  | ALT2)
#define PB3_ALT1                (PB3  | ALT1)
#define PB4_ALT1                (PB4  | ALT1)
#define PB4_ALT2                (PB4  | ALT2)
#define PB5_ALT1                (PB5  | ALT1)
#define PB5_ALT2                (PB5  | ALT2)
#define PB6_ALT1                (PB6  | ALT1)
#define PB6_ALT2                (PB6  | ALT2)
#define PB7_ALT1                (PB7  | ALT1)
#define PB7_ALT2                (PB7  | ALT2)
#define PB8_ALT1                (PB8  | ALT1)
#define PB8_ALT2                (PB8  | ALT2)
#define PB9_ALT1                (PB9  | ALT1)
#define PB9_ALT2                (PB9  | ALT2)
#define PB11_ALT1               (PB11 | ALT1)
#define PB14_ALT1               (PB14 | ALT1)
#define PB15_ALT1               (PB15 | ALT1)
#define PB15_ALT2               (PB15 | ALT2)
#define PC0_ALT1                (PC0  | ALT1)
#define PC1_ALT1                (PC1  | ALT1)
#define PC2_ALT1                (PC2  | ALT1)
#define PC3_ALT1                (PC3  | ALT1)
#define PC6_ALT1                (PC6  | ALT1)
#define PC7_ALT1                (PC7  | ALT1)
#define PC8_ALT1                (PC8  | ALT1)
#define PC9_ALT1                (PC9  | ALT1)
#define PC10_ALT1               (PC10 | ALT1)
#define PC11_ALT1               (PC11 | ALT1)
#define PD10_ALT1               (PD10 | ALT1)
#define PD11_ALT1               (PD11 | ALT1)
#define PD12_ALT1               (PD12 | ALT1)
#define PD13_ALT1               (PD13 | ALT1)
#define PD14_ALT1               (PD14 | ALT1)
#define PE1_ALT1                (PE1  | ALT1)
#define PE2_ALT1                (PE2  | ALT1)
#define PE3_ALT1                (PE3  | ALT1)
#define PE4_ALT1                (PE4  | ALT1)
#define PE5_ALT1                (PE5  | ALT1)
#define PE8_ALT1                (PE8  | ALT1)
#define PF2_ALT1                (PF2  | ALT1)

#define NUM_DIGITAL_PINS        78
#define NUM_ANALOG_INPUTS       33

// On-board LED pin number
#ifndef LED_BUILTIN
#define LED_BUILTIN             PYn
#endif

// On-board user button
#ifndef USER_BTN
#define USER_BTN                PYn
#endif

// SPI definitions
#ifndef PIN_SPI_SS
#define PIN_SPI_SS              PA4
#endif
#ifndef PIN_SPI_SS1
#define PIN_SPI_SS1             PA15
#endif
#ifndef PIN_SPI_SS2
#define PIN_SPI_SS2             PYn
#endif
#ifndef PIN_SPI_SS3
#define PIN_SPI_SS3             PYn
#endif
#ifndef PIN_SPI_MOSI
#define PIN_SPI_MOSI            PA7
#endif
#ifndef PIN_SPI_MISO
#define PIN_SPI_MISO            PA6
#endif
#ifndef PIN_SPI_SCK
#define PIN_SPI_SCK             PA5
#endif

// I2C definitions
#ifndef PIN_WIRE_SDA
#define PIN_WIRE_SDA            PA10
#endif
#ifndef PIN_WIRE_SCL
#define PIN_WIRE_SCL            PA9
#endif

// Timer Definitions
// Use TIM6/TIM7 when possible as servo and tone don't need GPIO output pin
#ifndef TIMER_TONE
#define TIMER_TONE              TIM6
#endif
#ifndef TIMER_SERVO
#define TIMER_SERVO             TIM7
#endif

// UART Definitions
#ifndef SERIAL_UART_INSTANCE
#define SERIAL_UART_INSTANCE    2
#endif

// Default pin used for generic 'Serial' instance
// Mandatory for Firmata
#ifndef PIN_SERIAL_RX
#define PIN_SERIAL_RX           PA3
#endif
#ifndef PIN_SERIAL_TX
#define PIN_SERIAL_TX           PA2
#endif

// Extra HAL modules
#define HAL_DAC_MODULE_ENABLED

#ifdef __cplusplus
} // extern "C"
#endif

/*----------------------------------------------------------------------------
 *        Arduino objects - C++ only
 *----------------------------------------------------------------------------*/

#ifdef __cplusplus
  // These serial port names are intended to allow libraries and architecture-neutral
  // sketches to automatically default to the correct port name for a particular type
  // of use.  For example, a GPS module would normally connect to SERIAL_PORT_HARDWARE_OPEN,
  // the first hardware serial port whose RX/TX pins are not dedicated to another use.
  //
  // SERIAL_PORT_MONITOR        Port which normally prints to the Arduino Serial Monitor
  //
  // SERIAL_PORT_USBVIRTUAL     Port which is USB virtual serial
  //
  // SERIAL_PORT_LINUXBRIDGE    Port which connects to a Linux system via Bridge library
  //
  // SERIAL_PORT_HARDWARE       Hardware serial port, physical RX & TX pins.
  //
  // SERIAL_PORT_HARDWARE_OPEN  Hardware serial ports which are open for use.  Their RX & TX
  //                            pins are NOT connected to anything by default.
  #define SERIAL_PORT_MONITOR   Serial
  #define SERIAL_PORT_HARDWARE  Serial
#endif

#endif /* _VARIANT_ARDUINO_STM32_ */
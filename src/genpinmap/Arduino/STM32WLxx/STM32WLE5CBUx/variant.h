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
#define PA0                     0
#define PA1                     1
#define PA2                     2
#define PA3                     3
#define PA4                     4
#define PA5                     5
#define PA6                     6
#define PA7                     7
#define PA8                     8
#define PA9                     9
#define PA10                    A0
#define PA11                    A1
#define PA12                    A2
#define PA13                    A3
#define PA14                    A4
#define PA15                    A5
#define PB0                     16
#define PB2                     A6
#define PB3                     A7
#define PB4                     A8
#define PB5                     20
#define PB6                     21
#define PB7                     22
#define PB8                     23
#define PB12                    24
#define PC13                    25
#define PC14                    26
#define PC15                    27
#define PH3                     28

// Alternate pins number
#define PA1_ALT1                (PA1 | ALT1)
#define PA2_ALT1                (PA2 | ALT1)
#define PA3_ALT1                (PA3 | ALT1)
#define PA7_ALT1                (PA7 | ALT1)
#define PB8_ALT1                (PB8 | ALT1)

#define NUM_DIGITAL_PINS        29
#define NUM_ANALOG_INPUTS       9

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
#define PIN_SPI_SS2             PB2
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
#define PIN_SPI_SCK             PA1
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
#define TIMER_TONE              TIM16
#endif
#ifndef TIMER_SERVO
#define TIMER_SERVO             TIM17
#endif

// UART Definitions
#ifndef SERIAL_UART_INSTANCE
#define SERIAL_UART_INSTANCE    101
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
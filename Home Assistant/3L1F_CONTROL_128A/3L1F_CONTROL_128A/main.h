/*
 * main.h
 *
 * Created: 24-08-2024 08:44:55
 *  Author: kjeyabalan
 */ 


#ifndef MAIN_H_
#define MAIN_H_

#define F_CPU 16000000UL
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/wdt.h>
#include <util/delay.h>
#include <util/twi.h>
#include <string.h>
#include "fan_control.h"
#include "lights.h"
#include "eeprom.h"
#include "i2c.h"
#include "uart.h"
#include "spiDataProcess.h"
#include "uartDataProcess.h"

// USART configuration
#define FOSC 16000000 // Clock Speed
#define BAUD 9600
#define MYUBRR FOSC / 16 / BAUD - 1

#define EEPROM_ADDR 0x50 // EEPROM address

#define POLYNOMIAL 0x07  // CRC polynomial
#define INIT_CRC 0x00

/*#define SPI_SS_PIN PB0     // SS pin connected to PB0
#define SPI_MOSI_PIN PB2   // MOSI pin connected to PB2
#define SPI_MISO_PIN PB3   // MISO pin connected to PB3
#define SPI_SCK_PIN PB1    // SCK pin connected to PB1*/

typedef struct{
	uint8_t lightState_1;
	uint8_t lightState_2;
	uint8_t lightState_3;
	uint8_t lastF1State;
}states;

extern volatile states laststate;
extern uint16_t light1_address;
extern uint16_t light2_address;
extern uint16_t light3_address;
extern uint16_t fan1_address;
extern uint8_t fan1_speed;
extern volatile uint8_t timer_flag;
//extern const char* command;

void timer1_init();
void custom_delay_ms(uint16_t ms);
void SPI_init_slave();
void setup(void);
void readLastStatesFromEEPROM(void);
void clearEEPROM(void);
void retainLightStates(void);
void retainFanState(void);
void handle_All_OFF();
void handle_All_ON();
void handle_SPI_interrupt(void);
void handle_UART_interrupt(void);
void init_watchdog_timer(void);
void handle_watchdog_event();
void handle_TIMER_interrupt();
void write_All_States_ToEEPROM();
//void timer0_init(void);

#endif /* MAIN_H_ */
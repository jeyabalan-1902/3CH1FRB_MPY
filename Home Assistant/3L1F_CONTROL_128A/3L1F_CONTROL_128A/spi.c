/*
 * spi.c
 *
 * Created: 17-09-2024 09:41:16
 *  Author: kjeya
 */ 


#include "spi.h"

void SPI_MasterInit(void) {
	// Set MOSI, SCK, and SS as output, MISO as input
	DDRB |= (1 << SPI_MOSI_PIN) | (1 << SPI_SCK_PIN) | (1 << SPI_SS_PIN);
	DDRB &= ~(1 << SPI_MISO_PIN);  // MISO as input

	// Enable SPI, set as Master, set clock rate (fck/16)
	SPCR = (1 << SPE) | (1 << MSTR) | (1 << SPR0);  // Enable SPI and set as master
}

// SPI Slave Initialization
void SPI_SlaveInit(void) {
	// Set MISO as output, MOSI, SCK, and SS as input
	DDRB |= (1 << SPI_MISO_PIN);  // MISO as output
	DDRB &= ~(1 << SPI_MOSI_PIN) & ~(1 << SPI_SCK_PIN) & ~(1 << SPI_SS_PIN);  // MOSI, SCK, SS as input

	// Enable SPI, set as Slave
	SPCR = (1 << SPE);  // Enable SPI and set as slave
}

// SPI Master Transmit Data
void SPI_MasterTransmit(uint8_t data) {
	// Start transmission by pulling SS low
	PORTB &= ~(1 << SPI_SS_PIN);

	// Load data into the SPI data register
	SPDR = data;

	// Wait for transmission to complete
	while (!(SPSR & (1 << SPIF)));

	// End transmission by pulling SS high
	PORTB |= (1 << SPI_SS_PIN);
}

// SPI Master Receive Data
uint8_t SPI_MasterReceive(void) {
	// Transmit dummy byte to initiate SPI clock for receiving data
	SPDR = 0xFF;  // Dummy byte

	// Wait for reception to complete
	while (!(SPSR & (1 << SPIF)));

	// Return received data
	return SPDR;
}

// SPI Slave Transmit and Receive (via interrupt or polling)
uint8_t SPI_SlaveTransmit(uint8_t data) {
	// Load data to send to the master
	SPDR = data;

	// Wait for transmission/reception to complete
	while (!(SPSR & (1 << SPIF)));

	// Return received data from master
	return SPDR;
}
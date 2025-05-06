/*
 * i2c.c
 *
 * Created: 24-08-2024 08:46:41
 *  Author: kjeyabalan
 */ 


#include "i2c.h"

void i2c_init(void) {
	TWSR = 0x00;
	TWBR = 0x48;
}

void i2c_start(void) {
	TWCR = (1<<TWSTA) | (1<<TWEN) | (1<<TWINT);
	while (!(TWCR & (1<<TWINT)));
}

void i2c_stop(void) {
	TWCR = (1<<TWSTO) | (1<<TWEN) | (1<<TWINT);
	while (TWCR & (1<<TWSTO));
}

void i2c_write(uint8_t data) {
	TWDR = data;
	TWCR = (1<<TWEN) | (1<<TWINT);
	while (!(TWCR & (1<<TWINT)));
}

uint8_t i2c_read_ack(void) {
	TWCR = (1<<TWEN) | (1<<TWINT) | (1<<TWEA);
	while (!(TWCR & (1<<TWINT)));
	return TWDR;
}

uint8_t i2c_read_nack(void) {
	TWCR = (1<<TWEN) | (1<<TWINT);
	while (!(TWCR & (1<<TWINT)));
	return TWDR;
}
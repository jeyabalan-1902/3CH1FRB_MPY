/*
 * eeprom.c
 *
 * Created: 24-08-2024 08:45:45
 *  Author: kjeyabalan
 */ 


#include "eeprom.h"


void eeprom_write(uint16_t address, uint8_t data) {
	i2c_start();
	i2c_write((EEPROM_ADDR << 1) | 0);
	i2c_write((address >> 8) & 0xFF);
	i2c_write(address & 0xFF);
	i2c_write(data);
	i2c_stop();
}

uint8_t eeprom_read(uint16_t address) {
	uint8_t data;
	i2c_start();
	i2c_write((EEPROM_ADDR << 1) | 0);
	i2c_write((address >> 8) & 0xFF);
	i2c_write(address & 0xFF);
	i2c_start();
	i2c_write((EEPROM_ADDR << 1) | 1);
	data = i2c_read_nack();
	i2c_stop();
	return data;
}
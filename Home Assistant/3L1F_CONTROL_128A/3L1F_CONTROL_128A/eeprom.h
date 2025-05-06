/*
 * eeprom.h
 *
 * Created: 24-08-2024 08:46:03
 *  Author: kjeyabalan
 */ 


#ifndef EEPROM_H_
#define EEPROM_H_


#include "main.h"

void eeprom_write(uint16_t address, uint8_t data);
uint8_t eeprom_read(uint16_t address);


#endif /* EEPROM_H_ */
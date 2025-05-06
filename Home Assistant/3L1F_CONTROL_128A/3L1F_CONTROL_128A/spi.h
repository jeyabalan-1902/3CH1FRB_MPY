/*
 * spi.h
 *
 * Created: 17-09-2024 09:41:33
 *  Author: kjeya
 */ 


#ifndef SPI_H_
#define SPI_H_

#include "main.h"

void SPI_MasterInit(void);
void SPI_SlaveInit(void);
void SPI_MasterTransmit(uint8_t data) ;
uint8_t SPI_MasterReceive(void);
uint8_t SPI_SlaveTransmit(uint8_t data);


#endif /* SPI_H_ */
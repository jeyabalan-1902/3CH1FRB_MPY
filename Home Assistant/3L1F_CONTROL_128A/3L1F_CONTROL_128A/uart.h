/*
 * uart.h
 *
 * Created: 24-08-2024 08:47:21
 *  Author: kjeyabalan
 */ 


#ifndef UART_H_
#define UART_H_

#include "main.h"

void USART_Init(unsigned int ubrr);
void USART_Transmit(uint8_t data);
unsigned char USART_Receive(void);
void USART_SendString(const char *str);


#endif /* UART_H_ */
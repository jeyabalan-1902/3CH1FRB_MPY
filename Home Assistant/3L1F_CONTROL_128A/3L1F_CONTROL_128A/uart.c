/*
 * uart.c
 *
 * Created: 24-08-2024 08:47:01
 *  Author: kjeyabalan
 */ 


#include "uart.h"


void USART_Init(unsigned int ubrr)
{
	UBRR0H = (unsigned char)(ubrr >> 8);
	UBRR0L = (unsigned char)ubrr;
	UCSR0B = (1 << RXEN0) | (1 << TXEN0) | (1 << RXCIE0);
	UCSR0C = (1 << USBS0) | (3 << UCSZ00);
}

void USART_Transmit(uint8_t data) {
	while (!(UCSR0A & (1 << UDRE0)));
	UDR0 = data;
}

void USART_SendString(const char *str) {
	while (*str) {
		USART_Transmit(*str++);
	}
}

unsigned char USART_Receive(void)
{
	while (!(UCSR0A & (1 << RXC0)));
	return UDR0;
}
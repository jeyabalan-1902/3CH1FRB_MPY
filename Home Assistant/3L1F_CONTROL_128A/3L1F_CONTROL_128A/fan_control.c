/*
 * fan_control.c
 *
 * Created: 24-08-2024 08:55:24
 *  Author: kjeyabalan
 */ 


#include "fan_control.h"

void as0() {                     // Fan Speed 0
	
	PORTC &= ~(1 << PC2);     //Fan On Led
	
	PORTD &= ~(1 << PD4);
	PORTD &= ~(1 << PD5);
	PORTD &= ~(1 << PD6);     // Led Pins
	PORTD &= ~(1 << PD7);
	PORTC &= ~(1 << PC0);

	PORTF &= ~(1 << PF0);     //Relay Pins
	PORTF &= ~(1 << PF1);
	PORTF &= ~(1 << PF2);
	PORTF &= ~(1 << PF3);
}

void as1() {         // Fan speed 1

	PORTC |= (1 << PC2);   //Fan On Led

	PORTD |= (1 << PD4);
	PORTD &= ~(1 << PD5);
	PORTD &= ~(1 << PD6);     // Led Pins
	PORTD &= ~(1 << PD7);
	PORTC &= ~(1 << PC0);
	//relay Pins
	PORTF &= ~ (1 << PF0);
	PORTF |= (1 << PF1);   //2.2k
	PORTF &= ~(1 << PF2);
	PORTF &= ~(1 << PF3);
}

void as2() {   // fan Speed 2

	PORTC |= (1 << PC2); //Fan on led
	
	PORTD |= (1 << PD4);
	PORTD |= (1 << PD5);
	PORTD &= ~(1 << PD6);     // Led Pins
	PORTD &= ~(1 << PD7);
	PORTC &= ~(1 << PC0);

	PORTF |=  (1 << PF0);     //Relay Pins
	PORTF |= (1 << PF1);
	PORTF &= ~ (1 << PF2);     //3.3k
	PORTF &= ~(1 << PF3);
}

void as3() {   //Fan speed 3

	PORTC |= (1 << PC2); //fan on led
	
	PORTD |= (1 << PD4);
	PORTD |= (1 << PD5);
	PORTD |= (1 << PD6);     // Led Pins
	PORTD &= ~(1 << PD7);
	PORTC &= ~(1 << PC0);

	PORTF |= (1 << PF0);     //Relay Pins
	PORTF &= ~(1 << PF1);
	PORTF |= (1 << PF2);    //4.3k
	PORTF &= ~(1 << PF3);
}

void as4() {     //Fan speed 4
	
	PORTC |= (1 << PC2); //fan on led
	
	PORTD |= (1 << PD4);
	PORTD |= (1 << PD5);
	PORTD |= (1 << PD6);     // Led Pins
	PORTD |= (1 << PD7);
	PORTC &= ~(1 << PC0);

	PORTF &= ~(1 << PF0);     //Relay Pins
	PORTF |= (1 << PF1);
	PORTF |= (1 << PF2);      //5.5k
	PORTF &= ~(1 << PF3);
}

void as5() {       // fan speed 5
	
	PORTC |= (1 << PC2);  // fan on led
	
	PORTD |= (1 << PD4);
	PORTD |= (1 << PD5);
	PORTD |= (1 << PD6);     // Led Pins
	PORTD |= (1 << PD7);
	PORTC |= (1 << PC0);
	

	PORTF &= ~(1 << PF0);     //Relay Pins
	PORTF &= ~(1 << PF1);
	PORTF &= ~(1 << PF2);
	PORTF |= (1 << PF3);       //direct
}

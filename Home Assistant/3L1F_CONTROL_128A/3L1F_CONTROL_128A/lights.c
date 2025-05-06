/*
 * lights.c
 *
 * Created: 24-08-2024 08:55:04
 *  Author: kjeyabalan
 */ 


#include "lights.h"

void light1_ON(){
	PORTC |= (1 << PC1);
	PORTF |= (1 << PF4);
	laststate.lightState_1 = 1;
}

void light1_OFF(){
	PORTC &= ~(1 << PC1);
	PORTF &= ~(1 << PF4);
	laststate.lightState_1 = 0;
}

void light2_ON(){
	PORTC |= (1 << PC3);
	PORTF |= (1 << PF5);
	laststate.lightState_2 = 1;
}
void light2_OFF(){
	PORTC &= ~(1 << PC3);
	PORTF &= ~(1 << PF5);
	laststate.lightState_2 = 0;
}

void light3_ON(){
	PORTC |= (1 << PC4);
	PORTF |= (1 << PF6);
	laststate.lightState_3 = 1;
}

void light3_OFF(){
	PORTC &= ~(1 << PC4);
	PORTF &= ~(1 << PF6);
	laststate.lightState_3 = 0;
}
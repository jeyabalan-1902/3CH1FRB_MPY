/*
 * uartDataProcess.c
 *
 * Created: 27-08-2024 15:08:38
 *  Author: kjeyabalan
 */ 

#include "uartDataProcess.h"

void UARTprocessCommand(unsigned char receivedData){
	if (receivedData == 'L') {
		receivedData = USART_Receive();
		if (receivedData == '1') {	    // light1 ON
			light1_ON();
		}
		else if (receivedData == '0') {   //light1 OFF
			light1_OFF();
		}
	}
	
	else if (receivedData == 'M') {
		receivedData = USART_Receive();
		if (receivedData == '1') {        // light2 ON
			light2_ON();
		}
		else if (receivedData == '0') {       //light2 OFF
			light2_OFF();
		}
	}
	
	else if (receivedData == 'N') {
		receivedData = USART_Receive();
		if (receivedData == '1') {      //light3 ON
			light3_ON();
		}
		else if (receivedData == '0') {     //light3 OFF
			light3_OFF();
		}
	}
	else if (receivedData == 'F') {
		receivedData = USART_Receive();
		if (receivedData == '1') {     // fan ON
			as1();
			laststate.lastF1State = 1;
			fan1_speed = 1;
		}
		else if(receivedData == '2')
		{
			as3();
			laststate.lastF1State = 2;
			fan1_speed = 2;
		}
		else if (receivedData == '3') {    
			as5();
			laststate.lastF1State = 3;
			fan1_speed = 3;
		}
		else if (receivedData == '0') {       // Fan OFF
			as0();
			laststate.lastF1State = 0;
		}	
	}
}
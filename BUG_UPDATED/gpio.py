import esp32
import machine
from machine import Pin, Timer
import utime
import uasyncio as asyncio
 

S_Led = Pin(17, Pin.OUT)

Rst = Pin(4, Pin.IN, Pin.PULL_UP)

# Globals
press_start_time = None
reset_timer = Timer(2)
  
async def http_server_led():
    for _ in range(3):
        S_Led.value(1)
        await asyncio.sleep(1)
        S_Led.value(0)
        await asyncio.sleep(1)

    
async def blink_reconnect():
    for _ in range(3):
        S_Led.value(1)
        await asyncio.sleep(0.5)
        S_Led.value(0)
        await asyncio.sleep(0.5)
    






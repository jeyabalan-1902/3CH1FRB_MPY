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

DEBOUNCE_DELAY = 400
debounce_timer = Timer(1)

last_trigger_times = {
    "F1": 0,
    "F2": 0,
    "F3": 0,
    "F4": 0,
}

    
async def http_server_led():
    for _ in range(3):
        S_Led.value(1)
        await asyncio.sleep(1)
        S_Led.value(0)
        await asyncio.sleep(1)

    

    






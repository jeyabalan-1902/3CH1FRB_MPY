import esp32
import machine
from machine import Pin, Timer
import utime
from mqtt import*

# Pin Setup
R1 = Pin(25, Pin.OUT)   #light 1
R2 = Pin(33, Pin.OUT)   #light 2
R3 = Pin(32, Pin.OUT)   #light 3
R4 = Pin(13, Pin.OUT)   #fan speed 1
R5 = Pin(14, Pin.OUT)   #fan speed 2
R6 = Pin(27, Pin.OUT)   #fan_speed 3
R7 = Pin(26, Pin.OUT)   #fan_speed 4

S_Led = Pin(17, Pin.OUT)

F1 = Pin(5, Pin.IN, Pin.PULL_DOWN)
F2 = Pin(18, Pin.IN, Pin.PULL_DOWN)
F3 = Pin(19, Pin.IN, Pin.PULL_DOWN)
F4 = Pin(23, Pin.IN, Pin.PULL_DOWN)

Rst = Pin(4, Pin.IN, Pin.PULL_UP)

# Globals
last_trigger_times = {"F1": 0, "F2": 0, "F3": 0, "F4": 0}
press_start_time = None
DEBOUNCE_DELAY = 400
debounce_timer = Timer(2)
reset_timer = Timer(1)


    
def http_server_led():
    S_Led.value(1)
    time.sleep(1)
    S_Led.value(0)
    time.sleep(1)
    S_Led.value(1)
    time.sleep(1)
    S_Led.value(0)
    time.sleep(1)
    S_Led.value(1)
    time.sleep(1)
    S_Led.value(0)
    time.sleep(1)
    

    






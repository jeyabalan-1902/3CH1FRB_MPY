from machine import I2C, Pin
import time


i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=50000)
EEPROM_ADDR = 0x50

def save_device_states(r1, r2, r3, fan_state, fan_speed):
    data = bytes([r1, r2, r3, fan_state, fan_speed])
    i2c.writeto_mem(EEPROM_ADDR, 0x00, data)
    print("All device states saved to EEPROM:", data)

def load_device_states():
    data = i2c.readfrom_mem(EEPROM_ADDR, 0x00, 5)
    print("All device states loaded from EEPROM:", data)

    r1 = data[0] if data[0] in [0, 1] else 0
    r2 = data[1] if data[1] in [0, 1] else 0
    r3 = data[2] if data[2] in [0, 1] else 0
    fan_state = data[3] if data[3] in [0, 1] else 0
    fan_speed = data[4] if 0 <= data[4] <= 5 else 0

    return r1, r2, r3, fan_state, fan_speed

def view_eeprom_data():
    try:
        data = i2c.readfrom_mem(EEPROM_ADDR, 0x00, 5)
        print("EEPROM raw data:", list(data))
        return data
    except Exception as e:
        print("EEPROM view error:", e)
        return None

from machine import I2C, Pin
import time


i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
EEPROM_ADDR = 0x50

def save_relay_state(r1, r2, r3):
    data = bytes([r1, r2, r3])
    i2c.writeto_mem(EEPROM_ADDR, 0x00, data)
    print("Relay states saved to EEPROM:", data)

def load_relay_state():
    state = i2c.readfrom_mem(EEPROM_ADDR, 0x00, 3)
    print("Relay states loaded from EEPROM:", state)
    return state[0], state[1], state[2]

def save_fan_state(fan_state, speed):
    data = bytes([fan_state, speed])
    i2c.writeto_mem(EEPROM_ADDR, 0x03, data)
    print("Fan state and speed saved to EEPROM:", data)

def load_fan_state():
    data = i2c.readfrom_mem(EEPROM_ADDR, 0x03, 2)
    print("Fan state and speed loaded from EEPROM:", data)
    return data[0], data[1]

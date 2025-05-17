import esp32
from umqtt.simple import MQTTClient
import ujson
import ntptime
import time
import ubinascii
import urandom
import machine
import utime
import network
from collections import OrderedDict
from machine import Timer, Pin
import uasyncio as asyncio
from nvs import get_product_id, product_key, clear_wifi_credentials, store_pid, nvs
from gpio import S_Led
from at24c32n import eeprom, save_device_states
from wifi_con import wifi


client = None
mqtt_listener_task = None
mqtt_keepalive_task = None
mqtt_reconnect_lock = asyncio.Lock()

product_id = get_product_id()

last_fan_speed = 0
fan_state = 0

BROKER_ADDRESS = "mqtt.onwords.in"
PORT = 1883
USERNAME = "Nikhil"
MQTT_PASSWORD = "Nikhil8182"
MQTT_KEEPALIVE = 60
MQTT_CLIENT_ID = product_id

TOPIC_STATUS = f"onwords/{product_id}/status"
TOPIC_GET_CURRENT_STATUS = f"onwords/{product_id}/getCurrentStatus"
TOPIC_SOFTRST = f"onwords/{product_id}/softReset"
TOPIC_CURRENT_STATUS = f"onwords/{product_id}/currentStatus"
TOPIC_PID = f"onwords/{product_id}/storePid"
TOPIC_FIRMWARE = f"onwords/{product_id}/firmware"
TOPIC_DEVICE_LOG = f"onwords/{product_id}/switch"
TOPIC_CREDENTIALS = f"onwords/{product_id}/credentials"



# Pin Setup
R1 = Pin(25, Pin.OUT)   #light 1
R2 = Pin(33, Pin.OUT)   #light 2
R3 = Pin(32, Pin.OUT)   #light 3
R4 = Pin(13, Pin.OUT)   #fan speed 1
R5 = Pin(14, Pin.OUT)   #fan speed 2
R6 = Pin(27, Pin.OUT)   #fan_speed 3
R7 = Pin(26, Pin.OUT)   #fan_speed 4

def get_timestamp():
    try:
        ntptime.settime()  
        return utime.time() * 1000  
    except:
        return 0 

def hardReset():
    global client
    if client is None:
        print("MQTT client not initialized. Cannot publish hard reset message.")
    else:
        try:
            payload = {"id": product_id}
            client.publish("onwords/hardReset", ujson.dumps(payload))
            print("Hard reset published to MQTT broker.")
        except Exception as e:
            print(f"Failed to publish hard reset message: {e}")

#publish devices state
def publish_state():
    global client
    global last_fan_speed, fan_state, R1, R2, R3
    if client:
        state = OrderedDict([
            ("device1", R1.value()),
            ("device2", R2.value()),
            ("device3", R3.value()),
            ("device4", fan_state),
            ("speed", last_fan_speed)
        ])
        client.publish(TOPIC_CURRENT_STATUS, ujson.dumps(state))
        print("Published state:", state)
    else:
        print("MQTT client not connected!")
 
 
#publish Device log
def publish_deviceLog(device, state):
    global client
    global last_fan_speed, fan_state
    if client:
        log = {
            "id": product_id,
            "client_id": "Switch",
            "ip": network.WLAN(network.STA_IF).ifconfig()[0],
            "time_stamp": get_timestamp()
        }
        
        if device == "device4":
            log[device] = 1 if state else 0   
            log["speed"] = last_fan_speed      
        else:
            log[device] = state

        client.publish(TOPIC_DEVICE_LOG, ujson.dumps(log))
        print("log published:", log)
    else:
        print("mqtt client not connected")


#MQTT callback
def mqtt_callback(topic, msg):
    global last_fan_speed, fan_state, R1, R2, R3
    topic_str = topic.decode()
    print(f"Received from {topic_str}: {msg.decode()}")

    if topic_str == f"onwords/{product_id}/status":
        try:
            data = ujson.loads(msg)

            if "device1" in data and data["device1"] in [0, 1]:
                R1.value(data["device1"])

            if "device2" in data and data["device2"] in [0, 1]:
                R2.value(data["device2"])

            if "device3" in data and data["device3"] in [0, 1]:
                R3.value(data["device3"])
                
            if "device4" in data and data["device4"] in [0, 1]:
                if "speed" in data and 0 <= data["speed"] <= 5:
                    speed = data["speed"]
                    if speed == 1:
                        fan_speed1()
                    elif speed == 2:
                        fan_speed2()
                    elif speed == 3:
                        fan_speed3()
                    elif speed == 4:
                        fan_speed4()
                    elif speed == 5:
                        fan_speed5()
                    
                    if data["device4"] == 1:
                        fan_state = 1
                        print("Fan ON with speed", speed)
                    else:
                        fan_speed0()
                        fan_state = 0
                        print("Fan OFF but retain speed", speed)      
                    
                        last_fan_speed = speed
            
            publish_state()    
            save_device_states(R1.value(), R2.value(), R3.value(), fan_state, last_fan_speed)
                
        except ValueError as e:
            print("Error parsing JSON:", e)

    if topic_str == f"onwords/{product_id}/getCurrentStatus":
        try:
            publish_state()

        except ValueError as e:
            print("Error parsing JSON:", e)

    if topic_str == f"onwords/{product_id}/softReset":
        try:
            clear_wifi_credentials()
            state = {
                "status": True
            }
            client.publish(TOPIC_SOFTRST, ujson.dumps(state))
            time.sleep(5)
            machine.reset()

        except ValueError as e:
            print("Error:", e)
            
    if topic_str == f"onwords/{product_id}/storePid":
        try:
            data = ujson.loads(msg)
            if "pid" in data:
                store_pid(data["pid"])
                status_msg = ujson.dumps({"pid": data["pid"]})
                client.publish(TOPIC_PID, status_msg)
                print("restarting device now....")
                time.sleep(2)
                machine.reset()
                
        except Exception as e:
            print("Error in JSON or storing:", e)
            
    if topic_str == TOPIC_CREDENTIALS:
        try:
            data = ujson.loads(msg)
            ssid = data.get("ssid")
            password = data.get("password")
            
            if "ssid" and "password" in data:
                nvs.set_blob("wifi_ssid", ssid.encode())
                nvs.set_blob("wifi_password", password.encode())
                nvs.commit()
                print(f"WiFi credentials stored: SSID={ssid}, Password={password}")
                status_msg = ujson.dumps({"status": "success","ssid": data["ssid"], "password": data["password"]})
                client.publish(TOPIC_CREDENTIALS, status_msg)
                time.sleep(2)
                machine.reset()
        except Exception as e:
            print("Error in JSON or storing:", e)
                  
    if topic_str == f"onwords/{product_id}/firmware":
        try:
            data = ujson.loads(msg)
            if data.get("update") is True:
                server_ip = data.get("server")
                if not server_ip:
                    print("No server IP provided in payload.")
                    return

                from ota_update import get_local_version  
                current_version = get_local_version()

                print(f"OTA update trigger received. Server IP: {server_ip}")

                status_msg = ujson.dumps({
                    "status": "update_started",
                    "pid": product_id,
                    "version": current_version
                })
                client.publish(f"onwords/{product_id}/firmware", status_msg)

                import ota_update
                success = ota_update.ota_update_with_result(server_ip)

                if success:
                    updated_version = ota_update.get_local_version()
                    status_msg = ujson.dumps({
                        "status": "update_success",
                        "pid": product_id,
                        "version": updated_version
                    })
                else:
                    status_msg = ujson.dumps({
                        "status": "update_failed",
                        "pid": product_id,
                        "version": current_version
                    })

                client.publish(f"onwords/{product_id}/firmware", status_msg)
                time.sleep(3)

                if success:
                    print("OTA complete, rebooting now...")
                    machine.reset()

        except Exception as e:
            print("Failed to parse OTA command:", e)

#Connect MQTT
def connect_mqtt():
    global client
    global mqtt_connect
    try:
        client = MQTTClient(client_id=product_id, server=BROKER_ADDRESS, port=PORT, user=USERNAME, password=MQTT_PASSWORD, keepalive=MQTT_KEEPALIVE)
        client.set_callback(mqtt_callback)
        client.connect()
        S_Led.value(1)
        client.subscribe(TOPIC_STATUS)
        client.subscribe(TOPIC_GET_CURRENT_STATUS)
        client.subscribe(TOPIC_SOFTRST)
        client.subscribe(TOPIC_PID)
        client.subscribe(TOPIC_FIRMWARE)
        client.subscribe(TOPIC_CREDENTIALS)
        print(f"Subscribed to {TOPIC_STATUS}")
        print(f"Subscribed to {TOPIC_GET_CURRENT_STATUS}")
        print(f"Subscribed to {TOPIC_SOFTRST}")
        print(f"Subscribed to {TOPIC_PID}")
        print(f"Subscribed to {TOPIC_FIRMWARE}")
        print(f"Subscribed to {TOPIC_CREDENTIALS}")
        mqtt_client = 1 
        return client
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
        mqtt_client = 0
        return None

async def reconnect_mqtt(max_retries = 5):
    global client, mqtt_client
    global mqtt_listener_task, mqtt_keepalive_task
    print("Reconnecting to MQTT broker...")
    
    async with mqtt_reconnect_lock:
        if not wifi.isconnected():
            print("Wi-Fi not connected, skipping MQTT reconnect.")
            return
        
        for attempt in range(1 , max_retries + 1):
            
            try:
                if client:
                    try:
                        client.disconnect()
                    except:
                        pass  
                client = None 
                await asyncio.sleep(2)  

                print("Attempting MQTT reconnection...")
                new_client = MQTTClient(
                    client_id=product_id,
                    server=BROKER_ADDRESS,
                    port=PORT,
                    user=USERNAME,
                    password=MQTT_PASSWORD,
                    keepalive=MQTT_KEEPALIVE
                )
                new_client.set_callback(mqtt_callback)
                new_client.connect()
                new_client.subscribe(TOPIC_STATUS)
                new_client.subscribe(TOPIC_GET_CURRENT_STATUS)
                new_client.subscribe(TOPIC_SOFTRST)
                new_client.subscribe(TOPIC_PID)
                new_client.subscribe(TOPIC_FIRMWARE)
                print("Reconnected to MQTT broker")
                if mqtt_listener_task is not None:
                    mqtt_listener_task.cancel()
                if mqtt_keepalive_task is not None:
                    mqtt_keepalive_task.cancel()

                mqtt_listener_task = asyncio.create_task(mqtt_listener())
                mqtt_keepalive_task = asyncio.create_task(mqtt_keepalive())
                if new_client:
                    client = new_client
                    mqtt_client = 1
                    S_Led.value(1)
                    return True

            except Exception as e:
                print(f"Unexpected error in reconnect_mqtt(): {e}")
                client = None
                mqtt_client = 0
                S_Led.value(0)
                await asyncio.sleep(2)
                
        print("All MQTT reconnection attempts failed.")
        return False
            
           
async def mqtt_listener():
    global client, mqtt_client
    while True:
        try:
            if client:
                try:
                    client.check_msg()
                except Exception as e:
                    print("MQTT check_msg error:", e)
                    mqtt_client = 0
                    client = None
                    await reconnect_mqtt()
            else:
                print("MQTT client not available, trying to reconnect...")
                await reconnect_mqtt()
        except Exception as e:
            print("Critical error in mqtt_listener():", e)
        await asyncio.sleep_ms(10)
        
        

async def mqtt_keepalive():
    global client, mqtt_client
    while True:
        try:
            if client:
                try:
                    print("Sending MQTT PINGREQ")
                    client.ping()
                except Exception as e:
                    print("MQTT Keep-Alive failed:", e)
                    mqtt_client = 0
                    client = None
                    await reconnect_mqtt()
            else:
                print("MQTT client not available in keepalive, reconnecting...")
                await reconnect_mqtt()
        except Exception as e:
            print("Critical error in mqtt_keepalive():", e)
        await asyncio.sleep(MQTT_KEEPALIVE // 2)
        
        
def process_F1():
    global R1
    new_state = not R1.value()
    R1.value(new_state)
    print("switch 1 toggled")
    eeprom.write(0, bytes([R1.value()]))
    publish_state()
    publish_deviceLog("device1", new_state)
    
def process_F2():
    global R2
    new_state = not R2.value()
    R2.value(new_state)
    print("Switch 2 toggled")
    eeprom.write(1, bytes([R2.value()]))
    publish_state()
    publish_deviceLog("device2", new_state)
    

def process_F3():
    global R3
    new_state = not R3.value()
    R3.value(new_state)
    print("Switch 3 toggled")
    eeprom.write(2, bytes([R3.value()]))
    publish_state()
    publish_deviceLog("device3", new_state)
    
def process_F4():
    global fan_state, last_fan_speed
    fan_state = 1 if fan_state == 0 else 0
    print("switch 4 toggled")
    if fan_state == 1:
        restore_last_fan_speed()
    else:
        fan_speed0()
    eeprom.write(3, bytes([fan_state]))
    eeprom.write(4, bytes([last_fan_speed]))
    publish_state()
    publish_deviceLog("device4", fan_state)
       

def restore_last_fan_speed():
    global last_fan_speed
    if last_fan_speed == 1:
        fan_speed1()
    elif last_fan_speed == 2:
        fan_speed2()
    elif last_fan_speed == 3:
        fan_speed3()
    elif last_fan_speed == 4:
        fan_speed4()
    elif last_fan_speed == 5:
        fan_speed5()
        
        
def fan_speed0():
    R4.value(0)
    R5.value(0)
    R6.value(0)
    R7.value(0)

def fan_speed1():
    global last_fan_speed
    last_fan_speed = 1
    R4.value(0)
    R5.value(1)
    R6.value(0)
    R7.value(0)

def fan_speed2():
    global last_fan_speed
    last_fan_speed = 2
    R4.value(1)
    R5.value(1)
    R6.value(0)
    R7.value(0)

def fan_speed3():
    global last_fan_speed
    last_fan_speed = 3
    R4.value(1)
    R5.value(0)
    R6.value(1)
    R7.value(0)

def fan_speed4():
    global last_fan_speed
    last_fan_speed = 4
    R4.value(0)
    R5.value(1)
    R6.value(1)
    R7.value(0)

def fan_speed5():
    global last_fan_speed
    last_fan_speed = 5
    R4.value(0)
    R5.value(0)
    R6.value(0)
    R7.value(1) 

    
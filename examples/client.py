# Client to manage air raid alert map state
# Device: Raspberry Pi Pico W
# Create config.py file with the following structure:
#   WIFI_SSID = 'your wifi ssid'
#   WIFI_PASSWORD = 'your wifi password'
#   SERVER_URL = 'ws://air-raid-alerts-server-example.com/ws'
#   AUTH_KEY = 'API auth key'
# Create pinout.py file, example for Pico W model:
#   REGION_PIN_MAP = {
#      1: 0, # pin 1,    AR Crimea
#      2: 1, # pin 2,    Vinnytska oblast
#      3: 2, # pin 4,    Volynska oblast
#      4: 3, # pin 5,    Dnipropetrovska oblast
#      5: 4, # pin 6,    Donetska oblast
#      6: 5, # pin 7,    Zhytomyrska oblast
#      7: 6, # pin 9,    Zakarpatska oblast
#      8: 7, # pin 10,   Zaporizka oblast
#      9: 8, # pin 11,   Ivano-Frankivska oblast
#      10: 9, # pin 12,  Kyivska oblast
#      11: 10, # pin 14, Kirovohradska oblast
#      12: 11, # pin 15, Luhanska oblast
#      13: 12, # pin 16, Lvivska oblast
#      14: 13, # pin 17, Mykolaivska oblast
#      15: 14, # pin 19, Odeska oblast
#      16: 15, # pin 20, Poltavska oblast
#      17: 16, # pin 21, Rivnenska oblast
#      18: 17, # pin 22, Sumska oblast
#      19: 18, # pin 24, Ternopilska oblast
#      20: 19, # pin 25, Kharkivska oblast
#      21: 20, # pin 26, Khersonska oblast
#      22: 21, # pin 27, Khmelnytska oblast
#      23: 22, # pin 29, Cherkaska oblast
#      24: 26, # pin 31, Chernivetska oblast
#      25: 27, # pin 32, Chernihivska oblast
#    }
#
#   DISCONNECTED_GPIO = 28 # pin 34
import uasyncio as asyncio
import network
import gc
from machine import Pin
import json
import config # Do not forget to create config.py file
import pinout # Do not forget to create pinout.py file
import uwebsockets.client as websocket_client # use https://github.com/danni/uwebsockets

async def connect_to_wifi(ssid, password):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    while True:
        if not station.isconnected():
            print("Connecting to WiFi...")
            station.connect(ssid, password)
            await asyncio.sleep(10)
            if station.isconnected():
                print('WiFi Connection successful!')
                return
            else:
                print("Failed to connect to WiFi. Retrying...")
                gc.collect()
        else:
            return
        await asyncio.sleep(5)
        gc.collect()

def set_pin(pin_number, state):
    led = Pin(pin_number, Pin.OUT)
    led.on() if state else led.off()
    print("{} Pin: {}".format("\U0001F534" if state else "\U0001F7E2", pin_number))

def set_disconnected_pin(state):
    set_pin(pinout.DISCONNECTED_GPIO, state)

def update_map(active_regions):
    print('-----Map update!-----')
    for region, pin_number in pinout.REGION_PIN_MAP.items():
        state = region in active_regions
        set_pin(pin_number, state)

async def handle_server_message(message):
    set_disconnected_pin(False)
    update_map(json.loads(message))

async def websocket_communication(url, auth_key):
    while True:
        websocket = None
        try:
            websocket = websocket_client.connect(url)
            if not websocket:
                set_disconnected_pin(True)
                raise Exception("Failed to connect to the WebSocket server.")

            websocket.send(auth_key) # Send auth key as the first message to authorize

            while True:
                message = websocket.recv()
                if message:
                    await handle_server_message(message)
                    await asyncio.sleep(1)  # Prevent tight loop
                else:
                    print("Connection closed by the server.")
                    break
        except Exception as e:
            print("WebSocket error:", e)
            set_disconnected_pin(True)

        finally:
            if websocket:
                websocket.close()
            gc.collect()

        print("Attempting to reconnect in 5 seconds...")
        await asyncio.sleep(5)
        gc.collect()

async def main():
    while True:
        update_map([]) # Turn all LEDs off
        set_disconnected_pin(True)
        await connect_to_wifi(config.WIFI_SSID, config.WIFI_PASSWORD)
        await websocket_communication(config.SERVER_URL, config.AUTH_KEY)

if __name__ == "__main__":
    asyncio.run(main())

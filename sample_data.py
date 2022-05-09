from cmath import nan
from re import T
from websocket import create_connection
import sys
import json
import time
import keyboard
import math
import time

import websocket

class Drone:
    def __init__(self, id, alt, lat, long, pitch, roll, yaw, velocityX, velocityY, velocityZ):
        self.DroneId = id
        self.Altitude = alt
        self.Latitude = lat
        self.Longitude = long
        self.Pitch = pitch
        self.Roll = roll
        self.Yaw = yaw
        self.Compass = yaw
        self.VelocityX = velocityX
        self.VelocityY = velocityY
        self.VelocityZ = velocityZ

    def translate_in_direction(self, angle, force):
        angle = (angle + self.Yaw) % 360
        x = force * math.cos(math.radians(angle)) #lat
        y = force * math.sin(math.radians(angle)) #long
        self.Latitude += x
        self.Longitude += y
        self.VelocityX = round(1000000*x, 1)
        self.VelocityY = round(1000000*y, 1)
        
def close_connection():
    ws.close()

def send_data(ws:websocket):
    controll = False
    if (len(sys.argv) > 1):
        drone.DroneId = sys.argv[1]

    input_given = False
    previously_pressed = False
    sleepTime = 0.1
    force = 0.0000001 * (sleepTime / 0.02)
    altitudeForce = 0.02 * (sleepTime / 0.02)

    while True:
        jsonData = json.dumps(drone.__dict__)
        
        ws.send(jsonData)
        
        if keyboard.is_pressed('`'):
            if not previously_pressed:
                controll = not controll
                print(f"Input set to {controll}", flush=True)
                previously_pressed  = True
            time.sleep(sleepTime)
            continue
        
        previously_pressed = False

        if keyboard.is_pressed('esc'):
            ws.close()
            break

        if not controll:
            time.sleep(sleepTime)
            continue

        input_given = False
        if keyboard.is_pressed('d'):
            input_given = True
            print("D", end=" ")
            drone.translate_in_direction(90, force)
            drone.Roll = 30
        elif keyboard.is_pressed('a'):
            input_given = True
            print("A", end=" ")
            drone.translate_in_direction(-90, force)
            drone.Roll = -30
        else:
            drone.Roll = 0

        if keyboard.is_pressed('w'):
            input_given = True
            print("W", end=" ")
            drone.translate_in_direction(0, force)
            drone.Pitch = -30
        elif keyboard.is_pressed('s'):
            input_given = True
            print("S", end=" ")
            drone.translate_in_direction(180, force)
            drone.Pitch = 30
        else:
            drone.Pitch = 0

        if keyboard.is_pressed('shift'):
            input_given = True
            print("SHIFT", end=" ")
            drone.Altitude += altitudeForce
        elif keyboard.is_pressed('ctrl'):
            input_given = True
            print("CTRL", end=" ")
            drone.Altitude -= altitudeForce

        if keyboard.is_pressed('q'):
            input_given = True
            print("Q", end=" ")
            drone.Yaw = (drone.Yaw - 3) % 360
            drone.Compass = drone.Yaw
        elif keyboard.is_pressed('e'):
            input_given = True
            print("E", end=" ")
            drone.Yaw = (drone.Yaw + 3) % 360
            drone.Compass = drone.Yaw

        if input_given:
            print(' '*15, end='\r', flush=True)
        else:
            drone.VelocityY = 0
            drone.VelocityX = 0
            drone.VelocityZ = 0
        
        time.sleep(sleepTime)

def on_message(vs, msg:str):
    if msg.startswith("testdata"):
        print(msg)

ws = None
try:
    server = '147.229.14.181'
    if (len(sys.argv) > 2):
        server = sys.argv[2]
    ws = create_connection(f"ws://{server}:5555", on_message=on_message)
    altitude = 221.4
    yaw = 0
    latitude = 49.227227662057544
    longtitude = 16.59721346994562
    pitch = 0
    roll = 0
    drone = Drone('Drone0', altitude, latitude, longtitude, 0, 0, 0, 0, 0, 0)
except:
    print('Failed to connect')

if ws:
    try:
        send_data(ws)
    except KeyboardInterrupt:
        ws.close()
        sys.exit(0)
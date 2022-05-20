#!/usr/bin/env python3

"""
Noch einzufügen Empfang der GPS Koordinate
Drohne hebt ab
fliegt zur Zeilkoordinate (lat,long) auf 10m über dem Boden
und landet. 
Wenn unterwegs ein hinderniss in Flugrichtung auftaucht und näher als 3m kommt, stopp die Drohne. 
Nach 10 Sekunden landet sie. 
"""

import asyncio
import RPi.GPIO as GPIO
import time

from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw, PositionGlobalYaw)

lat = 49.032584
long = 9.318489

#GPIO Modus (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#GPIO Pins zuweisen
GPIO_TRIGGER_TOP = 23 #top sensor
GPIO_ECHO_TOP = 24
GPIO_TRIGGER_DOWN = 25 #bottom   sensor
GPIO_ECHO_DOWN = 12
GPIO_TRIGGER_LEFT = 16 #front left sensor
GPIO_ECHO_LEFT = 20
GPIO_TRIGGER_RIGHT =19  #front right sensor
GPIO_ECHO_RIGHT = 26
#Richtung der GPIO-Pins festlegen (IN / OUT)
GPIO.setup(GPIO_TRIGGER_TOP, GPIO.OUT)
GPIO.setup(GPIO_ECHO_TOP, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_DOWN, GPIO.OUT)
GPIO.setup(GPIO_ECHO_DOWN, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_LEFT, GPIO.OUT)
GPIO.setup(GPIO_ECHO_LEFT, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_RIGHT, GPIO.OUT)
GPIO.setup(GPIO_ECHO_RIGHT, GPIO.IN)

def distanz(triggerpin, echopin):
    # setze Trigger auf HIGH
    GPIO.output(triggerpin, True)

    # setze Trigger nach 0.01ms aus LOW
    time.sleep(0.00001)
    GPIO.output(triggerpin, False)

    StartZeit = time.time()
    StopZeit = time.time()

    # speichere Startzeit
    while GPIO.input(echopin) == 0:
        StartZeit = time.time()

    # speichere Ankunftszeit
    while GPIO.input(echopin) == 1:
        StopZeit = time.time()

    # Zeit Differenz zwischen Start und Ankunft
    TimeElapsed = StopZeit - StartZeit
    # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
    # und durch 2 teilen, da hin und zurueck
    distanz = (TimeElapsed * 34300) / 2

    return distanz
async def collision_prevention():
    while True:
        if distanz(GPIO_TRIGGER_LEFT, GPIO_ECHO_LEFT) < 3 or distanz(GPIO_TRIGGER_RIGHT, GPIO_ECHO_RIGHT) < 3:
            # stop drone on current position
            await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))
          

async def run():
    """ Does Offboard control using position NED coordinates. """

    drone = System()
    await drone.connect(system_address="serial:///dev/serial0:921600")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break

    print("-- Arming")
    await drone.action.arm()

    print("-- Setting initial setpoint")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return
    print("-- Takeoff")
    await drone.action.set_takeoff_altitude(3.5)
    await drone.action.takeoff()
    
    print("-- Go lat, long, -3.5m Down within global coordinate system")
    await drone.offboard.set_position_ned(PositionGlobalYaw(lat, long, -3.5, 0.0, AltitudeType(AGL)))
    
    await asyncio.sleep(10)

    await drone.action.land()

    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed with error code: {error._result.result}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
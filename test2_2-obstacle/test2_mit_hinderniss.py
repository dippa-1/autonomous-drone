from aiohttp import web
from mavsdk import *
#from mavsdk.offboard import (OffboardError, PositionNedYaw, PositionGlobalYaw)
from mavsdk.offboard import *


import asyncio
import RPi.GPIO as GPIO
import time

#GPIO Modus (BOARD / BCM)
#GPIO.setmode(GPIO.BCM)

#GPIO Pins zuweisen
#GPIO_TRIGGER_TOP = 23 #top sensor
#GPIO_ECHO_TOP = 24
#GPIO_TRIGGER_DOWN = 25 #bottom   sensor
#GPIO_ECHO_DOWN = 12
#GPIO_TRIGGER_LEFT = 16 #front left sensor
#GPIO_ECHO_LEFT = 20
#GPIO_TRIGGER_RIGHT =19  #front right sensor
#GPIO_ECHO_RIGHT = 26
#Richtung der GPIO-Pins festlegen (IN / OUT)
#GPIO.setup(GPIO_TRIGGER_TOP, GPIO.OUT)
#GPIO.setup(GPIO_ECHO_TOP, GPIO.IN)
#GPIO.setup(GPIO_TRIGGER_DOWN, GPIO.OUT)
#GPIO.setup(GPIO_ECHO_DOWN, GPIO.IN)
#GPIO.setup(GPIO_TRIGGER_LEFT, GPIO.OUT)
#GPIO.setup(GPIO_ECHO_LEFT, GPIO.IN)
#GPIO.setup(GPIO_TRIGGER_RIGHT, GPIO.OUT)
#GPIO.setup(GPIO_ECHO_RIGHT, GPIO.IN)

#def distanz(triggerpin, echopin):
    # setze Trigger auf HIGH
#    GPIO.output(triggerpin, True)

    # setze Trigger nach 0.01ms aus LOW
#    time.sleep(0.00001)
##    GPIO.output(triggerpin, False)

#    StartZeit = time.time()
##    StopZeit = time.time()

    # speichere Startzeit
#    while GPIO.input(echopin) == 0:
#        StartZeit = time.time()

    # speichere Ankunftszeit
#    while GPIO.input(echopin) == 1:
#        StopZeit = time.time()

    # Zeit Differenz zwischen Start und Ankunft
#    TimeElapsed = StopZeit - StartZeit
    # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
    # und durch 2 teilen, da hin und zurueck
#    distanz = (TimeElapsed * 34300) / 2

#    return distanz


async def root_post(request):
    print("got request")
    data = await request.json()
    print(data)
    if "lat" in data and "long" in data:
        lat = data["lat"]
        long = data["long"]
        await run(lat, long)
        return web.Response(text="Lat: " + str(data["lat"]) + ", Long: " + str(data["long"]))
    else:
        return web.Response(text="Incorrect data format")

async def run(lat, long):
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

    print("-- Setting maximum speed to 1")
    await drone.action.set_maximum_speed(1)

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
    #print("-- Takeoff")
    #await drone.action.takeoff()
    
    print("-- Go lat, long, -10m Down within global coordinate system")
    #await drone.offboard.set_position_global(PositionGlobalYaw(lat, long, -5.0, 0.0, AltitudeType(AGL)))
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -5.0, 0.0))
    await asyncio.sleep(5)
    await drone.offboard.set_position_ned(PositionNedYaw(5.0, 0.0, -5.0, 0.0))
    #while true:
     #   if distanz(GPIO_TRIGGER_LEFT, GPIO_ECHO_LEFT)<3 or distanz(GPIO_TRIGGER_RIGHT, GPIO_ECHO_RIGHT)<3:
      #      await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))
    await asyncio.sleep(5)
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -5.0, 0.0))
    await asyncio.sleep(25)


    #await drone.action.land()

    #print("-- Stopping offboard")
    #try:
    #    await drone.offboard.stop()
    #except OffboardError as error:
    #    print(f"Stopping offboard mode failed with error code: {error._result.result}")
        
#app = web.Application()
#app.add_routes([web.post('/', root_post)])
#web.run_app(app)        

async def collision_prevention():
    while True:
        if distanz(GPIO_TRIGGER_LEFT, GPIO_ECHO_LEFT) < 2 or distanz(GPIO_TRIGGER_RIGHT, GPIO_ECHO_RIGHT) < 2:
            await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))
            await drone.action.land()

            print("-- Stopping offboard")
            try:
                await drone.offboard.stop()
            except OffboardError as error:
                print(f"Stopping offboard mode failed with error code: {error._result.result}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    #loop.create_task(collision_prevention()) # DIESE ZEILE IST NEU
    loop.run_until_complete(run(49.0325917, 9.3185024))
    

#!/usr/bin/env python3

import asyncio
from mavsdk import System

lat = 49.0339625
long = 9.3177517
async def run():
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
            print("-- Global position state is good enough for flying.")
            break

    print("Fetching amsl altitude at home location....")
    async for terrain_info in drone.telemetry.home():
        absolute_altitude = terrain_info.absolute_altitude_m
        print("Abs altidude", absolute_altitude)
        break

    print("-- Arming")
    await drone.action.arm()

    print("-- Taking off")
    await drone.action.takeoff()

    await asyncio.sleep(5)
    # To fly drone 20m above the ground plane
    flying_alt = absolute_altitude + 10.0
    # goto_location() takes Absolute MSL altitude
    await drone.action.goto_location(lat, long, flying_alt, 0)
    
    await asyncio.sleep(30)
    
    await drone.action.land()

    while True:
        print("Staying connected, press Ctrl-C to exit")
        await asyncio.sleep(1)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())

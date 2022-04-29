from aiohttp import web
from mavsdk import System

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
            print("-- Global position state is good enough for flying.")
            break

    print("Fetching amsl altitude at home location....")
    async for terrain_info in drone.telemetry.home():
        absolute_altitude = terrain_info.absolute_altitude_m
        break

    print("-- Arming")
    #await drone.action.arm()

    print("-- Taking off")
    #await drone.action.takeoff()

    #await asyncio.sleep(1)
    # To fly drone 20m above the ground plane
    flying_alt = absolute_altitude + 20.0
    # goto_location() takes Absolute MSL altitude
    print(f"-- Flying to {lat}, {long}")
    #await drone.action.goto_location(lat, long, flying_alt, 0)

    while True:
        print("Staying connected, press Ctrl-C to exit")
        await asyncio.sleep(1)
	
app = web.Application()
app.add_routes([web.post('/', root_post)])

web.run_app(app)
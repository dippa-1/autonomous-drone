import requests
# import pycurl
import json
import time
import os

import asyncio
import websockets


BENCHMARK_TIME = 10
servers = {
    'http': 8000,
    'turbogears2': 8003,
    'bottle': 8007
}
WEBSOCKET_PORT = 8010
RESULTS_FILE = '/benchmarks/results.json'

def requests_benchmark(port: int):
    start = time.time()
    counter = 0

    while time.time() - start < BENCHMARK_TIME:
        r = requests.get(f"http://localhost:{port}")
        if r.status_code != 200:
            print("GET Error: status code is", r.status_code)
            exit()
        counter += 1

    return counter

async def websocket_request(results):
    async with websockets.connect(f"ws://localhost:{WEBSOCKET_PORT}") as websocket:
        start = time.time()
        counter = 0
        while time.time() - start < BENCHMARK_TIME:
            await websocket.send('')
            await websocket.recv()
            print('Received response')
            counter += 1
        results['websocket'] = counter
        with open(RESULTS_FILE, 'w') as file:
            json.dump(results, file)


if __name__ == "__main__":
    print("Requests client started.")

    results = {}
    for server in servers:
        requests_counter = requests_benchmark(servers[server])

        if os.path.exists(""):
            with open(RESULTS_FILE, 'r') as file:
                results = json.load(file)

        results['requests_' + server] = requests_counter
        with open(RESULTS_FILE, 'w') as file:
            json.dump(results, file)

    asyncio.run(websocket_request(results))

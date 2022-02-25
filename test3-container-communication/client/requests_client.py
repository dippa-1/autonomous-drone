import requests
# import pycurl
import json
import time
import os

BENCHMARK_TIME = 10
servers = {
    'http': 8000,
    # 'django': 8001,
    # 'flask': 8002,
    'turbogears2': 8003,
    # 'tornado': 8004,
    # 'sanic': 8005,
    # 'falcon': 8006,
    # 'bottle': 8007
}

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


if __name__ == "__main__":
    print("Requests client started.")

    results = {}
    for server in servers:
        requests_counter = requests_benchmark(servers[server])

        if os.path.exists("/benchmarks/results.json"):
            with open("/benchmarks/results.json", 'r') as file:
                results = json.load(file)

        results['requests_' + server] = requests_counter
        with open("/benchmarks/results.json", 'w') as file:
            json.dump(results, file)

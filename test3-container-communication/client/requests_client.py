import requests
import json

print("Req client: Hello world!")
r = requests.get("http://localhost:8000")
with open("/benchmarks/requests.json", 'w') as file:
    content = {
        'after_1_minute': r.content.decode('ascii')
    }
    json.dump(content, file)

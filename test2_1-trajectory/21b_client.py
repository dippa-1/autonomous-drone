import requests
import json

data = {
    "lat": 0.1245,
    "long": 1.234
}
r = requests.post('http://localhost:8000', data=json.dumps(data))

print(r.content.decode('utf-8'))

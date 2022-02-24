import requests

print("Req client: Hello world!")
r = requests.get("http://server:8000")
print(r.status_code, r.json())

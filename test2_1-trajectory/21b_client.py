# Code modified from https://stackoverflow.com/a/61765710/8086761
import requests
import json
import subprocess as sp
import re

accuracy = 3

pshellcomm = ['powershell']
pshellcomm.append('add-type -assemblyname system.device; '\
                  '$loc = new-object system.device.location.geocoordinatewatcher;'\
                  '$loc.start(); '\
                  'while(($loc.status -ne "Ready") -and ($loc.permission -ne "Denied")) '\
                  '{start-sleep -milliseconds 100}; '\
                  '$acc = %d; '\
                  'while($loc.position.location.horizontalaccuracy -gt $acc) '\
                  '{start-sleep -milliseconds 100; $acc = [math]::Round($acc*1.5)}; '\
                  '$loc.position.location.latitude; '\
                  '$loc.position.location.longitude; '\
                  '$loc.position.location.horizontalaccuracy; '\
                  '$loc.stop()' %(accuracy))

p = sp.Popen(pshellcomm, stdin = sp.PIPE, stdout = sp.PIPE, stderr = sp.STDOUT, text=True)
(out, err) = p.communicate()
out = re.split('\n', out)

data = {
    "lat": float(out[0]),
    "long": float(out[1])
}
data_str = json.dumps(data)

print("Sending", data_str)
r = requests.post('http://localhost:8000', data=data_str)
print("Got", r.content.decode('utf-8'))

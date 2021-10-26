import requests
import json

url = 'http://0.0.0.0:8000'
message = 'Hello world'

incoming_message = b''

json_message = json.dumps({
    "text": message,
    "user": "annoying_user",
    "message": "awesome_theme"
    }
    )
headers = {'Content-type': 'application/json'}
pipou = requests.post(url, headers = headers, data = incoming_message)

print(json.loads(pipou.text))

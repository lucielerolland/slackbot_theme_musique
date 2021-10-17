import requests
import json

# url = 'https://hooks.slack.com/services/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'
url = 'http://localhost:8888'
message = 'Hello world'

json_message = json.dumps({
    "text": message,
    "user": "annoying_user",
    "message": "awesome_theme"
    }
)
headers = {'Content-type': 'application/json'}
pipou = requests.post(url, headers = headers, data = json_message)

print(json.loads(pipou.text))
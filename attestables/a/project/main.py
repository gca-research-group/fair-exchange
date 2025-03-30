import json

import requests


def start_exchange():
    url = "http://localhost:5000/api/exchange/"

    response = requests.post(url)
    response.raise_for_status()

    with open("response.json", "w") as json_file:
        json.dump(response.json(), json_file, indent=4)


start_exchange()

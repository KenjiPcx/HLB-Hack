import json

import requests

API_URL = "https://api-inference.huggingface.co/models/limivan/bert-esg"
url = "https://huggingface.co/limivan/bert-esg"
API_TOKEN = "api_NyUsmLJdCTDdyjRIKxaSEigKVGRWZYRoIL"
headers = {"Authorization": f"Bearer {API_TOKEN}"}


def query(payload):
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))


data = query(
    """In fiscal year 2019, we reduced our comprehensive carbon footprint for the fourth
consecutive year—down 35 percent compared to 2015, when Apple’s carbon emissions
peaked, even as net revenue increased by 11 percent over that same period. In the past
year, we avoided over 10 million metric tons from our emissions reduction initiatives—like
our Supplier Clean Energy Program, which lowered our footprint by 4.4 million metric tons.

"""
)

print(data)

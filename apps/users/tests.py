import requests
import json

web_url = "http://127.0.0.1:8000"

def test_sms():
    url = "{}/code/".format(web_url)
    data = {
        "mobile": "181419099996096"
    }
    response = requests.post(url, json=data)
    print(json.loads(response.text))


if __name__ == "__main__":
    test_sms()
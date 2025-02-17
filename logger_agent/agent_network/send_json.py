from time import sleep
import requests
import json
import os

url = 'http://127.0.0.1:5000'
def post_json():
    sleep(10) #TODO ask the server for request to send
    try:
        with open("sample.json","r") as f:
            data = json.load(f)

        x = requests.post(url, json = data) ##send the data
        if x.status_code == 200:
            os.remove("sample.json") ##delate the file after sending
    except Exception as e:
        requests.post(url, json={"error": f"Unexpected error: {str(e)}"})

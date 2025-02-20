from time import sleep
import requests
import json
from config.config import json_path

url = 'http://127.0.0.1:5000'
def post_json():
    try:
        with open(json_path,"r") as f:
            data = json.load(f)

        x = requests.post(url, json = data) ##send the data
        if x.status_code == 200:
            with open(json_path,"r+") as f:
                current_json = json.load(f)
                f.seek(0)
                current_json["data"] = []
                json.dump(current_json, f, indent=2)
                f.truncate() 

    except Exception as e:
        requests.post(url, json={"error": f"Unexpected error: {str(e)}"})

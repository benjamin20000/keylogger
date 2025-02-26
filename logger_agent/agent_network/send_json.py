
from time import sleep
import requests
import json
from getmac import get_mac_address as gma 
from config.config import json_path

url = 'http://127.0.0.1:5000'

def post_json():
    mac_address = gma()  

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        x = requests.post(url, json=data)  #send data -> server
        
        if x.status_code == 200:
            with open(json_path, "r+", encoding="utf-8") as f:
                current_json = json.load(f)
                f.seek(0)

                if mac_address in current_json:
                    current_json[mac_address] = []  
                    
                json.dump(current_json, f, indent=2, ensure_ascii=False)
                f.truncate()  

    except Exception as e:
        requests.post(url, json={"error": f"Unexpected error: {str(e)}"})

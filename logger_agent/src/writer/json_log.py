from interface.writer_interface import WriterInterface
from datetime import datetime
from getmac import get_mac_address as gma
import json
import os
from config.config import json_path



class JsonLog(WriterInterface):
    def create_file(self):
        data = {gma(): []} 
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)#save Hebrew

    def write(self, new_dict: dict):
        mac_address = gma()  

        if not os.path.exists(json_path):
            self.create_file()

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                try:
                    current_json = json.load(f)
                except json.JSONDecodeError: 
                    current_json = {mac_address: []}
        except FileNotFoundError:  
            current_json = {mac_address: []}

        
        new_data_list = [
            {
                "window": key,
                "time": datetime.now().strftime('%Y-%m-%d %H:%M'),
                "data": value
            }
            for key, value in new_dict.items()
        ]

        
        if mac_address not in current_json:
            current_json[mac_address] = []  

        current_json[mac_address].extend(new_data_list)

        
        try:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(current_json, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"error witre to json: {e}")

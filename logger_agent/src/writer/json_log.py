from interface.writer_interface import WriterInterface
from datetime import datetime
from getmac import get_mac_address as gma
import json
import os
from config.config import json_path

class JsonLog(WriterInterface):
    def create_file(self):
        with open(json_path, "w") as f:
            data = {"mac_addres": gma(),"data":[]}
            json.dump(data, f, indent=2)
        
    def write(self, message):
        new_data = {"time": datetime.now().strftime('%Y-%m-%d %H:%M'),
                    "data": message}
        
        if not os.path.exists(json_path):
            self.create_file()

        try:
            with open(json_path,"r+") as f:
                current_json = json.load(f)
                current_json["data"].append(new_data)
                f.seek(0)
                json.dump(current_json, f, indent=2)
        except Exception as e:
            print(e)


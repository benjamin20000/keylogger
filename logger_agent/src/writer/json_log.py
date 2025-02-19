from interface.writer_interface import WriterInterface
from datetime import datetime
import json

class JsonLog(WriterInterface):
    def write(self, message):
        new_data = {"time": datetime.now().strftime('%Y-%m-%d %H:%M'),
                    "data": message}
        try:
            with open("agent_data.json", "r") as f:
                data = json.load(f) 
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
            
        data.append(new_data)
        with open("agent_data.json","w") as f:
            json.dump(data, f, indent=2)


        
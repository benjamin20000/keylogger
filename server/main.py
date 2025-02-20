from flask import Flask, Response, request
import json
import os 
app = Flask(__name__)

json_path = "data/server.json"
def create_json():
    with open(json_path, "w") as f:
            new_schema = {}
            json.dump(new_schema, f, indent=2)

@app.route('/', methods=['POST'])
def get_data():
    if not os.path.exists(json_path):
        create_json()
    incoming_json = json.loads(request.data.decode("utf-8"))
    with open(json_path, "r+") as f: 
        current_json = json.load(f)
        if incoming_json["mac_addres"] not in current_json:            
            current_json[incoming_json["mac_addres"]] = incoming_json["data"]
        else:
            current_json[incoming_json["mac_addres"]] += incoming_json["data"]
        f.seek(0)
        json.dump(current_json, f, indent=2)
        
             
    return Response('We recieved something…')

if __name__ == '__main__':
    app.run(debug=True)
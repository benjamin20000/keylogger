from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import json
import os 


app = Flask(__name__)
CORS(app)
script_dir =os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, "data", "server.json")
if not os.path.exists(os.path.dirname(json_path)):
    os.makedirs(os.path.dirname(json_path), exist_ok=True)

def create_json():
    with open(json_path, "w") as f:
            new_schema = {}
            json.dump(new_schema, f, indent=2)


@app.route('/', methods=['POST'])
def post_requ():
    if not os.path.exists(json_path):
        create_json()

    incoming_json = json.loads(request.data.decode("utf-8"))

    with open(json_path, "r+", encoding="utf-8") as f:  
        try:
            current_json = json.load(f)
        except json.JSONDecodeError:
            current_json = {}

        for mac_address, entries in incoming_json.items():  
            if mac_address not in current_json:
                current_json[mac_address] = []  
            
            current_json[mac_address].extend(entries)  

        f.seek(0)
        json.dump(current_json, f, indent=2, ensure_ascii=False)  
        f.truncate() 

    return Response('Data received and saved successfully.', status=200)


    
@app.route('/data', methods=['GET'])
def get_data():
    if not os.path.exists(json_path):
        return jsonify({"error": "Data file not found"}), 404

    with open(json_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return jsonify({"error": "Failed to decode JSON"}), 500

    return jsonify(data), 200



@app.route('/command', methods=['POST'])
def handle_command():
    try:
        command_data = request.get_json()
        mac = command_data.get('mac')
        command = command_data.get('command')
        user = command_data.get('user')

        if not mac or not command:
            return jsonify({"error": "Missing mac or command"}), 400

       
        with open(json_path, "r+", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}

            if mac not in data:
                data[mac] = []

           
            if command == "start_monitoring":
           
                message = f"Monitoring started for {mac} by {user}"
            elif command == "stop_monitoring":
               
                message = f"Monitoring stopped for {mac} by {user}"
            else:
                return jsonify({"error": "Unknown command"}), 400

            f.seek(0)
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.truncate()

        return jsonify({"message": message}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
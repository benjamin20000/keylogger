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



@app.route("/data", methods=['GET'])
def helloWorld():
    computer = request.args.get('computer')
    sDate = request.args.get('startDate')
    eDate = request.args.get('endDate')
    sTime = request.args.get('startTime')
    eTime = request.args.get('endTime')
    filterdData = get_filterd_data(computer,sDate,eDate,sTime,eTime)
    return jsonify(filterdData)




if __name__ == '__main__':
    app.run(debug=True)
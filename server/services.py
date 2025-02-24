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
    # print(incoming_json)
    with open(json_path, "r+") as f: 
        current_json = json.load(f)
        if incoming_json["mac_addres"] not in current_json:            
            current_json[incoming_json["mac_addres"]] = incoming_json["data"]
        else:
            current_json[incoming_json["mac_addres"]] += incoming_json["data"]
        f.seek(0)
        json.dump(current_json, f, indent=2)
    return Response('We recieved something…')

def get_filterd_data(computer,sDate,eDate,sTime,eTime): ##TODO implemnt this function
    with open(json_path,"r") as f:
        data = json.load(f)
    return data

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
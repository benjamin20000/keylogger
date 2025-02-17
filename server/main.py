from flask import Flask, Response, request
import json 
app = Flask(__name__)

@app.route('/', methods=['POST'])
def get_data():
    try:
        with open("server_data.json", "r") as f:
                data = json.load(f) 
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
            
    data.append(json.loads(request.data.decode("utf-8")))
    with open("server_data.json","w") as f:
            json.dump(data, f, indent=2)

    print('Recieved data: {}'.format(request.data))
    return Response('We recieved something…')

if __name__ == '__main__':
    app.run(debug=True)
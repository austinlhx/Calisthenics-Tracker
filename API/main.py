from flask import Flask, request
import os
from ML import main

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    return "Hello World!"

@app.route('/position-estimate', methods=['POST'])
def run_ML():
    output = request.get_json()
    print(output)
    return main.run(output['video_path'], output['exercise']) 

if __name__ == "__main__":
    environment_port = os.getenv("PORT", 5000)
    app.run(debug=True, host='0.0.0.0', port=environment_port)
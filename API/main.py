from flask import Flask, request, make_response
from flask_cors import CORS, cross_origin
import os

from ML import main

app = Flask(__name__)
cors = CORS(app, resources={r"/position-estimate": {"origins": "*"}})

@app.route('/', methods=['GET'])
def hello_world():
    return "Hello World!"

@app.route('/position-estimate', methods=['POST'])
def run_ML():
    output = request.get_json()
    print(output)
    response = main.run(output['video_path'], output['exercise']) 
    
    return response

if __name__ == "__main__":
    environment_port = os.getenv("PORT", 5000)
    app.run(debug=True, host='0.0.0.0', port=environment_port)
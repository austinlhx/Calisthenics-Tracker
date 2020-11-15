from flask import Flask
import os
import ML

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    return "Hello World!"

@app.route('/position-estimate', methods=['POST'])
def run_ML():
    ML.run()

if __name__ == "__main__":
    environment_port = os.getenv("PORT", 5000)
    app.run(debug=True, host='0.0.0.0', port=environment_port)
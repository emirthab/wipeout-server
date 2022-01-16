from pyngrok import ngrok
from flask import Flask
from src.http_server import app
import json

App = Flask(__name__)
App.register_blueprint(app)

NGROK_CONFIG_PATH = "./ngrokconfig.yml"
ngrok.connect(config_path=NGROK_CONFIG_PATH)

f = open("./server_config.json")
CONFIG = json.load(f)


if __name__ == "__main__":
    App.run(debug=True,port=CONFIG["http-server"]["port"],host=CONFIG["http-server"]["ip"])

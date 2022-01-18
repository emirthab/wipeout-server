import asyncio
from operator import indexOf
from src.websocket import server
import threading
from pyngrok import ngrok
import websockets
from flask import Flask
from src.http_server import app
from src.dc import bot
import logging
import click
import json
from src.logger import consoleLog
from src.input import Input
import requests
import time
#NGROK_CONFIG_PATH = "./ngrokconfig.yml"
#ngrok.connect(config_path=NGROK_CONFIG_PATH)

f = open("./server_config.json")
CONFIG = json.load(f)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def secho(text, file=None, nl=None, err=None, color=None, **styles):
    pass

def echo(text, file=None, nl=None, err=None, color=None, **styles):
    pass

click.echo = echo
click.secho = secho

def printLogo():
    logo = "\033[95m                                                   __      \n\
                __                                /\ \__ \n\
     __  __  __/\_\  _____      __    ___   __  __\ \ ,_\  \n\
    /\ \/\ \/\ \/\ \/\ '__`\  /'__`\ / __`\/\ \/\ \\ \ \/  \n\
    \ \ \_/ \_/ \ \ \ \ \L\ \/\  __//\ \L\ \ \ \_\ \\ \ \_ \n\
     \ \___x___/'\ \_\ \ ,__/\ \____\ \____/\ \____/ \ \__\ \n\
      \/__//__/   \/_/\ \ \/  \/____/\/___/  \/___/   \/__/ \n\
                       \ \_\                               \n\
                        \/_/                               \n \n\
    \033[92m www.github.com/emirthab/wipeout-server \n \
    \033[36mversion = 0.01a \033[0m \n \n"
    print(logo)

printLogo()

time.sleep(1)

async def start_websocket(handler, host, port):
    async with websockets.serve(handler, host, port) as s:
        consoleLog("WEBSOCKET","succ","Websocket started succesfully!")
        await s.wait_closed()

def threadWebsocket():
    try:
        consoleLog("WEBSOCKET","info","Trying to start websocket server...")
        asyncio.run(start_websocket(server, CONFIG["websocket"]["ip"], CONFIG["websocket"]["port"]))
    except Exception as exc:
        consoleLog("WEBSOCKET","err",str(exc))

def threadDiscord():
    try:
        consoleLog("DISCORDBOT","info","Trying to start Discord Bot...")
        bot.run(CONFIG["discord"]["token"])
    except Exception as exc:
        consoleLog("DISCORDBOT","err",str(exc))

def threadFlask():
    App = Flask(__name__)
    App.register_blueprint(app)
    consoleLog("HTTP","info","Trying to start http server...")
    try:
        if __name__ == "__main__":
            App.run(debug=False,port=CONFIG["http-server"]["port"],host=CONFIG["http-server"]["ip"])
    except Exception as exc:
        consoleLog("HTTP","err",str(exc))


threading.Thread(target=Input).start()

runFlask = threading.Thread(target=threadFlask)
runFlask.start()

runWebsocket = threading.Thread(target=threadWebsocket)
runWebsocket.start()

def testHttp():
    try:
        ip = "http://localhost:" if CONFIG["http-server"]["ip"] == "0.0.0.0" else "http://"+CONFIG["http-server"]["ip"]+":"
        url = ip+str(CONFIG["http-server"]["port"])+"/testconnection"
        req = requests.get(url).content
        if req == b"OK":
            consoleLog("HTTP","succ","HTTP web server started succesfully!")
        else:
            consoleLog("HTTP","err",str(req))
    except Exception as exc:
        consoleLog("HTTP","err",str(exc))

testHttp()

threadDiscord()



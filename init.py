import asyncio
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

App = Flask(__name__)
App.register_blueprint(app)

NGROK_CONFIG_PATH = "./ngrokconfig.yml"
ngrok.connect(config_path=NGROK_CONFIG_PATH)

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

runWebsocket = threading.Thread(target=threadWebsocket)
runWebsocket.start()

try:
    consoleLog("DISCORDBOT","info","Trying to start Discord Bot...")
    bot.run(CONFIG["discord"]["token"])
except Exception as exc:
    consoleLog("DISCORDBOT","err",str(exc))

if __name__ == "__main__":
    pass
    #App.run(debug=True,port=CONFIG["http-server"]["port"],host=CONFIG["http-server"]["ip"])




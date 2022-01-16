import time
import atexit

lastLogFile = ""

def inColor(text,color):
    if color == "blue":
        return("\033[94m"+text+"\033[0m")
    elif color == "cyan":
        return("\033[96m"+text+"\033[0m")
    elif color == "puple":
        return("\033[95m"+text+"\033[0m")
    elif color == "darkcyan":
        return("\033[36m"+text+"\033[0m")
    elif color == "green":
        return("\033[92m"+text+"\033[0m")
    elif color == "yellow":
        return("\033[93m"+text+"\033[0m")
    elif color == "red":
        return("\033[91m"+text+"\033[0m")
    elif color == "bold":
        return("\033[1m"+text+"\033[0m")

def consoleLog(logger,thread,log):
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    logger = inColor("["+logger+"]","yellow")

    if thread == "err":
        logger += inColor(" thread/ERROR","red")
    elif thread == "warn":
        logger += inColor(" thread/WARNING","purple")
    elif thread == "info":
        logger += inColor(" thread/INFO","blue")
    elif thread == "succ":
        logger += inColor(" thread/INFO","green")

    _log = current_time + " " + logger + " : " + log
    print(_log)
    global lastLogFile
    lastLogFile = lastLogFile + _log + "\n"

def exit_handler():
    consoleLog(inColor("[SERVER]","yellow") + inColor(" / Server thread/INFO","blue"),"Stopping server...")

def logSave():
    f = open("log.txt", "a")
    f.write(lastLogFile)
    f.close()

atexit.register(exit_handler)
    

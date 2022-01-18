import time
from datetime import date

replacer = ["\033[94m","\033[96m","\033[95m","\033[36m","\033[92m","\033[93m","\033[91m","\033[1m","\033[0m"]
today = date.today()
t1 = time.strftime("%H:%M:%S", time.localtime())
d1 = today.strftime("%d/%m/%Y")

def getTime():
    today = date.today()
    t1 = time.strftime("%H-%M-%S", time.localtime())
    d1 = today.strftime("%d-%m-%Y")
    Time = d1+"_"+t1
    return Time

t1 = getTime()

lastLogFile = ""

def inColor(text,color):
    if color == "blue":
        return("\033[94m"+text+"\033[0m")
    elif color == "cyan":
        return("\033[96m"+text+"\033[0m")
    elif color == "purple":
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
        logger += inColor(" thread/SUCCESS","green")
    else:
        logger += inColor(" "+thread,"bold")

    _log = current_time + " " + logger + " : " + log
    print(_log)
    global lastLogFile
    lastLogFile = lastLogFile + _log + "\n" 

def logSave():
    try:
        global lastLogFile
        for rep in replacer:
            lastLogFile = lastLogFile.replace(rep,"")
        t2 = getTime()
        f = open("./logs/"+ t1 + "__" + t2 +".txt", "a")
        f.write(lastLogFile)
        f.close()
    except Exception as exc:
        print(exc)


    

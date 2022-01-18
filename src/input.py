from src.logger import consoleLog, logSave
import os
import sys
import threading
import asyncio

availableCommands = ["exit","start ngrok","restart"]

def Input():
    val = ""
    while val == "":
        val = input("")
        print("\033[A                             \033[A") 
        if val != "":
            if val in availableCommands:

                if val == "restart":
                    os.system("python init.py")
                    os._exit(1)
                    
                consoleLog("SERVER",">",val)
            else:
                consoleLog("SERVER","err","Unknown Command!" + "("+val+")")
        if val != "exit":
            val = ""
        else:
            consoleLog("SERVER","warn","Stopping server...")
            logSave()
            os._exit(1)

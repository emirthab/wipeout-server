from src.logger import consoleLog , inColor
import threading
from src.dc import getAllRoles
import sqlite3 as sql
import json

connected = set()

conList = []
tokens = []
maxId = 0

db = sql.connect("database.sqlite",check_same_thread=False)
cur = db.cursor()
lock = threading.Lock()

f = open("./server_config.json")
CONFIG = json.load(f)


async def server(websocket, path):
    connected.add(websocket)
    try:
        async for message in websocket:
            msg = msg2eval(message)

            #send connection for get id                        
            if msg[0] == 1:
                global maxId ; maxId+=1 ; _id = maxId ; name = str(msg[1]) ; token = str(msg[2])
                if token in tokens:
                    output,newList = [],[]
                    try:
                        userId = getUserByName(name)[0][0]
                        dc_id = getDcIdFromUserId(userId)[0][0]
                        roles = getAllRoles(dc_id)
                        chatColor = chatColorPicker(roles)
                        chatIcon = chatIconPicker(roles)

                        conList.append( {
                        "id": _id,
                        "user_id" : userId,
                        "name": name,
                        "websocket" : websocket,
                        "dc_id": dc_id,
                        "dc_roles": roles,
                        "chat_color" : chatColor,
                        "chat_icon" : chatIcon
                        } )

                        print(conList)

                        consoleLog("SERVER","info",inColor("Player connected","green")+ " '"+name+"'")
                    except Exception as exc:
                        consoleLog("WEBSOCKET","err",exc)
                        consoleLog("SERVER","warn","User dc id is not linked. ID : "+str(_id))
                        
                    await websocket.send( str([2,str(_id)]) )                
                    #filter "websocket" key
                    for con in conList:                    
                        obj={} ; [obj.update({key:con[key]}) for key in con if key!="websocket"] and newList.append(obj)
                        output = [x for x in newList if x["id"] is not _id]
                    await websocket.send(str([4,output]))
                    #send other clients connecting info
                    for conn in connected:
                        if conn != websocket : await conn.send(str( [3,_id,name] ))
                else:
                    await websocket.send(str([16]))

            #player position
            elif msg[0] == 5:
                _id = msg[1] ; pos = str(msg[2]).replace("(","") ; _pos = pos.replace(")","")
                for conn in connected:
                    if conn != websocket : await conn.send(str( [6,_id,_pos] ))

            #Ping
            elif msg[0] == 8:
                await websocket.send(str([9]))
            
            #Player rotation
            elif msg[0] == 10:
                _id = msg[1] ; rot = str(msg[2]).replace("(","") ; _rot = rot.replace(")","")
                for conn in connected:
                    if conn != websocket : await conn.send(str( [11,_id,_rot] ))
            
            #Chat
            elif msg[0] == 12:
                _id = msg[1] ; data = str(msg[2]) ; name = ""
                data = data.replace("[","")
                data = data.replace("]","")
                for con in conList:
                    if con["id"] == _id : name = str(con["name"]) ; chatIcon = con["chat_icon"] ; chatColor = con["chat_color"]
                if data != "":
                    if chatColor is not None:
                        name = "[color=" + chatColor + "]" + name + "[/color]"
                    if chatIcon is not None:
                        name = "[img=16x16]res://assets/ui/chat-icons/"+ chatIcon +".png[/img] " + name
                    for conn in connected:
                        await conn.send(str( [13,name,data] ))

            #Player animations
            elif msg[0] == 14:
                for conn in connected:
                    if conn != websocket : await conn.send(str( [15,msg[1],msg[2]] ))
    finally:
        _id = None
        for con in conList:
            if con["websocket"] == websocket:
                _id = con["id"]
                name = con["name"]
                conList.remove(con)
                consoleLog("SERVER","info",inColor("Player disconnected","red")+ " '"+name+"'")

        connected.remove(websocket)


        for conn in connected:
            await conn.send(str( [7,_id] ))
    
def msg2eval(data):
    return eval(data.decode("utf_8"))

def getDcIdFromUserId(userID):
    sql = "SELECT discord_id FROM discord_id WHERE id = "+ str(userID)
    try:
        lock.acquire(True)
        cur.execute(sql)
        fetch = cur.fetchall()
        return fetch
    finally:
        lock.release()

def getUserByName(name):
    sql = "SELECT * FROM players WHERE name = '"+ name +"'"
    try:
        lock.acquire(True)
        cur.execute(sql)
        return cur.fetchall()
    finally:
        lock.release()

def chatColorPicker(roles):
    chatColorRoles = CONFIG["discord"]["chat_color_roles"]
    for chatColorRole in chatColorRoles:
        for role in roles:
            if str(role) == chatColorRole:
                color = chatColorRoles[chatColorRole]
                return color
    return None

def chatIconPicker(roles):
    chatIconRoles = CONFIG["discord"]["chat_icon_roles"]
    for chatIconRole in chatIconRoles:
        for role in roles:
            if str(role) == chatIconRole:
                icon = chatIconRoles[chatIconRole]
                return icon
    return None
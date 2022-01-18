import asyncio
import websockets

connected = set()

conList = []
maxId = 0

async def server(websocket, path):
    connected.add(websocket)
    try:
        async for message in websocket:
            msg = msg2eval(message)

            #send connection for get id                        
            if msg[0] == 1:
                global maxId ; maxId+=1 ; _id = maxId ; name = str(msg[1]) ;
                output,newList = [],[]
                conList.append( {
                    "id": _id,
                    "name": name,
                    "websocket" : websocket
                } )
                await websocket.send( str([2,str(_id)]) )                
                #filter "websocket" key
                for con in conList:                    
                    obj={} ; [obj.update({key:con[key]}) for key in con if key!="websocket"] and newList.append(obj)
                    output = [x for x in newList if x["id"] is not _id]
                await websocket.send(str([4,output]))
                #send other clients connecting info
                for conn in connected:
                    if conn != websocket : await conn.send(str( [3,_id,name] ))

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
                for con in conList:
                    if con["id"] == _id : name = str(con["name"])
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
                conList.remove(con)

        connected.remove(websocket)

        for conn in connected:
            await conn.send(str( [7,_id] ))
    
def msg2eval(data):
    return eval(data.decode("utf_8"))

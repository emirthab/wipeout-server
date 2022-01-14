import asyncio
from xmlrpc.client import MAXINT
import websockets
import time

connected = set()

conList = []
maxId = 0

async def server(websocket, path):
    print(websocket)
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
                print(msg)
                _id = msg[1] ; pos = str(msg[2]).replace("(","") ; _pos = pos.replace(")","")
                for conn in connected:
                    if conn != websocket : await conn.send(str( [6,_id,_pos] ))
            elif msg[0] == 8:
                await websocket.send(str([9]))

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

start_server = websockets.serve(server, "0.0.0.0", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
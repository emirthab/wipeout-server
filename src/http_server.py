#TR470006701000000051107194 Tufan Özyurt
from secrets import token_urlsafe
import sqlite3 as sql
import threading
from random import randint
from flask import Blueprint, request
from src.websocket import tokens

app = Blueprint("app",__name__)

db = sql.connect("database.sqlite",check_same_thread=False)
cur = db.cursor()
lock = threading.Lock()

@app.route("/testconnection")
def testConnection():
    try:
        return("OK")
    except Exception as exc:
        return(str(exc))

def execute(sql):
    try:
        lock.acquire(True)
        cur.execute(sql)
        db.commit()
    finally:
        lock.release()

execute("CREATE TABLE if not exists 'players' (id, name, password)")
execute("CREATE TABLE if not exists 'discord_id' (id, discord_id)")
execute("CREATE TABLE if not exists 'discord_code' (id, discord_code)")

@app.route("/login",methods=["POST"])
def login():
    content = request.json
    userName = content["name"]
    password = content["pass"]
    user =  getUserByName(userName)
    if len(list(user)) != 0:
        sql = "SELECT * FROM players WHERE name = '"+ userName +"'"
        try:
            lock.acquire(True)
            cur.execute(sql)
            fetch = cur.fetchall()[0]
            password_2 = fetch[2]
            playerID = fetch[0]
        finally:
            lock.release()
        if str(password) == str(password_2):
            fetch = getDcIdFromUserId(playerID)

            if len(list(fetch)) > 0:
                token = token_urlsafe(64)
                tokens.append(token)
                return {
                    "response":"OK",
                    "token": str(token)
                }
            else:
                return {"response":"Discordunuzu bağlayın."}
        else:
            return {"response":"Yanlış şifre ya da kullanıcı adı"}
    else:
        return {"response":"Yanlış şifre ya da kullanıcı adı"}

@app.route("/register",methods=["POST"])
def register():
    content = request.json
    print(content)
    userName = content["name"]
    password = content["pass"]
    user =  getUserByName(userName)
    if len(userName) > 3 and len(password) > 7:
        if len(list(user)) == 0:
            _id = getLastId("players")
            add = "INSERT INTO players VALUES ("+ str(_id) + ",'" +userName + "','" + password + "')"
            execute(add)
            code = randint(100000,999999)
            add = "INSERT INTO discord_code VALUES ("+ str(_id) + ", '" + str(code) + "')"
            execute(add)
            return {
                "response": "OK",
                "dc_code": str(code)
                }
        else:
            return {"response": "Kullanıcı adı zaten tanımlı.",}
    elif len(userName) < 4:
        return {"response":"Kullanıcı adı en az 4 karakter olmalı."}
    else:
        print(len(password))
        return {"response":"Şifre en az 8 karakter olmalı."}

def getUserByName(name):
    sql = "SELECT * FROM players WHERE name = '"+ name +"'"
    try:
        lock.acquire(True)
        cur.execute(sql)
        return cur.fetchall()
    finally:
        lock.release()

def getLastId(table_name):
    sqlid = "SELECT MAX(CAST(id AS INT )) FROM "+table_name+";"
    try:
        lock.acquire(True)
        cur.execute(sqlid)
        fetch = cur.fetchall()
    finally:
        lock.release()
        _id = fetch[0][0]
        
    if _id == None:
        _id = 0
    else:
        _id += 1
    return _id

def getDcIdFromUserId(userID):
    sql = "SELECT discord_id FROM discord_id WHERE id = "+ str(userID)
    try:
        lock.acquire(True)
        cur.execute(sql)
        fetch = cur.fetchall()
        return fetch
    finally:
        lock.release()
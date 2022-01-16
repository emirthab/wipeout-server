import sqlite3 as sql
import threading
from random import randint
from flask import Blueprint, request

app = Blueprint("app",__name__)

db = sql.connect("database.db",check_same_thread=False)
cur = db.cursor()
lock = threading.Lock()

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
    print("")

@app.route("/register",methods=["POST"])
def register():
    content = request.json
    userName = content["name"]
    password = content["pass"]
    user =  getUserByName(userName)
    if len(list(user)) == 0:
        _id = getLastId("players")
        add = "INSERT INTO players VALUES ("+ _id + "," +userName + "," + password + ")"
        execute(add)
        code = randint(100000,999999)
        add = "INSERT INTO discord_code VALUES ("+ _id + "," + code + ")"
        execute(add)
        return {
            "response": "OK",
            "dc_code": str(code)
            }
    else:
        return {"response": "username is already used",}

def getUserByName(name):
    sql = "SELECT * FROM users WHERE name = '"+ name +"'"
    try:
        lock.acquire(True)
        cur.execute(sql)
        fetch = cur.fetchall()
    finally:
        lock.release()
        return fetch

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

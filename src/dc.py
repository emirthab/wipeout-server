import discord
from src.logger import consoleLog
import json
import sqlite3 as sql
import threading
from src.logger import consoleLog
from discord.utils import get

intents = discord.Intents.default()
intents.members = True
bot = discord.Client(intents=intents)

f = open("./server_config.json")
DC_CONFIG = json.load(f)["discord"]

db = sql.connect("database.sqlite",check_same_thread=False)
cur = db.cursor()
lock = threading.Lock()

def execute(sql):
    try:
        lock.acquire(True)
        cur.execute(sql)
        db.commit()
    except Exception as exc:
        print(exc)
    finally:
        lock.release()

@bot.event
async def on_ready():
    getAllRoles(536467127750623233)
    consoleLog("DISCORDBOT","succ","Discord bot successfully started!")
    #channel = bot.get_channel(DC_CONFIG["code_channel"])
    #messagge = await channel.send('hello')
    #await messagge.add_reaction(emoji='🏃')

@bot.event
async def on_message(message):
    channel = bot.get_channel(DC_CONFIG["code_channel"])
    if message.channel == channel:
        member = message.author
        if not member.bot:
            await message.delete()
            sql = "SELECT * FROM discord_code WHERE discord_code = '"+ str(message.content) + "'"
            try:
                lock.acquire(True)
                cur.execute(sql)
                playerId = cur.fetchall()[0][0]
                add = "INSERT INTO discord_id VALUES ("+ str(playerId) + ", '" + str(member.id) + "')"
                cur.execute(add)
                db.commit()
            except Exception as exc:
                consoleLog("DİSCORD","warn",str("Discord code is invalid! / "+ str(member) + " : " +str(message.content)))
            finally:
                lock.release()

def getAllRoles(dcId):
    guild = bot.get_guild(DC_CONFIG["guild"])
    member = guild.get_member(int(dcId))
    arr = []
    roles = member.roles
    for role in roles:
        arr.append(role.id)
    return arr

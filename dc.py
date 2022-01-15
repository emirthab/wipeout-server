from multiprocessing.connection import Client
import discord
from pyngrok import ngrok

CONFIG_PATH = "./ngrokconfig.yml"

ngrok.connect(config_path=CONFIG_PATH)

TOKEN = 'OTMxNjI0Mjg0ODY5MjMwNTky.YeHIug.PiRG44WiOI5OP3gWsWXLnxqjkRQ'
GUILD = '931623089459048469'

bot = discord.Client()

guild = bot.get_guild(931623089459048469)

@bot.event
async def on_ready():
    channel = bot.get_channel(931623090046238741)
    messagge = await channel.send('hello')
    message = await channel.fetch_message(931641780523368459)
    await messagge.add_reaction(emoji='🏃')

@bot.event
async def on_message(message):
    channel = bot.get_channel(931623090046238741)
    if message.channel == channel:
        member = message.author
        if not member.bot:
            await channel.send(member.id)
            await message.delete()

        
bot.run(TOKEN)
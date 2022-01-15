import discord
from pyngrok import ngrok

CONFIG_PATH = "./ngrokconfig.yml"

ngrok.connect(config_path=CONFIG_PATH)


TOKEN = 'OTMxNjI0Mjg0ODY5MjMwNTky.YeHIug.RaBG_Ep6rFaaZ1lc8Ck0djp0398'
GUILD = '931623089459048469'

bot = discord.Client()

@bot.event
async def on_ready():
    channel = bot.get_channel(931623090046238741)
    messagge = await channel.send('hello')
    message = await channel.fetch_message(931641780523368459)
    await messagge.add_reaction(emoji='🏃')

@bot.event
async def on_reaction_add(reaction, user):
    channel = bot.get_channel('931623090046238741')
    if reaction.message.channel.id != channel:
      return
    if reaction.emoji == "🏃":
      await reaction.message.channel.send("asd")

        
bot.run(TOKEN)
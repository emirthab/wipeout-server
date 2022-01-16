import discord
from src.logger import consoleLog

bot = discord.Client()

@bot.event
async def on_ready():
    consoleLog("DISCORDBOT","succ","Discord bot successfully started!")
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
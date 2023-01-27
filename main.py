import os
import platform
import discord
from discord.ext import commands
from globals import TOKEN, cmdPrefix, ownerId

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=cmdPrefix, owner_id=ownerId, intents=intents) #Creates the bot object

#Loads all cogs from the 'cogs' folder
def loadExtensions():
    initial_extensions = []
    for fileName in os.listdir('./cogs'):
        if fileName.endswith('.py'):
            initial_extensions.append('cogs.' + fileName[:-3])
    if __name__ == '__main__':
        for extension in initial_extensions:
            bot.load_extension(extension)

def main():
    loadExtensions()
    bot.run(TOKEN) #Starts the bot

@bot.event
#Changes the bot's rich presence and prints a console message on startup
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='twitch.tv/xijon | ?help'))
    print(f'Logged in as {bot.user.name}#{bot.user.discriminator}')
    print(f'Python version {platform.python_version()}')
    print(f'Discord.py version {discord.__version__}')

#Universal error handler
# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.CommandNotFound):
#         return
#     if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.send(f'Invalid argument. Type `{cmdPrefix}help` to see the correct usage.'); return
#     await ctx.send(f'`{str(error)}`')

#Another, simpler error handler
# @bot.event
# async def on_error(ctx, error):
#     print(str(error))

if __name__ == '__main__':
    main()
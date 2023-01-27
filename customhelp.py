import discord
from discord.ext import commands

def createEmbed():
    embed = discord.Embed(title='Bot Commands')

class CustomHelp(commands.HelpCommand):

    def __init__(self, bot):
        self.bot = bot

    async def send_bot_help(self, mapping):
        for cog in mapping:
            await self.get_destination()
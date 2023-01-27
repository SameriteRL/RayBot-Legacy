import discord
from discord.ext import commands
from globals import chatbotChannels
import random

input_words = open('cogs/input_words.txt').read().strip().split('\n')
response_list = open('cogs/responses.txt').read().strip().split('\n')

class Chatbot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener('on_message')
    async def reply(self, message):
        for word in input_words:
            if word in message.content.lower():
                await message.channel.send(random.choice(response_list))
                break

def setup(bot):
    # bot.add_cog(Chatbot(bot))
    pass
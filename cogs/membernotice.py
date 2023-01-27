import discord
from discord.ext import commands
from globals import welcomeGuilds

class MemberNotice(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    #When the bot joins a new server
    @commands.Cog.listener('on_guild_join')
    async def newGuidLog(self, guild):
        print(f'I\'ve joined a new server, {guild.name}, ID {guild.id}')
    
    #When someone joins the server
    @commands.Cog.listener('on_member_join')
    async def welcome(self, member):
        #If the member is in a notice enabled guild
        if member.guild.id in welcomeGuilds:
            channel = member.guild.system_channel #Fetches ID of the server's system channel
            #If a system channel exists
            if channel is not None:
                await channel.send(f'Welcome **{member.name}#{member.discriminator}** to the server!') #Sends a welcome message

    #When someone leaves the server
    @commands.Cog.listener('on_member_remove')
    async def dismissal(self, member):
        #If the member is in a notice enabled guild
        if member.guild.id in welcomeGuilds: 
            channel = member.guild.system_channel #Fetches ID of the server's system channel
            #If a system channel exists
            if channel is not None: 
                await channel.send(f'**{member.name}#{member.discriminator}** has left the server.') #Sends a dismissal message

def setup(bot):
    bot.add_cog(MemberNotice(bot))
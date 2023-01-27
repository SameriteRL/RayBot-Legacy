import discord
from discord.ext import commands

icup = 245729921320615946
coronacage = 689158341720801386

class AutoRole(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener('on_member_join')
    async def autoAssign(self, member):
        if member.guild.id == icup:
            role = member.guild.get_role(745853793647853608)
            await member.add_roles(role)
        elif member.guild.id == coronacage:
            role = member.guild.get_role(689169114945683485)
            await member.add_roles(role)

def setup(bot):
    bot.add_cog(AutoRole(bot))
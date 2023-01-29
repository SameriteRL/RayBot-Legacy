import discord
from discord.ext import commands
import random
# from moods import responses, rareResponses

#Filters strings so only lowercase letters remain
def letterOnly(message):
    return ''.join(filter(str.isalnum, message.content.lower()))

class OtherCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Ping pong!')
    async def ping(self, ctx):
        await ctx.send('Pong!')
    
    @commands.command(description='Flip a coin!', aliases=['flipcoin'])
    async def coinflip(self, ctx):
        coin = random.random() #Chooses a number between 0 and 1
        if coin <= 0.5:
            await ctx.send('Heads.') #Heads if between 0 to 0.5
        else:
            await ctx.send('Tails.') #Tails otherwise
    
    #To do: Add more info

    @commands.command()
    async def whois(self, ctx, member:discord.Member):
        embed = discord.Embed(title=f'{member.name}#{member.discriminator}', description=member.mention, colour=member.color) #Creates an embed with some info
        embed.set_thumbnail(url=member.avatar_url) #Adds the user's avatar to the embed
        #embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url) #Adds footer content to the embed
        embed.add_field(name='Created on:', value=member.created_at.strftime(r'%#m/%d/%Y at %#I:%M:%S %p')) #Adds a Created on: MM/DD/YYYY at HH::MM:SSSS field to the embed
        if (member.bot):
            embed.set_footer(text='This user is a bot.')
        if (member.system):
            embed.set_footer(text='This user is a Discord system account.')
        await ctx.send(embed=embed)
    
    @whois.error
    async def whois_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(f'Member \'{error.argument}\' not found. Is it spelled and capitalized correctly?')
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Enter a username.')
        else:
            print(str(error))
    
    @commands.command(description='Randomly chooses an integer within a specified interval.', aliases=['rand', 'random', 'randrange'])
    async def rng(self, ctx, min:int, max:int):
        if min >= max:
            await ctx.send('The lower bound must be less than the upper.')
        await ctx.send('{:,}'.format(random.randrange(min, max + 1)))
    
    @rng.error
    async def rng_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Enter two integers separated by a space.')
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Specify a start and end range.')
    
    # @commands.command(description='Ask about my current mood! I get mood swings a lot.', aliases=['feeling', 'moods'])
    # async def mood(self, ctx):
    #     if random.random() < 0.9:
    #         await ctx.send(responses[random.randrange(0, len(responses))])
    #     else:
    #         await ctx.send(rareResponses[random.randrange(0, len(rareResponses))])
    
    # @commands.command()
    # async def avatar(self, ctx, member:discord.Member):
    #     await ctx.send(member.avatar.url)
    
    # @avatar.error
    # async def avatar_error(self, ctx, error):
    #     if isinstance(error, commands.UserNotFound):
    #         await ctx.send(f'User \'{error.argument}\' not found. Is it spelled and capitalized correctly?')
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         await ctx.send('Enter a username.')
    #     else:
    #         print(str(error)

def setup(bot):
    bot.add_cog(OtherCommands(bot))
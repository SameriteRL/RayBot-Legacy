import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from globals import musicGuilds

class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(description='Disconnects me from a voice channel.', aliases=['disconnect', 'dc'])
    async def leave(self, ctx):
        #If the bot is in a voice channel
        if ctx.voice_client is not None:
            #If the user is not in a voice channel or isn't in the same channel as the bot
            if ctx.author.voice is None or ctx.author.voice.channel != ctx.voice_client.channel:
                await ctx.send('You\'re not in my voice channel.')
            #If the user is in the same voice channel as the bot
            else:
                await ctx.voice_client.disconnect()
                await ctx.message.add_reaction('✅')
        #If the bot is not in a voice channel
        else:
            await ctx.send('I\'m not in a voice channel.')
    
    @commands.command(description='Moves me to a specified person\'s call, or yours if no one is specified.', aliases=['moveto'])
    async def move(self, ctx, *members:discord.Member):
        #If the bot is not in a voice channel
        if ctx.voice_client is None:
            await ctx.send('I\'m not in a voice channel.')
        #If more than one member is specified
        elif len(members) > 1:
            raise commands.CommandInvokeError #Returns an error
        #If no members are specified
        elif len(members) < 1:
            #If the user is not in a voice channel
            if ctx.author.voice is None:
                await ctx.send('You\'re not in a voice channel.')
            #If the user is in a voice channel
            else:
                #If the user and bot are already in the same channel
                if ctx.author.voice.channel == ctx.voice_client.channel: 
                    await ctx.send('We\'re already in the same channel.')
                #If both the user and bot are in a voice channel but not the same one
                else: 
                    voiceChannel = ctx.author.voice.channel
                    await ctx.voice_client.move_to(voiceChannel) #Moves the bot to the user
                    await ctx.message.add_reaction('✅')
        #If a member is specified in the command
        else: 
            #If the specified user is not in a voice channel
            if members[0].voice is None: 
                await ctx.send(f'{members[0].name} isn\'t in a voice channel.')
            else:
                #If the specified user and bot are already in the same channel
                if members[0].voice.channel == ctx.voice_client.channel: 
                    await ctx.send(f'I\'m already in the same channel as {members[0].name}.')
                #If both the user and bot are in a voice channel but not the same one
                else:
                    voiceChannel = members[0].voice.channel
                    await ctx.voice_client.move_to(voiceChannel) #Moves the bot to the user
                    await ctx.message.add_reaction('✅')

    #To do: Use **kwargs instead to only allow for one argument max
    
    @move.error
    async def move_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Only specify one person, or none.')
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(f'User \'{error.argument}\' not found. Is it spelled and capitalized correctly?')
        else:
            print(str(error))
    
    @commands.command(description='Pauses the currently playing audio.')
    async def pause(self, ctx):
        #If the bot is not in a voice channel
        if ctx.voice_client is None:
            await ctx.send('I\'m not in a voice channel.')
        #If the user is not in a voice channel or isn't in the same channel as the bot
        elif ctx.author.voice is None or ctx.author.voice.channel != ctx.voice_client.channel:
            await ctx.send('You\'re not in my voice channel.')
        #If the correct conditions are met
        else:
            #If the audio is already paused
            if ctx.voice_client.is_paused():
                await ctx.send('I\'m already paused.')
            #If audio is playing
            else:
                ctx.voice_client.pause() #Pauses the currently playing audio
                await ctx.message.add_reaction('✅')
    
    @commands.command(description='Resumes the currently paused audio.')
    async def resume(self, ctx):
        #If the bot is not in a voice channel
        if ctx.voice_client is None:
            await ctx.send('I\'m not in a voice channel.')
        #If the user is not in a voice channel or isn't in the same channel as the bot
        elif ctx.author.voice is None or ctx.author.voice.channel != ctx.voice_client.channel:
            await ctx.send('You\'re not in my voice channel.')
        #If the correct conditions are met
        else:
            #If the audio is already playing
            if ctx.voice_client.is_playing():
                await ctx.send('I\'m already playing audio.')
            #If audio is paused
            else:
                ctx.voice_client.resume() #Resumes the paused audio
                await ctx.message.add_reaction('✅')
    
    @commands.command(description='Play from a selection of audio files I have saved. I currently don\'t support streaming YouTube or Spotify songs.')
    async def play(self, ctx, name:str):
        #If the command is used in a music enabled guild
        if ctx.guild.id in musicGuilds: 
            #If the user is not in a voice channel
            if ctx.author.voice is None: 
                voice = await ctx.send('You\'re not in a voice channel.')
            #If the bot is already connected to a voice channel
            elif ctx.voice_client is not None:
                #If the bot is playing audio or is paused
                if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
                    await ctx.send('Disconnect me first if you want to play a different track.')
                #If the bot is not playing anything and isn't paused
                else:
                    await ctx.send('Disconnect me then use the command again.')
            #If the user is in a voice channel
            else:
                voiceChannel = ctx.author.voice.channel
                #If the bot isn't in a voice channel
                if ctx.voice_client is None: 
                    voice = await voiceChannel.connect() #Connects to the channel
                #If the user and bot are in the same voice channel
                elif ctx.voice_client.channel == ctx.author.voice.channel: 
                    voice = ctx.voice_client
                #If both the user and bot are in voice channels but not the same one
                else: 
                    await ctx.send('You\'re not in my voice channel.')
                    return
                source = FFmpegPCMAudio(f'{name}.mp3')
                voice.play(source) #Plays the audio
                await ctx.message.add_reaction('✅')
        else:
            await ctx.send('This server isn\'t authorized for voice functions. Contact the bot owner for help.')

    @play.error
    async def play_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Specify the audio to play. `goodmood` and `ghibli` are currently available.')
        if isinstance(error, commands.BadArgument):
            await ctx.send('I don\'t have an audio file with that name.')
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('I\'m already playing audio.')
        else:
            print(str(error))

def setup(bot):
    bot.add_cog(Music(bot))
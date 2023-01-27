import discord
from discord.ext import commands
from globals import delDelay, ownerId, filterGuilds

#Loads a file with words to filter from chat
data = open('forbidden/nonono/forbiddenwords.txt'); badWords = data.read().replace('\n', '').split(','); data.close()

#Checks if a message author has the 'Manage Messages' permission or is the bot owner
def hasManageMessages(ctx):
    return ctx.message.author.roles[-1].permissions.manage_messages or ctx.message.author.id == ownerId

#Checks if a message author has the 'Manage Roles' permission or is the bot owner
def hasManageRoles(ctx):
    return ctx.message.author.roles[-1].permissions.manage_roles or ctx.message.author.id == ownerId

#Checks if a message author has the 'Kick Members' permission or is the bot owner
def hasKickMembers(ctx):
    return ctx.message.author.top_role.permissions.kick_members or ctx.message.author.id == ownerId

#Filters strings so only lowercase letters remain
def letterOnly(message):
    return ''.join(filter(str.isalnum, message.content.lower()))

class ModeratorTools(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    # @commands.Cog.listener('on_message')
    # async def saul(self, message):
    #     if message.author == self.bot.user:
    #         return #Bot ignores messages from itself
    #     #If the message is in a list of guilds to filter
    #     if message.guild.id in filterGuilds: 
    #         for word in badWords:
    #             #If someone uses a 'bad word'
    #             if word in letterOnly(message): 
    #                 print(message.author.name)
    #                 await message.delete() #Deletes the message with the word
    #                 await message.channel.send(file=discord.File('saul.png')) #Sends a picture of Saul
    
    @commands.command(description='Delete the last n number of messages in the channel.', aliases=['purge'])
    @commands.check(hasManageMessages) #Checks the sender's permissions
    async def clear(self, ctx, num:int):
        await ctx.channel.purge(limit=num + 1) #Deletes the specified number of messages prior to the command, and the command
        await ctx.send(f'{num} message(s) cleared.', delete_after=delDelay) #Confirmation message
    
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            await ctx.send('Enter a valid integer.')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('You don\'t have the \'Manage Messages\' permission.')
        elif isinstance(error, commands.CommandInvokeError):
            error = error.original
            if isinstance(error, (discord.errors.HTTPException, discord.HTTPException)):
                await ctx.send('I don\'t have the \'Manage Messages\' permission.')
    
    @commands.command(description='Assigns one or more roles to a member. Separate role names with a comma and space. Ex: ?addrole Joe role 1, role 2, role 3', aliases=['roleadd', 'assignrole', 'roleassign', 'assign'])
    @commands.check(hasManageRoles) #Checks the sender's permissions
    async def addrole(self, ctx, member:discord.Member=None, *, rolenames:str):
        converter = commands.RoleConverter()
        roles = [await converter.convert(ctx, name) for name in rolenames.split(', ')] #Converts the string argument into a list of role objects
        #Command target defaults to command invoker if no one is specified
        if member is None:
            member = ctx.author
        #Require one argument
        if len(roles) < 1:
            raise commands.UserInputError
        count = 0
        #If more than one role is specified
        if len(roles) > 1:
            for role in roles:
                if role in member.roles:
                    count += 1
            #If the user already has all roles specified in command
            if count == len(roles): 
                await ctx.send(f'{member.name} already has all these roles.')
            #If the user has one or more of the roles specified in command
            elif count > 0: 
                for role in roles:
                    await member.add_roles(role)
                await ctx.send(f'{member.name} already has one or more of these roles. The rest were added anyway.')
            #If the user has none of the roles specified in command
            else:
                for role in roles:
                    await member.add_roles(role)
                await ctx.send('Role(s) added.')
        #If only one role is specified in command
        else:
            #If the user already has the role
            if roles[0] in member.roles:
                await ctx.send(f'{member.name} already has this role.')
            #If the user doesn't already have the role
            else:
                for role in roles:
                    await member.add_roles(role)
                await ctx.send('Role(s) added.')

    @addrole.error
    async def addRole_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('You don\'t have the \'Manage Roles\' permission.')
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(f'User \'{error.argument}\' not found. Is it spelled and capitalized correctly?')
        elif isinstance(error, commands.RoleNotFound):
            await ctx.send(f'Role \'{error.argument}\' not found. Is it spelled and capitalized correctly?')
        elif isinstance(error, commands.CommandInvokeError):
            error = error.original
            if isinstance(error, (discord.errors.HTTPException, discord.HTTPException)):
                await ctx.send('I don\'t have the \'Manage Roles\' permission.')
        elif isinstance(error, commands.UserInputError):
            await ctx.send('Enter an optional username and at least one role.')
    
    @commands.command(description='Assign one or more roles to yourself. Separate role names with a comma and space. Ex: ?addrole Joe role 1, role 2, role 3', aliases=['roleself', 'selfassign', 'assignself'])
    @commands.check(hasManageRoles) #Checks the sender's permissions
    async def selfrole(self, ctx, *, rolenames:str):
        converter = commands.RoleConverter()
        roles = [await converter.convert(ctx, name) for name in rolenames.split(', ')]
        #Require one argument
        if len(roles) < 1:
            raise commands.UserInputError
        count = 0
        #If more than one role is specified
        if len(roles) > 1:
            for role in roles:
                if role in ctx.author.roles:
                    count += 1
            #If the user already has all roles specified in command
            if count == len(roles): 
                await ctx.send('You already have all these roles.')
            #If the user has one or more of the roles specified in command
            elif count > 0: 
                for role in roles:
                    await ctx.author.add_roles(role)
                await ctx.send('You already have one or more of these roles. The rest were added anyway.')
            #If the user has none of the roles specified in command
            else:
                for role in roles:
                    await ctx.author.add_roles(role)
                await ctx.send('Role(s) added.')
        #If only one role is specified in command
        else:
            #If the user already has the role
            if roles[0] in ctx.author.roles:
                await ctx.send('You already have this role.')
            #If the user doesn't already have the role
            else:
                for role in roles:
                    await ctx.author.add_roles(role)
                await ctx.send('Role(s) added.')

    @selfrole.error
    async def selfrole_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('You don\'t have the \'Manage Roles\' permission.')
        elif isinstance(error, commands.RoleNotFound):
            await ctx.send(f'Role \'{error.argument}\' not found. Is it spelled and capitalized correctly?')
        elif isinstance(error, commands.CommandInvokeError):
            error = error.original
            if isinstance(error, (discord.errors.HTTPException, discord.HTTPException)):
                await ctx.send('I don\'t have the \'Manage Roles\' permission.')
        elif isinstance(error, commands.UserInputError):
            await ctx.send('Enter at least one role to assign yourself.')
    
    @commands.command(description='Removes one or more roles from a member. Separate role names with a comma and space. Ex: ?delrole Joe role 1, role 2, role 3', aliases=['removerole', 'roledelete', 'deleterole', 'roledel', 'unassign'])
    @commands.check(hasManageRoles) #Checks the sender's permissions
    async def delrole(self, ctx, member:discord.Member=None, *, rolenames:str):
        converter = commands.RoleConverter()
        roles = [await converter.convert(ctx, name) for name in rolenames.split(', ')] #Converts the string argument into a list of role objects
        #Command target defaults to command invoker if no one is specified
        if member is None:
            member = ctx.author
        #Require one argument
        if len(roles) < 1:
            raise commands.UserInputError
        count = 0
        #If more than one role is specified
        if len(roles) > 1:
            for role in roles:
                if role not in member.roles:
                    count += 1
            #If the user is already missing all roles specified in command
            if count == len(roles): 
                await ctx.send(f'{member.name} is already missing all these roles.')
            #If the user is already missing one or more of the roles specified in command
            elif count > 0: 
                for role in roles:
                    await member.remove_roles(role)
                await ctx.send(f'{member.name} is already missing one or more of these roles. The rest were removed anyway.')
            else:
                for role in roles:
                    await member.remove_roles(role)
                await ctx.send('Role(s) removed.')
        #If only one role is specified in command
        else: 
            #If the member is already missing the role
            if roles[0] not in member.roles: 
                await ctx.send(f'{member.name} is already missing this role.')
            #If the member has the specified role
            else:
                for role in roles:
                    await member.remove_roles(role)
                await ctx.send('Role(s) removed.')
    
    @delrole.error
    async def delrole_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('You don\'t have the \'Manage Roles\' permission.')
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(f'User \'{error.argument}\' not found. Is it spelled and capitalized correctly?')
        elif isinstance(error, commands.RoleNotFound):
            await ctx.send(f'Role \'{error.argument}\' not found. Is it spelled and capitalized correctly?')
        elif isinstance(error, commands.CommandInvokeError):
            error = error.original
            if isinstance(error, (discord.errors.HTTPException, discord.HTTPException)):
                await ctx.send('I don\'t have the \'Manage Roles\' permission.')
        elif isinstance(error, commands.UserInputError):
            await ctx.send('Enter a username and at least one role.')
    
    @commands.command(description='Remove one or more roles from a specified person.', aliases=['unroleself', 'selfdelrole', 'delroleself'])
    @commands.check(hasManageRoles)
    async def selfunrole(self, ctx, *, rolenames:str):
        converter = commands.RoleConverter()
        roles = [await converter.convert(ctx, name) for name in rolenames.split(', ')]
        #Require one argument
        if len(roles) < 1:
            raise commands.UserInputError
        count = 0
        #If more than one role is specified
        if len(roles) > 1:
            for role in roles:
                if role not in ctx.author.roles:
                    count += 1
            #If the user already has all roles specified in command
            if count == len(roles): 
                await ctx.send('You\'re already missing all these roles.')
            #If the user has one or more of the roles specified in command
            elif count > 0: 
                for role in roles:
                    await ctx.author.remove_roles(role)
                await ctx.send('You\'re already missing one or more of these roles. The rest were removed anyway.')
            #If the user has none of the roles specified in command
            else:
                for role in roles:
                    await ctx.author.remove_roles(role)
                await ctx.send('Role(s) removed.')
        #If only one role is specified in command
        else:
            #If the user already has the role
            if roles[0] not in ctx.author.roles:
                await ctx.send('You\'re already missing this role.')
            #If the user doesn't already have the role
            else:
                for role in roles:
                    await ctx.author.remove_roles(role)
                await ctx.send('Role(s) removed.')

    @selfunrole.error
    async def selfunrole_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('You don\'t have the \'Manage Roles\' permission.')
        elif isinstance(error, commands.RoleNotFound):
            await ctx.send(f'Role \'{error.argument}\' not found. Is it spelled and capitalized correctly?')
        elif isinstance(error, commands.CommandInvokeError):
            error = error.original
            if isinstance(error, (discord.errors.HTTPException, discord.HTTPException)):
                await ctx.send('I don\'t have the \'Manage Roles\' permission.')
        elif isinstance(error, commands.UserInputError):
            await ctx.send('Enter at least one role to remove from yourself.')

    @commands.command(description='Removes all roles from yourself or a specified person.', aliases=['clearrole', 'roleclear', 'rolesclear', 'purgerole', 'purgeroles', 'rolepurge', 'rolespurge'])
    @commands.check(hasManageRoles)
    async def clearroles(self, ctx, member:discord.Member=None):
        #Command target defaults to command invoker if no one is specified
        if member is None:
            member = ctx.author
            #If the person has no roles aside from @everyone
            if len(ctx.author.roles) == 1:
                await ctx.send('You don\'t have any roles to remove.')
            else:
                roles = ctx.author.roles
                await member.remove_roles(*roles[1:])
                await ctx.send('Role(s) removed.')
        else:
            #If the person has no roles aside from @everyone
            if len(ctx.author.roles) == 1:
                await ctx.send(f'{member.name} doesn\'t have any roles to remove.')
            else:
                roles = ctx.author.roles
                await member.remove_roles(*roles[1:])
                await ctx.send('Role(s) removed.')
    
    @clearroles.error
    async def clearroles_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('You don\'t have the \'Manage Roles\' permission.')
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(f'User \'{error.argument}\' not found. Is it spelled and capitalized correctly?')
        elif isinstance(error, commands.CommandInvokeError):
            error = error.original
            if isinstance(error, (discord.errors.HTTPException, discord.HTTPException)):
                await ctx.send('I don\'t have the \'Manage Roles\' permission.')
    
    # Doesn't accept multiple words as the reason, disabled for now
    # @commands.command()
    # @commands.check(hasKickMembers)
    # async def kick(self, ctx, member:discord.Member, *, reason:str=None):
    #     message = ' '.join([reason.split(' ')]) #Idk if this works
    #     await member.kick(reason=message)
    #     await ctx.send(f'{member.name} kicked successfully.')
    
    # @kick.error
    # async def kick_error(self, ctx, error):
    #     if isinstance(error, commands.CheckFailure):
    #         await ctx.send('You don\'t have the \'Kick Members\' permission.')
    #     elif isinstance(error, commands.CommandInvokeError):
    #         error = error.original
    #         if isinstance(error, (discord.errors.HTTPException, discord.HTTPException)):
    #             await ctx.send('I don\'t have the \'Kick Members\' permission.')
    #     if isinstance(error, commands.MissingRequiredArgument):
    #        await ctx.send('Specify a user to kick.')

    # 2.0 Feature
    # @commands.command()
    # async def timeout(self, ctx, member:discord.Member, time:str):
    #     days=0; hours = 0; minutes = 0; seconds = 0
    #     splitTime = time.split()
    #     print(splitTime)
    #     for times in splitTime:
    #         if times.endswith('d'):
    #             days = [int(t) for t in times if t.isdigit()]
    #         elif times.endswith('h'):
    #             hours = [int(t) for t in times if t.isdigit()]
    #         elif times.endswith('m'):
    #             minutes = [int(t) for t in times if t.isdigit()]
    #         elif times.endswith('s'):
    #             seconds = [int(t) for t in times if t.isdigit()]
    #     await member.timeout(timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds))
    #     await ctx.send(f'{member.name} has been put in timeout for {days}D {hours}H {minutes}M {seconds}S.')

def setup(bot):
    bot.add_cog(ModeratorTools(bot))
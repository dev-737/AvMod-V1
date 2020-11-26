import discord
import ast
import random
import asyncio
import datetime
from discord.ext import commands
import asyncio

import cogs._json
def convert(time):
    pos = ["s","m","h","d","w"]

    time_dict = {"s" : 1, "m" : 60, "h" : 3600 , "d" : 3600*24, "w" : 3600*24*7}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2


    return val * time_dict[unit]

class moderation(commands.Cog, name="moderation"):


  def __init__(self, bot):
    self.bot = bot
    """    self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc2MTQxNDIzNDc2Nzg4NDMxOCIsImJvdCI6dHJ1ZSwiaWF0IjoxNjA1NTEzODIwfQ.gGVEavQ2R7ORhhzcu2dgzpEE1XwneOyvEQ2L6KmTooI' # set this to your DBL token"""


  """  @commands.Cog.listener()
  async def on_ready(self):
      print("Commands Cog has been loaded\n-----")"""

  

  @commands.command(aliases=['disconnect', 'close', 'stopbot'], hidden=True)
  @commands.is_owner()
  async def logout(self, ctx):
      """
      If the user running the command owns the bot then this will disconnect the bot from discord.
      """
      await ctx.send(f"Hey {ctx.author.mention}, I am now logging out :wave:")
      await self.bot.logout()

  @commands.command(hidden=True)
  @commands.is_owner()
  async def blacklist(self, ctx, user: discord.Member):
      """
      Blacklist someone from the bot
      """
      if ctx.message.author.id == user.id:
          await ctx.send("Hey, you cannot blacklist yourself!")
          return

      self.bot.blacklisted_users.append(user.id)
      data = cogs._json.read_json("blacklist")
      data["blacklistedUsers"].append(user.id)
      cogs._json.write_json(data, "blacklist")
      await ctx.send(f"Hey, I have blacklisted {user.name} for you.")

  @commands.command(hidden=True)
  @commands.is_owner()
  async def unblacklist(self, ctx, user: discord.Member):
      """
      Unblacklist someone from the bot
      """
      self.bot.blacklisted_users.remove(user.id)
      data = cogs._json.read_json("blacklist")
      data["blacklistedUsers"].remove(user.id)
      cogs._json.write_json(data, "blacklist")
      await ctx.send(f"Hey, I have unblacklisted {user.name} for you.")

  @commands.command(aliases=["setprefix"])
  @commands.has_permissions(administrator=True)
  @commands.cooldown(1, 5, commands.BucketType.guild)
  async def set_prefix(self, ctx, *, pre='!'):
      """
      Set a custom prefix for a guild
      """
      data = cogs._json.read_json('prefixes')
      data[str(ctx.message.guild.id)] = pre
      cogs._json.write_json(data, 'prefixes')
      await ctx.send(f"The guild prefix has been set to `{pre}`. Use `{pre}set_prefix <prefix>` to change it again!")

  @commands.command(hidden=True)
  async def leave(self,ctx):
      if ctx.author.id == 701727675311587358:
        await ctx.send('Whats the guild id?')
        iid = await self.bot.wait_for('message')
        iid_content=int(iid.content)
        toleave = self.bot.get_guild (iid_content)
        print (iid.content)
        await ctx.send (f'Ok, leaving that guild now!')
        print (iid.content)
        await toleave.leave()
        print (iid.content)
        
  @commands.command(hidden=True)
  async def name(self, ctx):
    await ctx.send('What is your name')
    name = await self.bot.wait_for('message')
    await ctx.send('Which Country do you live in')
    country = await self.bot.wait_for('message')
    await ctx.send(f'>>> Name: {name.content}\nCountry: {country.content}')


  @commands.command()
  @commands.has_permissions(kick_members=True)
  async def kick(self, ctx, member: discord.Member=None, *, reason="No Reason Provided."):

    """Kicks the mentioned member."""

    if not member:
      embed=discord.Embed(title="<a:ThonkSpin:771004484884889610> Syntax Error", description="Please ping or use the id of the member you want to kick.\n\nex.`.kick <@User> [reason]`/`.kick <ID> [Reason]`", color=discord.Colour.red())
      await ctx.send(embed=embed)
      return
    dont_message=True
    try:
      await member.kick(reason=f'Moderator: {ctx.author}\nReason: {reason}')            
      embed=discord.Embed(description=f"<a:pikadance:771004586886299648> {member} was kicked!")  
      await ctx.send(embed=embed)
    except discord.errors.Forbidden:
      await ctx.send("<:yikes:771264130430402591> Sorry, I do not have enough permissions to kick that member.")
      dont_message=False

    if dont_message==True:
      await member.send(f"<a:alarm:772727409764990989> You were kicked from **{ctx.guild.name}**.\n\nReason: **{reason}**")
    
    

  @commands.command(description="")
  @commands.has_permissions(ban_members=True)
  async def ban(self, ctx, member: discord.Member=None, *, reason="No Reason Provided."):

    """Bans the mentioned member."""

    if not member:
      embed=discord.Embed(title="<a:ThonkSpin:771004484884889610> Syntax Error", description="Please ping or use the id of the member you want to ban.\n\nex.`.ban <@User> [reason]`/`.ban <ID> [Reason]`", color=discord.Colour.red())
      await ctx.send(embed=embed)
      return
    dont_message=True
    try:
      await member.ban(reason=f'Moderator: {ctx.author}\nReason: {reason}')            
      embed=discord.Embed(description=f"<a:pikadance:771004586886299648> {member} was banned!")  
      await ctx.send(embed=embed)
    except discord.errors.Forbidden:
      await ctx.send("<:yikes:771264130430402591> Sorry, I do not have enough permissions to ban that member.")
      dont_message=False

    if dont_message==True:
      await member.send(f"<a:alarm:772727409764990989> You were banned from **{ctx.guild.name}**.\n\nReason: **{reason}**")


  @ban.error
  async def kick_error(self, ctx, error):
    if isinstance(error, commands.MemberNotFound):
        if len(ctx.args) == 2:
            await ctx.send("<a:wrong:765080446937202698> Sorry, I couldn't find that user.")
        else:
            await ctx.send("<a:wrong:765080446937202698> Sorry, I couldn't find that user.")

  @ban.error
  async def ban_error(self, ctx, error):
    if isinstance(error, commands.MemberNotFound):
        if len(ctx.args) == 2:
            await ctx.send("<a:wrong:765080446937202698> Sorry, I couldn't find that user.")
        else:
            await ctx.send("<a:wrong:765080446937202698> Sorry, I couldn't find that user.")

  @commands.command()
  @commands.has_permissions(manage_messages=True)
  @commands.cooldown(1, 5, commands.BucketType.member)
  async def purge (self, ctx, amount=None):

    """Deletes a number of messages you say it to."""

    async with ctx.channel.typing():
      if amount == None:
        embed=discord.Embed(colour=discord.Colour.red())
        embed.add_field(name="<a:wrong:764074894392033331> ERROR", value="```Please provide the amount of messages you want to delete.```")
        await ctx.send(embed=embed)
        return
      elif int(amount) <= 0:
        embed = discord.Embed(
        colour=discord.Colour.red()) 
        embed.add_field(name="<a:wrong:764074894392033331> ERROR", value="```Please provide a number more than 0.```") 
        await ctx.send(embed=embed)
        return

      elif int(amount) >= 101:
          await ctx.send ("You can only delete 100 messages at a time.")
      else:
          await ctx.channel.purge(limit=int(amount) + 1)
          await ctx.send(f"<a:correct:765080491669061633> I have purged {amount} message(s).")
          await asyncio.sleep(2)
          await ctx.channel.purge(limit=1)
      await self.bot.get_channel(771373935622750248).send(f'**{ctx.author}** purged **{amount}** of messages in **{ctx.guild}**')



  @commands.command()
  @commands.has_permissions(manage_channels=True)
  @commands.cooldown(1, 10, commands.BucketType.user)
  async def poll(self, ctx, *, question):

    """Creates a simple poll with 1 question, with a 'yes' or 'no' answer"""

    author=ctx.message.author
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title="Poll")
    embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
    embed.add_field(name="Question",value = question, inline=False)
    embed.set_footer(text=f'Poll By: {author}')
    message = await ctx.send(embed=embed)
    await message.add_reaction('<a:correct:765080491669061633>')
    await message.add_reaction('<:netural:770215518732550164>')
    await message.add_reaction('<a:wrong:765080446937202698>')


  @commands.command(pass_context=True, aliases=["changenick"])
  @commands.has_permissions(manage_nicknames=True)
  async def change_nick(self, ctx, member: discord.Member, *, nick):
    
    """Changes the NickName of the person you mention."""
    
    await member.edit(nick=nick)
    await ctx.send(f'Nickname was changed for {member.mention} ')

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def role(self, ctx, member: discord.Member, role: discord.Role):

    """Adds a role to the member you mention."""

    await member.add_roles(role)
    await ctx.send(f'Added {role} role to {member.mention}')

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def derole(self, ctx, member: discord.Member, role: discord.Role):

    """Removes a role from the member you mention."""

    await member.remove_roles(role)
    await ctx.send(f'Removed {role} role from {member.mention}')

  @commands.command(aliases=["ctc"])
  @commands.has_permissions(manage_channels=True)
  async def create_text_channel(self, ctx, name=None, category: discord.CategoryChannel=None):

    """Creates a text channel."""

    if not name:
      await ctx.send("***Please provide a name.***")
      return
    guild = ctx.guild
    await guild.create_text_channel(name=name, category=category)
    await ctx.send(f'Created text channel `{name}` in category `{category}`')


  @commands.command(aliases=["cvc"])
  @commands.has_permissions(manage_channels=True)
  async def createVC(self, ctx, name=None, category: discord.CategoryChannel=None):

    """Creates a voice channel."""

    if not name:
      await ctx.send("***Please provide a name.***")
      return
    guild = ctx.guild
    await guild.create_voice_channel(name=name, category=category)
    await ctx.send(f'Created text channel `{name}` in category `{category}`')

  @commands.command(description="Announces the message you provide. It doesn't ping @everyone or @here as it in in an embed.")
  @commands.has_permissions(manage_messages=True)
  async def announce(self, ctx,chan: discord.TextChannel=None, *, message=None):
    if not chan:
      embed=discord.Embed(title="<a:wrong:764074894392033331> Invalid Syntax", description="***Please mention the channel you would like to send this announcement to!***\n\n*Eg.`!announce <#channel> <announcement text>`*")
      await ctx.send(embed=embed)
      return
    elif not message:
      embed=discord.Embed(colour=discord.Colour.red())
      embed.add_field(name="<a:wrong:764074894392033331> Invalid Syntax", value=f"```Please provide a message to be announced.```\n\nEg. `!announce <#channel> <announcement text>`")
      await ctx.send(embed=embed)
      return
    else:
      await ctx.message.delete()
      embed=discord.Embed(timestamp=ctx.message.created_at, description=f"{message}")
      embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
      await chan.send(embed=embed) 
      await ctx.send(f"<a:correct:765080491669061633> Announcement sent to {chan.mention}")

  @commands.command(aliases=["direct", "dm"])
  @commands.has_permissions(manage_guild=True)
  async def dmuser(self, ctx, member: discord.Member,*, message=None):

    """DM's a usert"""

    embed=discord.Embed(description=message, color=discord.Colour.blue())
    embed.set_author(name=f'Message from {ctx.guild.name}', icon_url=ctx.guild.icon_url)
    embed.set_footer(text="Contact the staff or make a ticket if you have any questions/doubts. Thank You!")
    await member.send(embed=embed)
    await ctx.send(f"<:yeye:771234905543147530> I have DM'ed **{member}** for you!")


  @commands.command()
  @commands.has_permissions(ban_members=True)
  async def softban(self, ctx, user: discord.Member=None, reason=None):
      """Temporarily restricts access to the server."""
      
      if not user: # checks if there is a user
          return await ctx.send("You must specify a user")
      
      try: # Tries to soft-ban user
          await ctx.guild.ban(user, f"By {ctx.author} for {reason}" or f"By {ctx.author} for None Specified") 
          await ctx.guild.unban(user, "Temporarily Banned")
      except discord.Forbidden:
          return await ctx.send("Are you trying to soft-ban someone higher than the bot?")

  @commands.command()
  @commands.has_permissions(manage_channels=True)
  async def block(self, ctx, user: discord.Member=None):
      """
      Blocks a user from chatting in current channel.
      """
                              
      if not user: # checks if there is user
          return await ctx.send("You must specify a user")
                              
      await ctx.channel.set_permissions(user, send_messages=False) 
  
  @commands.command()
  @commands.has_permissions(manage_channels=True)
  async def lock(self, ctx, channel : discord.TextChannel=None):

    """Locks a channel."""

    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send('Channel locked.')

  @commands.command()
  @commands.has_permissions(manage_channels=True)
  async def unblock(self, ctx, user: discord.Member=None):

      """Unblocks a user from current channel"""
                              
      if not user: # checks if there is user
          return await ctx.send("You must specify a user")
      
      await ctx.channel.set_permissions(user, send_messages=True) # gives back send messages permissions


  @commands.command(aliases=["dtc", "deletechannel"] )
  @commands.has_permissions(manage_channels=True)
  async def delete_channel(self, ctx, chan: discord.TextChannel, *, reason=None):

    """Deletes a Text channel."""

    await chan.delete(reason=reason)
    await ctx.send(f'Deleted channel `{chan}` for reason `{reason}`')

  
  
  @commands.command(aliases=['changechannelname', 'ccn'])
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.has_permissions(manage_messages=True)
  async def change_channel_name(self, ctx,*, name : str=None):

    """Changes the channel name to the name you provide."""

    if not name:
      await ctx.send("***Please give a name to change this channel name to.***")
      return
    await ctx.channel.edit(name=name)
    await ctx.send(f"The channel name has been set to `{name}`")

  @commands.command()
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.has_permissions(manage_channels=True)
  async def slowmode(self, ctx, duration : int):

    """Changes the slowmode of the channel you are in."""

    if duration > 0:
        await ctx.channel.edit(slowmode_delay=duration)
        await ctx.send(f"Slowmode has been set to `{duration}s`")
    
    elif duration == 0:
        await ctx.channel.edit(slowmode_delay=duration)
        await ctx.send(f"Slowmode has been disabled.")


  @commands.command()
  async def unban(self, ctx, *, member):
    banned_members= await ctx.guild.bans()
    member_name, member_descriminator = member.split('#')

    for ban_entry in banned_members:
      user=ban_entry.user

      if (user.name, user.discriminator) == (member_name, member_descriminator):
        await ctx.guild.unban(user)
        await ctx.send(f"Unbanned {user}")


"""  @commands.command()
  @commands.has_permissions(manage_channels=True)
  async def clone(self, ctx, channel):
    if channel==None:
      channel=ctx.Channel
    name=ctx.channel_name

    await channel.clone(name=name)
    await ctx.send('Cloned channel!')"""

"""  @commands.command()
  async def avtest(self, ctx, user_id: int):
    voted= await self.get_user_vote(self.bot_id, user_id)
    if voted == True:
      await ctx.send("TEST SUCCESSFUL!")
    else:
      await ctx.send("In order for you to use this command, pls vote in https://top.gg/bot/763626077292724264")"""





def setup(bot):
    bot.add_cog(moderation(bot))
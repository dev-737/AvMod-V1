import discord
import platform
import re
import os
import asyncio
import random
import urllib.parse
import aiohttp
from PIL import Image, ImageFont,ImageDraw
import datetime
from discord.ext import commands

snipe_message_content = None
snipe_message_author = None
snipe_message_id = None
snipe_message_channel = None

class utility(commands.Cog, name='utility'):

  def __init__(self, bot):
            self.bot = bot

  @commands.command(aliases=['stat', 'info'])
  @commands.cooldown(1, 5, commands.BucketType.member)
  async def stats(self, ctx):

      """Show's the bots statistics."""

      pythonVersion = platform.python_version()
      dpyVersion = discord.__version__
      serverCount = len(ctx.bot.guilds)
      memberCount=len(set(ctx.bot.get_all_members()))
      embed = discord.Embed(colour=ctx.author.colour, timestamp=ctx.message.created_at)

      embed.add_field(name='<:AvMod2:770247678885625856> Bot Version ',      value=ctx.bot.version)
      embed.add_field(name='<:python:769448668348416010>Python Version ',   value=pythonVersion)
      embed.add_field(name='<:discord:769449385670737940>Discord.py Version ',value=dpyVersion)
      embed.add_field(name='<:server_boost:769450820076306443>Total Guilds ',      value=serverCount)
      embed.add_field(name="<:members:769449777472471060>Total Members",      value= memberCount)
      embed.add_field(name='<a:botdev_shine:769445361693491200>Developer', value='<@701727675311587358>')

      embed.add_field(name="Discord", value="[Click to join](https://discord.gg/eJrTyEX)")

      embed.add_field(name="<:invite:769450163671400459>Bot Invite", value="[Invite](https://discord.com/api/oauth2/authorize?client_id=761414234767884318&permissions=8&scope=bot)", inline=True )
      embed.set_author(name=f"{ctx.bot.user.name} Stats", icon_url=ctx.bot.user.avatar_url)
      embed.add_field(name="<:upvote:274492025678856192> Vote", value="[vote](https://top.gg/bot/761414234767884318)")
      await ctx.send(embed=embed)

  @commands.command(aliases=["say", "repeat"])
  @commands.has_permissions(manage_messages=True)
  async def echo(self, ctx, *, message=None):
        """
        A simple command that repeats the users input back to them.
        """
        message = message or "Please provide the message to be repeated."
        await ctx.message.delete()
        await ctx.send(message)

  @commands.command(aliases=["av", "pfp"])
  async def avatar(self, ctx,*, member: discord.Member):

    """A command used to show your avatar!"""

    embed=discord.Embed(color=discord.Colour.blurple())
    embed.set_author(name=member, icon_url=member.avatar_url)
    embed.set_image(url=f"{member.avatar_url}")
    await ctx.send(embed=embed)

  @avatar.error
  async def avatar_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      embed=discord.Embed(color=ctx.author.colour)
      embed.set_author(name=f"{ctx.author}'s avatar", icon_url=ctx.author.avatar_url )
      embed.set_image(url=f"{ctx.author.avatar_url}")
      await ctx.send(embed=embed)

  @commands.command(aliases=["whois", "wi", "ui"])
  @commands.cooldown(1, 10, commands.BucketType.user)
  async def userinfo(self, ctx, member: discord.Member=None):

    """Shows Info about a user."""

    member=ctx.author if not member else member

    roles=[role for role in member.roles if role != ctx.guild.default_role]


    embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)
    embed.set_author(name=f"User Info - {member}", icon_url=member.avatar_url)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)

    embed.add_field(name='<:info:769844372107427860> ID', value=member.id)
    embed.add_field(name=":name_badge: NickName", value=member.display_name)

    embed.add_field(name=f":roll_of_paper: Roles ({len(roles)})", value=" ".join([role.mention for role in roles]), inline=False) 
    embed.add_field(name=":roll_of_paper: Top Role", value=member.top_role.mention)

    embed.add_field(name="<:bot_tag:772392739722756097> Bot?", value=member.bot)

    embed.add_field(name=':calendar:Created At', value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)

    embed.add_field(name="Status", value=str(member.status))

    embed.add_field(name=":calendar:Member Joined At", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

    await ctx.send(embed=embed)

  """ 
 @commands.command(aliases=["server", "guildinfo", "si"])
  async def serverinfo(self, ctx):
    
    Shows Information about the server.

    roles=[role for role in ctx.guild.roles if role != ctx.guild.default_role]
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)

    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)

    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(
        title=name + " Server Information",
        description=description,
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=id, inline=True)
    embed.add_field(name=f":roll_of_paper: Roles:", value=f'**{len(roles)}**', inline=False)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name=':calendar:Created At', value=ctx.guild.created_at.strftime("%a, %#d/%B/%Y, %I:%M %p UTC"), inline=True )
    embed.add_field(name="Member Count", value=memberCount, inline=True)

    await ctx.send(embed=embed)"""

  @commands.command(aliases=["server", "guildinfo", "si"], description="Shows Information about the server.")
  async def serverinfo(self, ctx):
    roles=[role for role in ctx.guild.roles if role != ctx.guild.default_role]
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)

    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    boosts = ctx.guild.premium_subscription_count
    memberCount = str(ctx.guild.member_count)

    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(
        title=name + " Server Information",
        description=description,
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=icon)
    #embed.add_field(name="<a:owner_crown:774605327873212426> Owner", value="737Aviator!#0737", inline=True)
    embed.add_field(name="<a:owner_crown:774605327873212426> Owner", value=owner, inline=True)
    embed.add_field(name="<:info:763023967761858581> Server ID", value=id, inline=True)
    embed.add_field(name="<a:boost_evolve:769448461824163870> Boosts", value=f"{boosts} boosts", inline=True)
    embed.add_field(name=f"🧻 Roles", value=len(roles), inline=True)
    embed.add_field(name="🌍Region", value=region, inline=True)
    embed.add_field(name=':calendar:Created At', value=ctx.guild.created_at.strftime("%a, %#d/%B/%Y, %I:%M %p UTC"), inline=True)
    embed.add_field(name="<:members:769449777472471060> Member Count", value=memberCount, inline=True)

    await ctx.send(embed=embed)


  @commands.command()
  @commands.cooldown(1, 15, commands.BucketType.user)
  async def emojify(self, ctx, *, text: str):
        '''
        Converts the alphabet and spaces into emojis.
        '''
        emojified = ''
        formatted = re.sub(r'[^A-Za-z ]+', "", text).lower()
        if text == '':
            await ctx.send('Please say what text you want to be converted.')
        else:
            for i in formatted:
                if i == ' ':
                    emojified += '     '
                else:
                    emojified += ':regional_indicator_{}: '.format(i)
            if len(emojified) + 2 >= 2000:
                await ctx.send('Your message in emojis exceeds 2000 characters!')
            if len(emojified) <= 25:
                await ctx.send('Please only provide text.')
            else:
                await ctx.send('_ _'+emojified+'')


  @commands.command()
  async def invite(self, ctx):

    """Shows you the invite link to the bot."""

    await ctx.send('Here you go! <https://discord.com/api/oauth2/authorize?client_id=761414234767884318&permissions=8&scope=bot>')
  @commands.command()
  @commands.cooldown(1, 5, commands.BucketType.user)
  async def ping(self, ctx):

    """Shows AvMod's's ping'"""
    msg = await ctx.send("**Checking ping...**")
    await msg.edit(content=f'Pong! `{round(ctx.bot.latency * 1000)}ms`')



  @commands.command(aliases=["discord", "support"])
  async def supportserver(self, ctx):
    
    """Shows you AvMod support server!"""

    await ctx.send("https://discord.gg/eJrTyEX")


  @commands.command()
  @commands.cooldown(1, 30, commands.BucketType.user)
  async def vote(self, ctx):
    vote=discord.Embed(title="Vote Options", description="`1.` [TOP.GG](https://top.gg/bot/761414234767884318/vote)\n`2.` [DISCORD.BOTLIST](https://discordbotlist.com/bots/avmod/upvote)\n`3.` [DISCORD.BOATS](https://discord.boats/bot/761414234767884318/vote)")
    await ctx.send(embed=vote)

  @commands.command()
  async def suggest(self, ctx, *, suggestion):

    """Suggest something to be added/removed to the bot."""

    embed=discord.Embed(title="New Suggestion:", description=suggestion, color=ctx.author.color)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
    embed.set_footer(text=f"Suggestion by: {ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.bot.get_channel(765067272041267220).send(embed=embed)
    await ctx.send("Your suggestion has been sent to <#765067272041267220>, join the support server to view it. - https://discord.gg/eJrTyEX")


  @commands.command(helpinfo='Searches the web (or images if typed first)', aliases=['search'])
  async def google(self, ctx, *, searchquery: str):
    '''
    Googles searchquery, or images if you specified that
    '''
    searchquerylower = searchquery.lower()
    if searchquerylower.startswith('images '):
        await ctx.send('<https://www.google.com/search?tbm=isch&q={}>'
                       .format(urllib.parse.quote_plus(searchquery[7:])))
    else:
        await ctx.send('<https://www.google.com/search?q={}>'
                       .format(urllib.parse.quote_plus(searchquery)))
  
  @commands.command()
  async def wiki(self, ctx, *, message: str):
    await ctx.send('<https://en.m.wikipedia.org/wiki/{}>'
                       .format(urllib.parse.quote_plus(message)))
  


  @commands.command(description="Reverces the text you provide!!")
  async def reverse(self, ctx, *, msg):
    t_rev = msg[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
    await ctx.send(f"🔁 {t_rev}")




  @commands.Cog.listener()
  async def on_message_delete(self, message):

      global snipe_message_content
      global snipe_message_author
      global snipe_message_id
      global snipe_message_channel

      snipe_message_content = message.content
      snipe_message_author = message.author
      snipe_message_id = message.id
      snipe_message_channel = message.channel
      await asyncio.sleep(60)

      if message.id == snipe_message_id:
          snipe_message_author = None
          snipe_message_content = None
          snipe_message_id = None
          snipe_message_channel = None
      await self.bot.process_commands(message)

  @commands.command()
  @commands.guild_only()
  @commands.cooldown(1, 10, commands.BucketType.member)
  async def snipe(self, message):
      if message.channel == snipe_message_channel:
          embed = discord.Embed(color=0x323232, description=f"{snipe_message_content}")
          embed.set_footer(text=f"Asked by {message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar_url)
          embed.set_author(name=snipe_message_author, icon_url=snipe_message_author.avatar_url)
          await message.channel.send(embed=embed)
          return
      else: 
        await message.channel.send("Theres nothing to snipe.")

def setup(bot):
    bot.add_cog(utility(bot))

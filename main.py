from flask import Flask
from threading import Thread

app=Flask("")

@app.route("/")
def index():
    return "<h1>Bot is running</h1>"

Thread(target=app.run,args=("0.0.0.0",8080)).start()

import discord
import json 
import logging
import contextlib
import io
import asyncio
import os
from discord.ext import commands
from pathlib import Path
import datetime

import cogs._json

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

def get_prefix(bot, message):
    data = cogs._json.read_json('prefixes')
    if not str(message.guild.id) in data:
        return commands.when_mentioned_or('!')(bot, message)
    return commands.when_mentioned_or(data[str(message.guild.id)])(bot, message)

#Defining a few things
#secret_file = json.load(open(cwd+'/bot_config/.env'))
bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, owner_id=701727675311587358, intents = discord.Intents.all()) #before messages=True, guilds=True, members=True
bot.remove_command('help')
#bot.config_token = secret_file['token']
logging.basicConfig(level=logging.INFO)

bot.blacklisted_users = []
bot.cwd = cwd

bot.version = '1.6.2'

bot.colors = {
  'WHITE': 0xFFFFFF,
  'AQUA': 0x1ABC9C,
  'GREEN': 0x2ECC71,
  'BLUE': 0x3498DB,
  'PURPLE': 0x9B59B6,
  'LUMINOUS_VIVID_PINK': 0xE91E63,
  'GOLD': 0xF1C40F,
  'ORANGE': 0xE67E22,
  'RED': 0xE74C3C,
  'NAVY': 0x34495E,
  'DARK_AQUA': 0x11806A,
  'DARK_GREEN': 0x1F8B4C,
  'DARK_BLUE': 0x206694,
  'DARK_PURPLE': 0x71368A,
  'DARK_VIVID_PINK': 0xAD1457,
  'DARK_GOLD': 0xC27C0E,
  'DARK_ORANGE': 0xA84300,
  'DARK_RED': 0x992D22,
  'DARK_NAVY': 0x2C3E50
}
bot.color_list = [c for c in bot.colors.values()]

@bot.event
async def on_command_error(ctx, error):
    ignored = (commands.CommandNotFound, commands.UserInputError)
    if isinstance(error, ignored):
      return

    if isinstance(error, commands.CommandOnCooldown):
        m, s = divmod(error.retry_after, 60)
        h, m = divmod(m, 60)
        if int(h) == 0 and int(m) == 0:
          embed = discord.Embed(color=ctx.author.colour)
          embed.add_field(name="CoolDown:", value=f"Whoa slow down there! You must wait `{int(s)} seconds` before using this command again!")
          await ctx.send(embed=embed)
        elif int(h) == 0 and int(m) != 0:
          embed = discord.Embed(color=ctx.author.colour)
          embed.add_field(name="CoolDown:",value=f"Whoa slow down there! You must wait `{int(m)} minutes and {int(s)}` before using this command again!")
          await ctx.send(embed=embed)
        else:
            
          embed = discord.Embed(color=ctx.author.colour)
          embed.add_field(name="CoolDown:", value=f"Whoa slow down there! You must wait `{int(h)} hours, {int(m)} minutes and {int(s)} seconds` before using this command again!")
          await ctx.send(embed=embed)    

    elif isinstance(error, commands.MissingPermissions):
      async with ctx.channel.typing():
        await ctx.send(f"Hey! You lack permissions to use this command.")
        raise error


@bot.event
async def on_ready():
    print(f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nMy current prefix is: -\n-----")
    await bot.change_presence(status=discord.Status.dnd,activity= discord.Activity(type=discord.ActivityType.listening,name=f"!help"))

@bot.event
async def on_message(message):
    #Ignore messages sent by yourself
    if message.author.id == bot.user.id:
        return

    #A way to blacklist users from the bot by not processing commands if the author is in the blacklisted_users list
    if message.author.id in bot.blacklisted_users:
        return

    #Whenever the bot is tagged, respond with its prefix
    if f"<@!{bot.user.id}> prefix" in message.content:
        data = cogs._json.read_json('prefixes')
        if str(message.guild.id) in data:
            prefix = data[str(message.guild.id)]
        else:
            prefix = '!'
        await message.channel.send(f"My prefix here is `{prefix}`")

    await bot.process_commands(message)




"""@bot.event
async def on_member_join(member):
  for channel in member.guild.channels:
        if str(channel) == "welcome-and-leave" or str(channel) == "welcome" :
          embed=discord.Embed(title="WELCOME!", description=f"Welcome to the server {member.mention}")
          await channel.send(embed=embed)"""

'''
@bot.command()
@commands.is_owner()
async def load(ctx, extension):
  bot.load_extension (f'cogs.{extension}')
  await ctx.send(f"Loaded `{extension}`")

@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
  bot.unload_extension (f'cogs.{extension}')
  
for filename in os.listdir('./cogs/'):
  if filename.endswith('.py') and not filename.startswith("help"):
    bot.load_extension(f'cogs.{filename[:-3]}')

@bot.command(aliases=['rl'])
@commands.is_owner()
async def reload(ctx, cog):
        if cog == 'all':
            for filename in os.listdir('./cogs/'):
                if filename.endswith('.py') and not filename.startswith("help"):
                    bot.unload_extension(f'cogs.{filename[:-3]}')
                    bot.load_extension(f'cogs.{filename[:-3]}')
            else:
                rlmsg = await ctx.send("Reloading all cogs...")
                asyncio.sleep(2)
                await rlmsg.edit("Reloaded all cogs!")

        elif cog.endswith(".py") and not cog.startswith("help"):
            await ctx.send(f"Reloading `{cog}`...")
            bot.unload_extension(f'cogs.{cog[:-3]}')
            bot.load_extension(f'cogs.{cog[:-3]}')
            await ctx.send(f'the `{cog}` cog has now been reloaded!')

        elif not cog.endswith(".py") and not cog.startswith("help"):
            await ctx.send(f"Reloading `{cog}`...")
            bot.unload_extension(f'cogs.{cog}')
            bot.load_extension(f'cogs.{cog}')
            await ctx.send(f'the `{cog}` cog has now been reloaded!')

        else:
            await ctx.send('Excetuion Failed. Reason: Unknown Cog')

        print(
            f"{ctx.author.id} attempted to reload an extension named {cog}.\n----------------------------------"
        )
'''
"""@bot.command()
@commands.is_owner()
async def eval(ctx, *, code):
    str_obj = io.StringIO() #Retrieves a stream of data
    try:
        with contextlib.redirect_stdout(str_obj):
            exec(code)
    except Exception as e:
        return await ctx.send(f"```py\n{e.__class__.__name__}: {e}```")
    await ctx.send(f'```py\n{str_obj.getvalue()}```')  """

if __name__ == '__main__':
    # When running this file, if it is the 'main' file
    # I.E its not being imported from another python file run this
    for file in os.listdir(cwd+"/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")
    token = os.environ.get("token")
    bot.run(token)
from flask import Flask
from threading import Thread

app=Flask("")

@app.route("/")
def index():
    return "<h1>Bot is running</h1>"

Thread(target=app.run,args=("0.0.0.0",8080)).start()

import discord
import json 
import ast
import logging
import contextlib
import io
import asyncio
import os
import sys
from termcolor import colored
from pathlib import Path
from discord.ext import commands
from pathlib import Path
import time
import datetime

import cogs._json

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

def get_prefix(bot, message):
    data = cogs._json.read_json('prefixes')
    if not str(message.guild.id) in data:
        return commands.when_mentioned_or('av!')(bot, message)
    return commands.when_mentioned_or(data[str(message.guild.id)])(bot, message)

#Defining a few things
#secret_file = json.load(open(cwd+'/bot_config/.env'))
bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, owner_id=701727675311587358, intents = discord.Intents.all()) #before messages=True, guilds=True, members=True
bot.remove_command('help')
#bot.config_token = secret_file['token']
logging.basicConfig(level=logging.INFO)

bot.blacklisted_users = []
bot.cwd = cwd

bot.version = '1.7.0'

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
    ignored = (commands.CommandNotFound)
    if isinstance(error, ignored):
      return
    if isinstance(error, commands.CommandOnCooldown):
          message = ctx.message
          await message.add_reaction("⏰")    

    elif isinstance(error, commands.MissingPermissions):
        await ctx.message.add_reaction("❌")
        raise error

@bot.event
async def on_ready():
  print(colored("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", 'red'))
  for e in colored("~~I AM READY FOR ACTION!~~", 'grey', 'on_cyan'):
    sys.stdout.write(e)
    sys.stdout.flush()
    time.sleep(0.08)
  print(colored("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", 'white'))

  for y in colored(f"Logged in as: {bot.user}", 'cyan'):
    sys.stdout.write(y)
    sys.stdout.flush()
    time.sleep(0.08)
  print(colored("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", 'red'))
  await bot.change_presence(status=discord.Status.dnd,activity= discord.Activity(type=discord.ActivityType.listening,name=f"!help"))

"""@bot.event
async def on_ready():
    print(f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nMy current prefix is: -\n-----")"""


@bot.event
async def on_message(message):
    #Ignore messages sent by yourself
    if message.author.id == bot.user.id:
        return

    #A way to blacklist users from the bot by not processing commands if the author is in the blacklisted_users list
    if message.author.id in bot.blacklisted_users:
        return

    #Whenever the bot is tagged, respond with its prefix #in message.content
    if message.content.startswith(f"<@!{bot.user.id}>"): 
        data = cogs._json.read_json('prefixes')
        if str(message.guild.id) in data:
            prefix = data[str(message.guild.id)]
        else:
            prefix = 'av!'
        await message.channel.send(f"My prefix here is `{prefix}`")

    await bot.process_commands(message)




"""@bot.event
async def on_member_join(member):
  for channel in member.guild.channels:
        if str(channel) == "welcome-and-leave" or str(channel) == "welcome" :
          embed=discord.Embed(title="WELCOME!", description=f"Welcome to the server {member.mention}")
          await channel.send(embed=embed)"""


"""@bot.command()
@commands.is_owner()
async def load(ctx, extension):
  for extension in os.listdir('./cogs/'):
      if extension.endswith(".py") and not extension.startswith("_"):
          bot.load_extension (f'cogs.{extension}')
          await ctx.send(f"Loaded {extension} ")


@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
  for extension in os.listdir('./cogs/'):
      if extension.endswith(".py") and not extension.startswith("_"):
          bot.unload_extension (f'cogs.{extension}')
          await ctx.send(f"Unloaded {extension}")"""
  
"""for filename in os.listdir('./cogs/'):
  if filename.endswith('.py') and not filename.startswith("_"):
    bot.load_extension(f'cogs.{filename[:-3]}')"""

@bot.command()
@commands.is_owner()
async def unload(ctx, cog):

  if cog.endswith(".py") and not cog.startswith("_"):
    await ctx.send(f"Unloading `{cog}`...")
    bot.unload_extension(f'cogs.{cog[:-3]}')
    await ctx.send(f'the `{cog}` cog has now been unloaded!')

  elif not cog.endswith(".py") and not cog.startswith("_"):
    await ctx.send(f"Unload `{cog}`...")
    bot.unload_extension(f'cogs.{cog}')
    await ctx.send(f'the `{cog}` cog has now been unloaded!')

  else:
    await ctx.send('Excetuion Failed. Reason: Unknown Cog')

  print(
    f"{ctx.author.id} attempted to reload an extension named {cog}.\n----------------------------------")

@bot.command()
@commands.is_owner()
async def load(ctx, cog):

  if cog.endswith(".py") and not cog.startswith("_"):
    await ctx.send(f"Loading `{cog}`...")
    bot.load_extension(f'cogs.{cog[:-3]}')
    await ctx.send(f'the `{cog}` cog has now been loaded!')

  elif not cog.endswith(".py") and not cog.startswith("_"):
    await ctx.send(f"Loading `{cog}`...")
    bot.load_extension(f'cogs.{cog}')
    await ctx.send(f'the `{cog}` cog has now been loaded!')

  else:
    await ctx.send('Excetuion Failed. Reason: Unknown Cog')

  print(
    f"{ctx.author.id} attempted to reload an extension named {cog}.\n----------------------------------")
  
"""for filename in os.listdir('./cogs/'):
  if filename.endswith('.py') and not filename.startswith("_"):
    bot.load_extension(f'cogs.{filename[:-3]}')"""


@bot.command(aliases=['rl'])
@commands.is_owner()
async def reload(ctx, cog):
        if cog == 'all':
            for filename in os.listdir('./cogs/'):
                if filename.endswith(".py") and not filename.startswith("_"):
                    bot.unload_extension(f'cogs.{filename[:-3]}')
                    bot.load_extension(f'cogs.{filename[:-3]}')
            else:
                msg = await ctx.send("Reloading all cogs...")
                await msg.edit(content="Realoaded all cogs.")

        elif cog.endswith(".py") and not cog.startswith("_"):
            await ctx.send(f"Reloading `{cog}`...")
            bot.unload_extension(f'cogs.{cog[:-3]}')
            bot.load_extension(f'cogs.{cog[:-3]}')
            await ctx.send(f'the `{cog}` cog has now been reloaded!')

        elif not cog.endswith(".py") and not cog.startswith("_"):
            await ctx.send(f"Reloading `{cog}`...")
            bot.unload_extension(f'cogs.{cog}')
            bot.load_extension(f'cogs.{cog}')
            await ctx.send(f'the `{cog}` cog has now been reloaded!')

        else:
            await ctx.send('Excetuion Failed. Reason: Unknown Cog')

        print(
            f"{ctx.author.id} attempted to reload an extension named {cog}.\n----------------------------------")
        


def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


@bot.command()
@commands.is_owner()
async def eval_fn(ctx, *, cmd):
    """Evaluates input.
    Input is interpreted as newline seperated statements.
    If the last statement is an expression, that is the return value.
    Usable globals:
      - `bot`: the bot instance
      - `discord`: the discord module
      - `commands`: the discord.ext.commands module
      - `ctx`: the invokation context
      - `__import__`: the builtin `__import__` function
    Such that `>eval 1 + 1` gives `2` as the result.
    The following invokation will cause the bot to send the text '9'
    to the channel of invokation and return '3' as the result of evaluating
    >eval ```
    a = 1 + 2
    b = a * 2
    await ctx.send(a + b)
    a
    ```
    """
    fn_name = "_eval_expr"

    cmd = cmd.strip("` ")

    # add a layer of indentation
    cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

    # wrap in async def body
    body = f"async def {fn_name}():\n{cmd}"

    parsed = ast.parse(body)
    body = parsed.body[0].body

    insert_returns(body)

    env = {
        'bot': ctx.bot,
        'discord': discord,
        'commands': commands,
        'ctx': ctx,
        '__import__': __import__
    }
    exec(compile(parsed, filename="<ast>", mode="exec"), env)

    result = (await eval(f"{fn_name}()", env))
    await ctx.send(result)

@bot.group()
@commands.is_owner()
@commands.guild_only()
async def debug(ctx):
  if ctx.invoked_subcommand is None:
    await ctx.send("```On / Off```")

@debug.command()
@commands.is_owner()
@commands.guild_only()
async def on(ctx):
  bot.load_extension('cogs._debug')
  await ctx.send(f'Debug On!')

@debug.command()
@commands.is_owner()
@commands.guild_only()
async def off(ctx):
  bot.unload_extension('cogs._debug')
  await ctx.send(f'Debug Off!')

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
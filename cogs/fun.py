import discord
import json
from aiohttp import request
import asyncio
import random
import aiohttp
from discord.ext import commands

class fun(commands.Cog, name='fun'):

  def __init__(self, bot):
            self.bot = bot
  @commands.command(description="Eject a person who you think is sus! <:sus:772060172138840084>")
  async def eject(self, ctx, member: discord.Member=None):
    if member == None:
      member=ctx.author
    responces=[f'''. 　　　。　　　　•　    　ﾟ　　。 　　.

        　　　.　　　  　　.　　　　　。　　   。　.  　

        .　　      。　　　　　 ඞ   。   . 　　 • 　　　　•

        　　ﾟ　　 {member.name} was not An Impostor. 。　.

        　　'　　　 2 Impostor remains 　 　　。

        　　ﾟ　　　.　　　. 　　　　.　 .''',
        f'''. 　　　。　　　　•　    　ﾟ　　。 　　.

        　　　.　　　  　　.　　　　　。　　   。　.  　

        .　　      。　　　　　 ඞ   。   . 　　 • 　　　　•

        　　ﾟ　　 {member.name} was An Impostor. 。　.

        　　'　　　 2 Impostor remains 　 　　。

        　　ﾟ　　　.　　　. 　　　　.　 .'''
        
        ]
    await ctx.send(f'{random.choice(responces)}')

  @commands.command()
  @commands.cooldown(1, 1, commands.BucketType.user)
  async def meme(self, ctx):
    embed = discord.Embed(title="MEME")
    async with aiohttp.ClientSession() as cs:
      async with cs.get('https://www.reddit.com/r/aviationmemes/new/.json?sort=hot') as r:
        res = await r.json()
        embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
        await ctx.send(embed=embed)

  @commands.command(description="A fun command that you can use the hack your friends or **Enimies**!!")
  @commands.cooldown(1, 30, commands.BucketType.user)
  async def hack(self, ctx, member: discord.Member=None):
    if not member:
      await ctx.send('Please specify a member you would like to perform the hack on.<:hack:765540760178917417>')
      return
    msg = await ctx.send(content=f'[▘] Starting to hack {member}...')
    await asyncio.sleep(2)
    await msg.edit(content=f"[▝ ] Finding {member}'s password...")
    await asyncio.sleep(2)
    await msg.edit(content=f"[▖] {member}'s Email: `{member}.Hello@Email.com` \nPassowrd: `PAJDHSF.SHU@{member.name}`...")
    await asyncio.sleep(2)
    await msg.edit(content='[▗] Finding IP adress...')
    await asyncio.sleep(2)
    await msg.edit(content=f"[▘]{member}'s IP adress is: `65.171.199.83`")
    await asyncio.sleep(2)
    await msg.edit(content=f"[▘] Finding {member}'s latest DM.")
    await asyncio.sleep(2)
    await msg.edit(content="[▗] Latest DM: <a:Thecat:765079289590579210> Aw cats are cute...")
    await asyncio.sleep(2)
    await msg.edit(content='[▖]<a:loading:750313247110070375> almost done... ')
    await asyncio.sleep(5)
    await msg.edit(content='The hack is almost finished...')
    await asyncio.sleep(2)
    hack_responces1 = [f'<a:correct:765080491669061633> I have successfuly hacked **{member}**!',
                    '<a:wrong:765080446937202698> Hack Failed! You have been reported to discord for abusing the API and have been banned from using Discord.'] 

    await ctx.send(f'{random.choice(hack_responces1)}')


  @commands.command(aliases=["birdfacts"])
  @commands.guild_only()
  async def bird_facts(self, ctx):

    """Random Bird Facts!"""

    with open("APIS.json", 'r') as f:
      API = json.load(f)

    bird = API['birdfact']

    async with request("GET", bird, headers={}) as response:
      if response.status == 200:
        data = await response.json()

        embed = discord.Embed(title="FAX", description=f'{data["fact"]}', color=discord.Colour.red())

        embed.set_footer(text=f'Requested By: {ctx.author}', icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url="https://news.usc.edu/files/2019/11/Taiwan-Blue-Magpie-web.jpg")

        await ctx.send(embed=embed)

      else:
        print(response.status)
def setup(bot):
    bot.add_cog(fun(bot))

import discord
import random
import asyncio
import datetime
from discord.ext import commands

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

class Giveaway(commands.Cog, name="giveaway"):


  def __init__(self, bot):
    self.bot = bot  
  
  @commands.command(description=f'Start a giveaway!', aliases=['gcreate', 'giveawaycreate'])
  @commands.guild_only()
  @commands.has_permissions(manage_guild=True)
  async def giveaway_create(self, ctx):

    await ctx.send("**Let's start with this giveaway!** Answer these questions within 30 seconds!")

    questions = ["1. **Which channel should this giveaway be hosted in?**", 
                "2. What should be the duration of the giveaway? (s|m|h|d|w) \nexample: `5d`",
                "3. What is the prize when someone wins the giveaway?"]

    answers = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel 

    for i in questions:
        await ctx.send(i)

        try:
            msg = await self.bot.wait_for('message', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('You didn\'t answer in time, please be quicker next time!')
            return
        else:
            answers.append(msg.content)
    try:
        c_id = int(answers[0][2:-1])
    except:
        await ctx.send(f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time.")
        return

    channel = self.bot.get_channel(c_id)

    time = convert(answers[1])

    if time == -1:
        await ctx.send(f"You didn't answer the time with a proper unit. Use (s|m|h|d|w) next time!")
        return
    elif time == -2:
        await ctx.send(f"The time must be an integer. Please enter an integer next time")
        return            

    prize = answers[2]

    await ctx.send(f"The __Giveaway will be in {channel.mention}__ and will last **{answers[1]}!** \n\nprize: **{prize}!**")


    embed = discord.Embed(title = "Giveaway!", description = f"{prize}", color = 0xB19CD9)

    embed.set_author(name = f"Giveaway Created by {ctx.author}!", icon_url=ctx.author.avatar_url)

    embed.set_footer(text = f"React with 🎉 to enter! | Ends {answers[1]} from now!")

    my_msg = await channel.send(embed = embed)


    await my_msg.add_reaction("🎉")


    await asyncio.sleep(time)


    new_msg = await channel.fetch_message(my_msg.id)


    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(self.bot.user))

    try:
      winner = random.choice(users)
    except IndexError:
      await ctx.send("Oh well... No one even entered. 😦")

    await ctx.author.send(f"The giveaway that you started {answers[1]} ago from {ctx.guild.name} has ended.\n\nWinner: {winner} | ID: `{winner.id}` ")
    await channel.send(f"Congratulations! {winner.mention} has won **{prize}**!")

  @commands.command()
  @commands.guild_only()
  @commands.has_permissions(administrator = True)
  async def reroll(self, ctx,  id_of_giveaway : int):
    await ctx.message.delete()

    try:
      new_msg = await ctx.channel.fetch_message(id_of_giveaway)
    except:
      await ctx.send("**ERROR!**\nInvalid message id")
      return
      
    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(self.bot.user))

    winner = random.choice(users)

    await ctx.channel.send(f"The new winner is {winner.mention}!")
  @commands.command(aliases=['Gstart'], description="Create a giveaway!\nUsage: `!gstart <sec(s), min(m), h(h)><prize>`")
  @commands.has_permissions(manage_guild=True)
  async def giveaway_start(self, ctx, time, *, prize: str):

    embed = discord.Embed(title=f'PRIZE:\n {prize}', description=f" ", color=discord.Color.green(),
                          timestamp=datetime.datetime.utcnow())
    seconds = 0
    if prize is None:
        embed.add_field(name='Warning', value='Please specify what do you want to giveaway.')  # Error message
    if time.lower().endswith("d"):
        seconds += int(time[:-1]) * 60 * 60 * 24
        counter = f"{seconds // 60 // 60 // 24} days"
    if time.lower().endswith("h"):
        seconds += int(time[:-1]) * 60 * 60
        counter = f"{seconds // 60 // 60} hours"
    elif time.lower().endswith("m"):
        seconds += int(time[:-1]) * 60
        counter = f"{seconds // 60} minutes"
    elif time.lower().endswith("s"):
        seconds += int(time[:-1])
        counter = f"{seconds} seconds"
    if seconds == 0:
        embed.add_field(name='Warning',
                        value='Please specify a proper duration')
    embed.add_field(name=f" Ends in :", value=f"{counter}", inline=False)
    embed.add_field(name=f"Host :", value=f"{ctx.author.mention}", inline=True)
    embed.set_footer(text=f"React with a 🎉 to enter")

    my_msg = await ctx.send("**<a:tada:771245416736882708> GIVEAWAY! <a:tada:771245416736882708>**", embed=embed)

    await my_msg.add_reaction("🎉")

    await asyncio.sleep(seconds)

    new_msg = await ctx.channel.fetch_message(my_msg.id)

    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(ctx.bot.user))

    winner = random.choice(users)

    win_embed = discord.Embed(title=f'{prize}', description=f" ", color=discord.Color.red())

    win_embed.add_field(name=" Winner :", value=f"{winner.mention}", inline=True)
    win_embed.add_field(name=" Host :", value=f"{ctx.author.mention}", inline=True)
    win_embed.set_footer(text=f"📃 Valid Entries : {new_msg.reactions[0].count - 1}")

    await my_msg.edit(content="**<a:tada:771245416736882708> GIVEAWAY ENDED! <a:tada:771245416736882708>**", embed=win_embed)
    await ctx.message.delete()
    await ctx.send(f"Congratulations! {winner.mention} won **{prize}**!")
def setup(bot):
    bot.add_cog(Giveaway(bot))

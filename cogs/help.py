import discord
from discord.ext import commands
import cogs._json
class help(commands.Cog, name="help"):

  def __init__(self, bot):
            self.bot = bot
        
  @commands.command()
  async def help(self, ctx, *cog):

    data = cogs._json.read_json('prefixes')
    if str(ctx.guild.id) in data:
        prefix = data[str(ctx.guild.id)]
    else:
        prefix = '!'

    if not cog:
      embed=discord.Embed(color=discord.Color.red(), description=f"**Guild Prefix:** `{prefix}`")
      cog_desc = " "
      for x in self.bot.cogs:
        cog_desc += ("{}".format(x)+'\n') #Old cog_desc += ("**{}** - {}".format(x, self.bot.cogs[x].__doc__)+'\n')
      embed.add_field(name="All Modules:", value=cog_desc[0:len(cog_desc)-1], inline=False)
      embed.set_footer(text=f"Use {prefix}help [module] for more info.")
      embed.set_author(name="Help Menu", icon_url=self.bot.user.avatar_url)
      await ctx.send(embed=embed)

    else:
      if len(cog) > 1:
        embed=discord.Embed(title="Error", description="Command/Module Not found!", color=discord.Color.red())
        await ctx.send(embed=embed)      
        
      else:
        found = False
        for x in self.bot.cogs:
          for y in cog:
            if x == y:
              embed=discord.Embed(color=discord.Color.red(), description=f"**Guild Prefix:** `{prefix}`")
              scog_info = ""
              #print (self.bot.get_cog(y).get_commands())
              for c in self.bot.get_cog(y).get_commands():
                if not c.hidden:
                  scog_info += f"`{c.name}` ➣ {c.help}\n"
              embed.add_field(name=f"{cog[0]} Module", value=scog_info) #Old = embed.add_field(name=f"{cog[0]} Module - {self.bot.cogs[cog[0]].__doc__}", value=scog_info)
              embed.set_footer(text=f"Use {prefix}help [command] for more info.")
        if not found:
          for x in self.bot.cogs:
            for c in self.bot.get_cog(x).get_commands():
              if c.name == cog[0]:
                
                embed=discord.Embed(color=discord.Color.red())
                embed.set_author(name=c.name.upper(), icon_url=self.bot.user.avatar_url)
                embed.add_field(name="Proper Syntax:", value=f'`{prefix}{c.qualified_name} {c.signature}`') 
                embed.add_field(name="Aliases:", value=f'`{c.aliases}`', inline=False)
                embed.add_field(name="Description:", value=f'**{c.help}**', inline=False)
                embed.set_footer(text="<> - Required ┃ [] - Optional")                    
          found = True
          if not found:
            embed=discord.Embed(description='That is not a cog.', color=discord.Color.red())
            await ctx.send(embed=embed)
        await ctx.send(embed=embed)

        
def setup(bot):
    bot.add_cog(help(bot))
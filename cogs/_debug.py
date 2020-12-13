import discord
from discord.ext import commands

class debug(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.UserInputError):
          await ctx.send(error)

def setup(bot):
    bot.add_cog(debug(bot))

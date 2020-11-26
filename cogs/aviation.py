import requests
from bs4 import BeautifulSoup
import aiohttp
import discord
from discord.ext import commands

class Aviation(commands.Cog, name='aviation'):

   def __init__(self, client):
      """Init"""
      self.client = client

   
   @commands.command()
   async def metar(self, ctx, APT=None):

      """Returns METAR for airport passed as arguement"""

      # print(f"METAR {APT.upper()}")
      embed = discord.Embed(
         title=f"{APT.upper()} METAR", 
         colour=discord.Colour.red(),
         description=await Aviation.async_metar(APT)
      )
      embed.set_author(name="Weather", icon_url="https://cdn.discordapp.com/avatars/761414234767884318/a824512ca5391941b1de5b4e1a6e5302.png?size=2048")
      await ctx.send(embed=embed)

   @commands.command()
   async def taf(self, ctx, APT=None):
     
      """Returns TAF for airport passed as arguement"""

      # print(f"TAF {APT.upper()}")
      embed = discord.Embed(
         title=f"{APT.upper()} TAF", 
         colour=discord.Colour.red(),
         description=await Aviation.async_taf(APT)
      )
      embed.set_author(name="AVWeather", icon_url="https://cdn.discordapp.com/avatars/761414234767884318/a824512ca5391941b1de5b4e1a6e5302.png?size=2048")
      await ctx.send(embed=embed)

   @commands.command(aliases=["wx"])
   async def report(self, ctx, APT=None):
      """Returns airport METAR/TAF passed as arguement"""
      # print(f"Report {APT.upper()}")
      embed = discord.Embed(
         title=f"{APT.upper()} Weather Report", 
         colour=discord.Colour.red()
      )
      embed.set_author(name="AVWeather", icon_url="https://cdn.discordapp.com/avatars/761414234767884318/a824512ca5391941b1de5b4e1a6e5302.png?size=2048")
      embed.add_field(name="METAR", value=await Aviation.async_metar(APT), inline=False)
      embed.add_field(name="TAF", value=await Aviation.async_taf(APT), inline=False)
      await ctx.send(embed=embed)

   # ------ Static methods not bound to discord ------
   @staticmethod
   def sync_metar(APT="EIDW"):
      """
      Returns (sync) requested airport METAR
      Default airport set to Dublin (EIDW)
      """

      uri = f"https://aviationweather.gov/metar/data?ids={APT}"
      web = requests.get(uri)
      if web.ok:
         soup = BeautifulSoup(web.text, "html.parser")
         try:
            return soup.code.text
         except AttributeError:
            return "Invalid airport"
      else:
         return f"Web error occured. code: {web.status_code}"

   @staticmethod
   def sync_taf(APT="EIDW"):
      """
      Returns (sync) requested airport TAF
      Default airport set to Dublin (EIDW)
      """

      uri = f"https://aviationweather.gov/taf/data?ids={APT}"
      web = requests.get(uri)
      if web.ok:
         soup = BeautifulSoup(web.text, "html.parser")
         try:
            return soup.code.text
         except AttributeError:
            return "Invalid airport"
      else:
         return f"Web error occured. code: {web.status_code}"

   @staticmethod
   async def async_metar(APT="EIDW"):
      """
      Returns (sync) requested airport METAR
      Default airport set to Dublin (EIDW)
      """

      uri = f"https://aviationweather.gov/metar/data?ids={APT}"
      timeout = aiohttp.ClientTimeout(total=10)
      async with aiohttp.ClientSession(timeout=timeout) as sesh:
         async with sesh.get(uri) as web_resp:
            if web_resp.status == 200:
               web = await web_resp.text()
               soup = BeautifulSoup(web, "html.parser")
               try:
                  return soup.code.text
               except AttributeError:
                  return "Invalid airport"
            else:
               return "Warning, Error occured. code: {web_resp.status}"
      return "Warning, request timeout"

   @staticmethod
   async def async_taf(APT="EIDW"):
      """
      Returns (async) requested airport TAF
      Default airport set to Dublin (EIDW)
      """
      
      uri = f"https://aviationweather.gov/taf/data?ids={APT}"
      timeout = aiohttp.ClientTimeout(total=10)
      async with aiohttp.ClientSession(timeout=timeout) as sesh:
         async with sesh.get(uri) as web_resp:
            if web_resp.status == 200:
               web = await web_resp.text()
               soup = BeautifulSoup(web, "html.parser")
               try:
                  return soup.code.text
               except AttributeError:
                  return "Invalid airport"
            else:
               return "Warning, Error occured. code: {web_resp.status}"
      return "Warning, request timeout"

def setup(client):
   client.add_cog(Aviation(client))


def main():
   print(" --- Airport METAR / TAF testing --- ")

   # print(Weather.sync_metar("EGLL"))
   # print(Weather.sync_taf("KLAX"))
   # print(Weather.sync_metar())


async def amain():
   print(" --- Airport METAR / TAF testing --- ")

   print(await Aviation.async_metar())
   # print(await Weather.async_taf("KLAX"))


if __name__ == "__main__":
   import asyncio
   # main()
   asyncio.run(amain())
import discord
import requests
import os
import dotenv
from bs4 import BeautifulSoup
from discord.ext import commands

#Your Discord Bot token goes here
TOKEN = 'MTA0NDgxNTk5MTYzNDQxNTc1Ng.Gx9UWQ.FuCgjTnblB5cQQLo3FK5UdTkJrJGl4mu3whLlI'

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='!',help_command=None,case_insensitive=True,intents=intents)

@bot.event
async def startup():
  await print('Logged in as {0.user}'.format(bot))
  
def scrape(url):
  response = requests.get(url)
  if response.status_code == 200:
    print("Scraping successful!")
    soup = BeautifulSoup(response.text,'html.parser')
    data = soup.find_all(lambda tag: tag.name == "script" and 'var meta = {"product":{' in tag.text)
    string = str(data).split('"id":')
    hm = {}
    for x in string:
      splitted = x.split(',')
      if len(splitted[0]) == 14:
        size = x.split('"public_title":"')[1]
        size = size.split('"')
        hm[size[0]] = splitted[0]
    length = len(hm)
    embed = create_embed(url,length,hm)
    print('Embed created successfully!')
    return embed
  else:
    print("Scrape failed!")
    embed = discord.Embed(
    title='Scraping Failed!',
    description="Try a different url?",
    color=discord.Colour.dark_purple()
    )
      
def create_embed(url,length,hashmap):
  embed = discord.Embed(
    title='Scraping successful!',
    description=str(length) + " ID's scraped!",
    color=discord.Colour.dark_purple()
    )
  for x in hashmap:
    embed.add_field(
    name="Size " + x,
    value=hashmap[x], 
    inline=True
    )
  return embed
  
@bot.command()
async def Variants(ctx, arg):
  embed = scrape(arg)
  await ctx.channel.send(embed=embed)
  

@bot.command()
async def help(ctx):
  embed = discord.Embed(
    title='VariantScraper Commands',
    description='Commands for VariantScraper!',
    color=discord.Colour.green()
  )
  embed.add_field(
    name='!help',
    value='List of VariantScraper Commands',
    inline=True
  )
  embed.add_field(
    name='!Variants',
    value='Grabs variants from url',
    inline=True
  )
  await ctx.send(embed=embed)

print('Ready to Scrape!')
bot.run(TOKEN)
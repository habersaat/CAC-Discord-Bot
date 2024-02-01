import discord
from discord.ext import commands
import json
import random
import requests
from time import strftime, localtime

with open("config.json", "r") as configjsonFile:
    configData = json.load(configjsonFile)
    TOKEN = configData["TOKEN"]
    PREFIX = configData["PREFIX"]
    API_KEY = configData["API_KEY"]

bot = commands.Bot(command_prefix = PREFIX, intents = discord.Intents.all())

def correctPerms(ctx):
    return ctx.channel.id == 1199128985490178111 and '@' not in ctx.message.content.lower()

def hasPermissions():
    return commands.check(correctPerms)


def veryCorrectPerms(ctx):
    return ctx.channel.id == 1199128985490178111 and ctx.author.id == 217098052941512705

def hasAdminPermissions():
    return commands.check(veryCorrectPerms)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command()
@hasPermissions()
async def ping(ctx):
    await ctx.send(f'Pong! Latency: {str(round(bot.latency * 1000))}ms')

@bot.command()
@hasPermissions()
async def echo(ctx, *args):
    arguments = ' '.join(args)
    await ctx.send(f'{arguments}')


@bot.event
async def on_member_join(member):
    print(f'{member} has entered the CAC Discord! Welcome!')

@bot.event
async def on_member_remove(member):
    print(f'{member} has left the CAC Discord! Welcome!')


##############################################################
    
@bot.command()
@hasPermissions()
async def slap(ctx, members: commands.Greedy[discord.Member], *, reason='no reason'):
    slapped = ", ".join(m.name for m in members)
    await ctx.send(f'{slapped} just got slapped by {ctx.author.mention} for {reason}.')

@bot.command()
@hasAdminPermissions()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit = amount)
    await ctx.send(f'Deleted {amount} messages')

@bot.command()
@hasAdminPermissions()
async def game(ctx, *args):
    name = ' '.join(args)
    game = discord.Game(name)
    await bot.change_presence(status=discord.Status.online, activity=game)

##############################################################
    
@bot.command()
@hasPermissions()
async def predict(ctx, *, question):

    responses = [
        'It is certain.',
        'Without a doubt.',
        'Most likely.',
        'Outlook not so good',
        'Very doubtful'
    ]

    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@bot.command()
@hasPermissions()
async def fact(ctx):

    limit = 1
    api_url = 'https://api.api-ninjas.com/v1/facts?limit={}'.format(limit)
    response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
    data = response.json()
    
    if response.status_code == requests.codes.ok:
        await ctx.send(f'Fun Fact: {data[0]["fact"]}')
    else:
        print("Error:", response.status_code, response.text)

@bot.command()
@hasPermissions()
async def stock(ctx, symbol):
    api_url = 'https://api.api-ninjas.com/v1/stockprice?ticker={}'.format(symbol)
    response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
    data = response.json()
    if response.status_code == requests.codes.ok:
        embed=discord.Embed(title=f'📈 {data["ticker"]} Stock Info', description=f'{data["name"]}', color=0x49be25)
        embed.add_field(name="Price:", value=f'{data["price"]}', inline=False)
        embed.add_field(name="Exchange:", value=f'{data["exchange"]}', inline=False)
        embed.add_field(name="Last updated:", value=f'{strftime("%Y-%m-%d %H:%M:%S", localtime(int(data["updated"])))}', inline=False)
        embed.set_footer(text="This does not constitute investment advice.")
        await ctx.send(f'{ctx.author.mention}', embed=embed)
    else:
        print("Error:", response.status_code, response.text)


bot.run(TOKEN)


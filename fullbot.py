import discord
from discord.ext import commands
import json
import random
import string

client = commands.Bot(command_prefix='*')
client.remove_command('help')

characterList = {}
enemyList = {}

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('*help'))
    print('Ready!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await client.process_commands(message)


@client.command()
async def ping(ctx):
    await ctx.send(f'{round(client.latency * 1000)} ms')


@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    recipient = await author.create_dm()
    embed = discord.Embed(
        color=discord.Colour.blurple()
    )
    embed.set_author(name='Help')
    embed.add_field(
        name='ping', value='returns the latency in milliseconds', inline=False)

    await recipient.send(embed=embed)


@client.command(pass_context=True)
async def new(ctx):
    author = ctx.message.author
    channel = ctx.message.channel
    await channel.send("Hello! To create a new player, type **p**. To enter data for an enemy, type **e**")
    print(str(author.mention) + " initiated command *new.")
    msg = await client.wait_for("message", check=lambda message: message.author == ctx.author)
    if msg.content.lower() == "p":
        await channel.send("Enter the name, hp, ac, and stats (top -> down) of the character separated by spaces.")
        msg = await client.wait_for("message", check=lambda message: message.author == ctx.author)
        msgContent = str(msg.content)
        msg = msgContent.split(' ')
        characterList[msg[0]] = {"health": int(msg[1]),
                                 "ac": int(msg[2]),
                                 "str": int(msg[3]),
                                 "dex": int(msg[4]),
                                 "con": int(msg[5]),
                                 "int": int(msg[6]),
                                 "wis": int(msg[7]),
                                 "chr": int(msg[8])}
        await channel.send("New character: " + msg[0] + ".")
        print("Successfully created " + msg[0] + ".")

    elif msg.content.lower() == "e":
        await channel.send("Enter the name, hp, ac, and stats (top -> down) of the enemy separated by spaces.")
        msg = await client.wait_for("message", check=lambda message: message.author == ctx.author)
        msgContent = str(msg.content)
        msg = msgContent.split(' ')
        enemyList[msg[0]] = {"health": int(msg[1]),
                                 "ac": int(msg[2]),
                                 "str": int(msg[3]),
                                 "dex": int(msg[4]),
                                 "con": int(msg[5]),
                                 "int": int(msg[6]),
                                 "wis": int(msg[7]),
                                 "chr": int(msg[8])}
        await channel.send("New enemy: " + msg[0] + ".")
        print("Successfully created " + msg[0] + ".")
    
    else:
        await channel.send("Invalid argument!")
        print("Invalid argument when passing modifier during *new execution.")
        
@client.command()
async def roll(ctx, type, modifier:int):
    author = ctx.message.author
    if(type == "init" or type == "initiative"):
        roll = random.randrange(1, 20)
        try:
            init = roll + modifier
            await ctx.send(str(author.mention) + ' rolled a ' + str(init))
        except ValueError:
            await ctx.send('Make sure your modifier is a number. Here is your roll without your modifier: ' + str(roll))
    else:
        # parse type to determine number of rolls and dype of dice
        # check the first character
        print('Invalid argument when passing modifier during *roll execution.')

client.run('Token')

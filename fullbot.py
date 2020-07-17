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


@client.command(pass_context=True)
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


@client.command(pass_context=True)
async def roll(ctx, param, *modifier):
    try:
        mod = modifier[0]
    except IndexError:
        mod = 0
    try:
        mod = int(mod)
    except ValueError:
        await ctx.send('Make sure your modifier is a number!')
        print("Invalid argument when passing modifier during *roll execution.")
        return
    print("Roll initiated successfully.")
    author = ctx.message.author
    if(param == "init" or param == "initiative"):
        await ctx.send(str(author.mention) + ' rolled a ' + str((random.randint(1, 20) + mod)))
    else:
        # parse type to determine number of rolls and dype of dice
        # check the first character
        paramSplit = []
        rollCount = 1
        for letter in range(len(param)):
            paramSplit.append(param[letter])
        if(paramSplit[0] == 'd' or paramSplit[0] == 'D'):
            rollCount = 1
        else:
            for item in paramSplit:
                try:
                    item = int(item)
                    print(item)
                except ValueError:
                    print(item)


@client.command(pass_context=True)
async def combat(ctx):
    channel = ctx.message.channel
    author = ctx.message.author
    await channel.send("Combat initiated! Please type the names of the characters in combat. Please make sure they are registered with *new.")
    msg = await client.wait_for("message", check=lambda message: message.author == ctx.author)
    msgContent = str(msg.content)
    msg = msgContent.split()
    combatList = []
    initDict = {}

    for i in range(len(msg)):
        if msg[i] in characterList:
            combatList.append(msg[i])
        else:
            await ctx.send("This character is not registered in our system!")
            return

    for i in range(len(combatList)):
        dex = (characterList[combatList[i]])
        cool = random.randint(1, 20)
        mod = (dex["dex"] / 2)
        mod = mod.__floor__()
        result = cool + mod
        print(f"{dex}\'s initiative is {result}.")
        await channel.send(str(author.mention) + " rolled a " + result + " for initative!")
        initDict.update(dex: result)

    newInitDict = sorted(initDict, reverse = True)

    for i in range(len(newInitDict)):
        await channel.send(f"{i}: {newInitDict[i]}")

client.run('Token')

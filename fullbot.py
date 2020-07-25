import discord
from discord.ext import commands
import json
import random
import string
import math

client = commands.Bot(command_prefix='*')
client.remove_command('help')


def loadCharacters(channel_ID, ctx):
    # load full JSON file into the allChr dict, pick out the correct one that correlates to the chanel_ID and save to characterList
    with open('characters.json', 'r') as file:
        allChr = json.load(file)
        allChr = json.loads(allChr)
    if(str(channel_ID) in allChr):
        characterList = allChr[str(channel_ID)]
    else:
        allChr.update(
            {str(channel_ID): {"channel_init": {"channel_init": "channel_init"}}})
        finaldump = json.dumps(allChr)
        with open('characters.json', 'w') as file:
            json.dump(finaldump, file, indent=4)
        ctx.send("This channel doesn't have any characters registered. Do \'*new\' to register a new character to this channel.")
        characterList = {None: {
            "name": None,
            "author": None,
            "health": None,
            "ac": None,
            "str": None,
            "dex": None,
            "con": None,
            "int": None,
            "wis": None,
            "chr": None}
        }
    return characterList


def saveCharacter(chrName, channel_ID, character):
    # save character
    channel = str(channel_ID)
    chrDict = character
    chrName = str(chrName)
    # make new char
    with open('characters.json') as f:
        allChr = json.load(f)
        allChr = json.loads(allChr)
    if(channel in allChr):
        # take out that dict
        workingDict = allChr[channel]
        updateChr = {chrName: chrDict}
        workingDict.update(updateChr)
    else:
        # channel not found, put in a placeholder then deposit the character
        allChr.update(
            {channel: {"channel_init": {"channel_init": "channel_init"}}})
        workingDict = allChr[channel]
        updateChr = {chrName: chrDict}
        workingDict.update(updateChr)
    # replace the old dict with the new one
    allChr[channel] = workingDict
    # put the new json into the file
    with open('characters.json', 'w') as file:
        dump = allChr
        finaldump = json.dumps(dump)
        json.dump(finaldump, file, indent=4)


def delCharacter(channel_ID, chrName):
    # pop that character
    chrName = str(chrName)
    channel = str(channel_ID)
    with open('characters.json') as f:
        allChr = json.load(f)
        allChr = json.loads(allChr)
    try:
        workingDict = allChr[channel]
        del workingDict[chrName]
        allChr[channel] = workingDict
        with open('characters.json', 'w') as file:
            dump = allChr
            finaldump = json.dumps(dump)
            json.dump(finaldump, file, indent=4)
        return True
    except:
        print("delete failed")
        return False


enemyList = {}


@ client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('*help'))
    print('Ready!')


@ client.event
async def on_message(message):
    if message.author == client.user:
        return
    await client.process_commands(message)


@ client.command(pass_context=True)
async def ping(ctx):
    await ctx.send(f'{round(client.latency * 1000)} ms')


@ client.command(pass_context=True)
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


@ client.command(pass_context=True)
async def new(ctx):
    author = ctx.author
    channel = ctx.channel.id
    await ctx.send("Hello! To create a new player, type **p**. To enter data for an enemy, type **e**")
    print(str(author) + " initiated command *new.")
    msg = await client.wait_for("message", check=lambda message: message.author == ctx.author)
    if msg.content.lower() == "p":
        await ctx.send("Enter the name, hp, ac, and stats (top -> down) of the character separated by spaces.")
        msg = await client.wait_for("message", check=lambda message: message.author == ctx.author)
        msgContent = str(msg.content)
        msg = msgContent.split(' ')
        characterList = {}
        characterList[msg[0]] = {"name": str(msg[0]),
                                 "author": str(ctx.author),
                                 "health": int(msg[1]),
                                 "ac": int(msg[2]),
                                 "str": int(msg[3]),
                                 "dex": int(msg[4]),
                                 "con": int(msg[5]),
                                 "int": int(msg[6]),
                                 "wis": int(msg[7]),
                                 "chr": int(msg[8])}
        saveCharacter(characterList[msg[0]]["name"], channel, characterList)
        await ctx.send("New character: " + characterList[msg[0]]["name"] + ".")

    elif msg.content.lower() == "e":
        await ctx.send("Enter the name, hp, ac, and stats (top -> down) of the enemy separated by spaces.")
        msg = await client.wait_for("message", check=lambda message: message.author == ctx.author)
        msgContent = str(msg.content)
        msg = msgContent.split(' ')
        enemyList[msg[0]] = {"name": str(msg[0]),
                             "health": int(msg[1]),
                             "ac": int(msg[2]),
                             "str": int(msg[3]),
                             "dex": int(msg[4]),
                             "con": int(msg[5]),
                             "int": int(msg[6]),
                             "wis": int(msg[7]),
                             "chr": int(msg[8])}
        await ctx.send("New enemy: " + msg[0] + ".")
        print("Successfully created " + msg[0] + ".")

    else:
        await ctx.send("Invalid argument!")
        print("Invalid argument when passing modifier during *new execution.")


@client.command(pass_context=True)
async def delete(ctx):
    channel = str(ctx.channel.id)
    author = str(ctx.author.mention)
    await ctx.send(author + ", are you absolutely sure that you want to delete a character? Type \"yes\" to confirm, or anything else to decline.")
    response = await client.wait_for("message", check=lambda message: message.author == ctx.author)
    response = str(response.content).lower()
    if(response == "yes"):
        # delete that boi
        await ctx.send("Please enter the character's name. Keep in mind, this is case sensitive.")
        resp = await client.wait_for("message", check=lambda message: message.author == ctx.author)
        resp = str(resp.content)
        status = delCharacter(channel, resp)
        if(status == True):
            await ctx.send("Character deleted.")
        else:
            await ctx.send("Delete failed. Are you sure there is a character with name " + str())
    else:
        await ctx.send("Delete cancelled.")


@ client.command(pass_context=True)
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
        for letter in range(len(param)):
            paramSplit.append(param[letter])
        if(paramSplit[0] == 'd' or paramSplit[0] == 'D'):
            if int(paramSplit[1]) <= 100:
                    a = str(random.randint(1, paramSplit[1]))
                    await ctx.send(f"{str(author.mention)} rolled a {str(a)}. :game_die:") #Exception TypeError: concatenating int to str is not possible, but where is the int?????
            else:
                await ctx.send("Make sure that you are only rolling dice less than or equal to 100!")
                return
        else:
            if("d" in paramSplit or "D" in paramSplit):
                # nomial path
                itemstr = ''
                for item in paramSplit:
                    itemstr += str(item)
                splitItem = itemstr.split('d')
                roll = 0
                if int(splitItem[1]) <= 100 and int(splitItem[0]) <= 100:
                    for rollnum in range(int(splitItem[0])):
                        roll += random.randint(1, int(splitItem[1]))
                    await ctx.send(str(author.mention) + ' rolled a ' + str(roll) + '. :game_die:')
                else:
                    await ctx.send("Make sure that you are only rolling dice less than or equal to 100!")
                    return
            else:
                await ctx.send('Please format your roll correctly: \"[number of rolls]d[die type]\". i.g. \"5d8\".*r')
                return


@ client.command(pass_context=True)
async def combat(ctx):
    channel = ctx.message.channel.id
    author = ctx.message.author
    await ctx.send("Combat initiated! Please type the names of the characters in combat. Please make sure they are registered with *new.")
    msg = await client.wait_for("message", check=lambda message: message.author == ctx.author)
    msgContent = str(msg.content)
    msg = msgContent.split()
    combatList = []
    initDict = {}
    characterList = loadCharacters(channel, ctx)
    print(characterList)
    for i in range(len(msg)):
        if msg[i] in characterList:
            combatList.append(msg[i])
        else:
            await ctx.send("This character is not registered in our system!")
            return

    for i in range(len(combatList)):
        dex = (characterList[combatList[i]])
        print(dex[combatList[i]]["dex"])
        dex = dex[combatList[i]]["dex"]
        roll = random.randint(1, 20)
        mod = (dex / 2)
        mod = math.floor(mod)
        result = roll + mod
        await ctx.send(str(author.mention) + " rolled a " + str(result) + " for initative!")
        initDict[str(dex)] = str(result)

    newInitDict = sorted(initDict, reverse=True)

    for i in range(len(newInitDict)):
        newI = i + 1
        await ctx.send(f"{str(newI)}: {combatList[i]}")
        # newInitDict[i]['name']

    for j in range(len(newInitDict)):
        await ctx.send(f"{str(newInitDict[i])}, it is your turn!")
        msg = await client.wait_for("message", check=lambda message: message.author == ctx.author)
        j += 0


client.run('Token')

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


def deltaXp(channel, character, operation, quantity):
    # do stuff
    channel = str(channel)
    character = str(character)
    quantity = int(quantity)
    if(operation == "add" or "sub"):
        # do it
        with open('xp.json', 'r') as f:
            allChr = json.load(f)
            allChr = json.loads(allChr)
        if(channel in allChr):
            channelDict = allChr[channel]
            if(character in channelDict):
                workingDict = channelDict[character]
                if(operation == 'add'):
                    workingDict['xp'] += quantity
                elif(operation == 'sub'):
                    workingDict['xp'] -= quantity
                channelDict[character] = workingDict
                allChr[channel] = channelDict
                with open('xp.json', 'w') as file:
                    dump = allChr
                    finaldump = json.dumps(dump)
                    json.dump(finaldump, file, indent=4)
            else:
                # create an empty xp dict and perform the operation
                channelDict.update({character: {'xp': 0, 'level': 0}})
                workingDict = channelDict[character]
                if(operation == 'add'):
                    workingDict['xp'] += quantity
                elif(operation == 'sub'):
                    workingDict['xp'] -= quantity
                channelDict[character] = workingDict
                allChr[channel] = channelDict
                with open('xp.json', 'w') as file:
                    dump = allChr
                    finaldump = json.dumps(dump)
                    json.dump(finaldump, file, indent=4)
        else:
            # create a channel dictionary
            allChr.update({channel: {"channel_init": "channel_init"}})
            channelDict = allChr[channel]
            channelDict.update({character: {'xp': 0, 'level': 0}})
            workingDict = channelDict[character]
            if(operation == 'add'):
                workingDict['xp'] += quantity
            elif(operation == 'sub'):
                workingDict['xp'] -= quantity
            channelDict[character] = workingDict
            allChr[channel] = channelDict
            with open('xp.json', 'w') as file:
                dump = allChr
                finaldump = json.dumps(dump)
                json.dump(finaldump, file, indent=4)
        return True
    else:
        return False


def loadXpLevels(channel, character):
    channel = str(channel)
    character = str(character)
    with open('xp.json', 'r') as f:
        allChr = json.load(f)
        allChr = json.loads(allChr)
    if(channel in allChr):
        channelDict = allChr[channel]
        if(character in channelDict):
            charDict = channelDict[character]
            charXp = charDict['xp']
            charLvl = charDict['level']
            returnList = [charXp, charLvl]
            return returnList
        else:
            return "No such character associated with this channel"
    else:
        return "No characters associated with this channel"


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
    channel = ctx.channel.id
    await ctx.send("Hello! To create a new player, type **p**. To enter data for an enemy, type **e**")
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
async def changexp(ctx):
    # dewit
    channel = str(ctx.channel.id)
    await ctx.send('Which character\'s xp count is being changed?')
    character = await client.wait_for("message", check=lambda message: message.author == ctx.author)
    character = str(character.content)
    await ctx.send('Are you adding (\'add\') or subtracting (\'sub\') from your xp count?')
    res1 = await client.wait_for("message", check=lambda message: message.author == ctx.author)
    res1 = res1.content
    res1 = res1.lower()
    if(res1 == 'add'):
        await ctx.send('How much xp do you want to add?')
        res2 = await client.wait_for("message", check=lambda message: message.author == ctx.author)
        res2 = res2.content
        try:
            intres2 = int(res2)
        except:
            await ctx.send('Make sure to enter a number.')
            return
        if(deltaXp(channel, character, 'add', intres2) == True):
            await ctx.send('The xp change was successful.')
        else:
            await ctx.send('The xp change failed. Make sure you are typing your character\'s name correct (caps count!) or that you have this character registered in this channel.')

    elif(res1 == 'sub'):
        # ask amount
        await ctx.send('How much xp do you want to add?')
        res2 = await client.wait_for("message", check=lambda message: message.author == ctx.author)
        res2 = res2.content
        try:
            intres2 = int(res2)
        except:
            await ctx.send('Make sure to enter a number.')
            return
        if(deltaXp(channel, character, 'sub', intres2) == True):
            await ctx.send('The xp change was successful.')
        else:
            await ctx.send('The xp change failed. Make sure you are typing your character\'s name correctl (caps count!) or that you have this character registered in this channel.')
    else:
        await ctx.send('Please enter either \'add\' or \'sub\'.')


@client.command(pass_context=True)
async def xp(ctx, *character):
    try:
        charName = str(character[0])
    except:
        await ctx.send("Please call the function as follows: *xp charactername")
        return
    returnList = loadXpLevels(str(ctx.channel.id), charName)
    # try:
    xp = returnList[0]
    try:
        throwaway = int(xp)
        throwaway += 0
    except:
        await ctx.send(returnList)
        return
    await ctx.send(charName + " has " + str(xp) + " xp.")


@client.command(pass_context=True)
async def level(ctx, *character):
    # dewit
    channel = str(ctx.channel.id)
    try:
        charName = str(character[0])
    except:
        await ctx.send("Please call the function as follows: *level charactername")
        return
    returnList = loadXpLevels(channel, charName)
    xpLevel = returnList[0]
    try:
        throwaway = int(xpLevel)
        throwaway += 0
    except:
        await ctx.send(returnList)
        return

    xpList = [300, 900, 2700, 6500, 14000, 23000, 34000, 48000, 64000, 85000,
              100000, 120000, 140000, 165000, 195000, 225000, 265000, 305000, 355000]
    for i in xpList:
        if int(xpLevel) < int(xpList[i]):
            level = i + 1
        await ctx.send(charName + " is level " + str(level) + ".")


@client.command(pass_context=True)
async def editstats(ctx, character):
    # new stats
    author = str(ctx.author)
    channel = str(ctx.channel.id)
    character = str(character)
    channelDict = loadCharacters(channel, ctx)
    if(character in channelDict):
        # work
        try:
            charDict = channelDict[character][character]
        except:
            await ctx.send("No character \"" + character + "\" found.")
            return
        print(charDict)
        if(charDict['author'] == author):
            # work
            await ctx.send(
                "Which stat do you want to change? (enter \'str\', \'dex\', \'con\', \'int\', \'wis\', or \'chr\').")
            msg = await client.wait_for("message", check=lambda message: message.author == ctx.author)
            msg = msg.content
            if(msg == 'str' or 'dex' or 'con' or 'int' or 'wis' or 'chr'):
                stat = msg
                await ctx.send("How much would you like to increase the statistic?")
                deltaStat = await client.wait_for("message", check=lambda message: message.author == ctx.author)
                deltaStat = deltaStat.content
                charDict[stat] += int(deltaStat)
                saveDict = {character: charDict}
                print(charDict)
                delCharacter(channel, character)
                saveCharacter(character, channel, saveDict)
                await ctx.send(str(msg) + " stat changed to " + str(charDict[stat]) + ".")
            else:
                await ctx.send("Please enter a valid stat in a 3-character string.")
        else:
            await ctx.send("You can only delete your own character.")
    else:
        await ctx.send("No such character " + character + " found.")
        return


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
            await ctx.send(str(author.mention) + ' rolled a ' + str(random.randint(1, paramSplit[1])) + '. :game_die:')
        else:
            if("d" in paramSplit or "D" in paramSplit):
                # nomial path
                itemstr = ''
                for item in paramSplit:
                    itemstr += str(item)
                splitItem = itemstr.split('d')
                roll = 0
                for rollnum in range(int(splitItem[0])):
                    roll += random.randint(1, int(splitItem[1]))
                    rollnum += 0
                await ctx.send(str(author.mention) + ' rolled a ' + str(roll) + '. :game_die:')
            else:
                await ctx.send('Please format your roll correctly: \"[number of rolls]d[die type]\". i.g. \"5d8\".*r')


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
        dex = combatList[i]
        print(dex)
        d = dex[i]["dex"]
        print(d)
        roll = random.randint(1, 20)
        mod = (d / 2)
        mod = math.floor(mod)
        result = roll + mod
        print(result)
        await ctx.send(str(author.mention) + " rolled a " + str(result) + " for initative!")
        initDict[str(dex)] = str(result)

    newInitDict = sorted(initDict, reverse=True)

    for i in range(len(newInitDict)):
        newI = i + 1
        await ctx.send(f"{str(newI)}: {combatList[i]}")

    for j in range(len(newInitDict)):
        await ctx.send(f"{str(newInitDict[i][newInitDict[msg[i]]])}, it is your turn!")
        msg = await client.wait_for("message", check=lambda message: message.author == ctx.author)
        j += 0


client.run('token here')

import discord
from discord.ext import commands
import json
import random
import string

client = commands.Bot(command_prefix='*')
client.remove_command('help')


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


client.run('Token')

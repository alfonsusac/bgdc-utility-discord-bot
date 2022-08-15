import discord
from discord.ext import commands, tasks
# from discord_slash import SlashCmd, SlashCtx
import os
import random
from itertools import cycle
import json

# chagneable prefixes
def get_prefix(client, message):
    with open('./data/prefixes.json','r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix)
client.remove_command('help')

@client.event
async def on_ready():
    print("Bot is ready.")
    await client.change_presence(status=discord.Status.online)
    # # to start status
    # change_status.start()


# # Creating tasks
# status = cycle(['Status 1','Status 2'])
# # change status for each 10 seconds
# @tasks.loop(seconds=10)
# async def change_status():
#     await client.change_presence(activity=discord.Game(next(status)))

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    print(f'Cogs {extension} loaded!')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    print(f'Cogs {extension} unloaded!')

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    print(f'Cogs {extension} reloaded!')

# to list down all existing cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run('Insert Token Here')

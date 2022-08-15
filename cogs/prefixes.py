import discord
from discord.ext import commands
import json

class Prefixes(commands.Cog):

    def __init__(self, client):
        self.client = client

    # creating event for adding to server databases on join
    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        print('adding serverid to prefixes.json...')
        with open('./data/prefixes.json','r') as f:
            prefixes = json.load(f)

        prefixes[str(guild.id)] = '.'

        with open('./data/prefixes.json','w') as f:
            json.dump(prefixes, f, indent=4)
        print('finished adding serverid to prefixes.json!')

    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        with open('./data/prefixes.json','r') as f:
            prefixes = json.load(f)

        prefixes.pop(str(guild.id))

        with open('./data/prefixes.json','w') as f:
            json.dump(prefixes, f, indent=4)

    @commands.command()
    async def changeprefix(self, ctx, prefix):
        with open('./data/prefixes.json','r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open('./data/prefixes.json','w') as f:
            json.dump(prefixes, f, indent=4)


def setup(client):
    client.add_cog(Prefixes(client))


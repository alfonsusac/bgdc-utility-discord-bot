import discord
import random
from discord.ext import commands


class Messages(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Events
    # decorator for the commands event USED inside Cog
    @commands.Cog.listener()
    # does not take any arguement but take one inside cog
    async def on_ready(self): 
      print('Bot is online.')

    #Commands
    @commands.command()
    async def ping(self, ctx):
      await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

    @commands.command(aliases=['8ball','eightball'])
    async def _8ball(self, ctx, *, question):
      responses = ["It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes - definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."]
      await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount):
      # async def clear(self, ctx, amount=5):
      await ctx.channel.purge(limit=int(amount))

    # creating checks
    def is_it_arufon(ctx):
      return ctx.author.id == 194128415954173952

    @commands.command()
    @commands.check(is_it_arufon)
    async def Arufon(self, ctx):
      # async def clear(self, ctx, amount=5):
      await ctx.send(f'Hi im {ctx.author}')

    # command specific error
    # @clear.error
    # async def clear_error(self, ctx, error):
    #   await ctx.send('Please specify an amount of messages to delete.')

# setup function to allow cog to connect to bot
def setup(client):
    # running method of client add_cog, passing in Messages Class
    client.add_cog(Messages(client))

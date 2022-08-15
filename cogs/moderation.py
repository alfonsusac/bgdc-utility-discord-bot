import discord
from discord.ext import commands

class Moderation(commands.Cog):
  
  def __init__(self, client):
    self.client = client

  # @commands.command()
  # async def kick(self, ctx, member : discord.Member, *, reason=None):
  #   # * = any parameter after member will be added to reason
  #   await member.kick(reason=reason)

  # @commands.command()
  # async def ban(self, ctx, member : discord.Member, *, reason=None):
  #   # * = any parameter after member will be added to reason
  #   await member.ban(reason=reason)
  #   await ctx.send(f'Banned {member.mention}')

  # @commands.command()
  # async def unban(self, ctx, *, member):
  #   banned_users = await ctx.guild.bans() #banentry (named tuple containing user object + reason)
  #   # Lucas#1234
  #   member_name, member_discriminator = member.split('#') # also a tuple
    
  #   for ban_entry in banned_users:
  #     user = ban_entry.user
  #     if (user.name, user.discriminator) == (member_name, member_discriminator):
  #       await ctx.guild.unban(user)
  #       await ctx.send(f'Unbanned {user.name}#{user.discriminator}')

def setup(client):
    client.add_cog(Moderation(client))
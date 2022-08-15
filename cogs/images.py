import discord
from discord.ext import commands, tasks
from PIL import Image, ImageDraw, ImageFont


class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "ping3",
                      description = "description",
                      enabled = False,
                      )
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def samplecommand2(self, ctx):
        await ctx.send("template command 2")

    @commands.command(name  = "slap",
                    #   aliases = ['command1', 'command2'], # Lists or Tuples
                    #   usage = ".ping2 <args>",
                    #   help  = "Long Help Text",
                    #   brief = "Brief Help Text", 
                    #   callback = print("Callback"), #??
                    #   description = "description",
                      enabled = True,
                      # cog = None,
                      # parent = None,
                      )
    # @commands.guild_only()
    # @commands.has_permissions()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def slap(self, ctx, *, namestr):
        print("Slapping", namestr,"!")
        # await ctx.message.delete()

        slapimg = Image.open(r'.\data\slap_out.jpg')
        draw = ImageDraw.Draw(slapimg)
        font = ImageFont.truetype(r'.\data\Calibri Regular.ttf', size=22)
        message = namestr.upper()
        W, H = (250, 250)
        w, h = draw.textsize(message)
        pos = ((300-w)/2,228)
        color = 'rgb(0,0,0)'

        draw.text(pos,message,fill=color,font=font)
        
        slapimg.save('./data/slap_out_temp.jpg',optimize=True)
        await ctx.send(file=discord.File('./data/slap_out_temp.jpg'))

    @slap.error
    async def clear_error(self, ctx, error):
        await ctx.send(error)

def setup(bot):
    bot.add_cog(Images(bot))
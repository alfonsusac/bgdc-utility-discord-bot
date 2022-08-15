import discord
from discord.ext import commands
import json
import string

class Mokou(commands.Cog):

    

    def __init__(self, client):
        self.client = client

    @commands.command(name="m", aliases=['mokou','mok','mo','moko'])
    @commands.cooldown(3, 10, commands.BucketType.member)
    async def mokou(self, ctx, *, imgstr):

        with open('./data/mokoutext.json','r') as f:
            datas = json.load(f)
        
        args = imgstr.split(' ')
        if args[0] == "browse":
            i = 0
            if len(args) == 2:
                i = int(args[1])-1
                if i > 9:
                    i = 9
            else:
                i = 0
            showlist = list(datas.keys())[(i*50):((i*50)+50)]
            print("\n".join(showlist))
            await ctx.send(f"Browsing page {i+1} of 10, showing 50 images\n> type `.m browse {i+2}` to see next page\n\nList of available images:\n> `"+"`, `".join(showlist)+"`")
        else:
            delchars = r"-'..?、[~…!,，()]+“_=<>/””"
            inputprocessed = imgstr.lower().translate({ord(c): None for c in (string.whitespace+delchars)}).replace('|','i').replace('1','i').lower()
            output = ""
            try:
                output = datas[inputprocessed]
                await ctx.send(file=discord.File(f'./data/mokou/{output}'))
            except:
                print(f'searching {imgstr}')
                # keys = datas.keys()
                result = [i for i in datas.keys() if inputprocessed in i]
                print(result)
                message = ""
                if len(result) == 0:
                    message = "```Mokou \""+imgstr+"\" Not found!```"
                elif len(result) == 1:
                    await ctx.send(file=discord.File(f'./data/mokou/{datas[result[0]]}'))
                    return
                else:
                    firstfive = result[:10]
                    message = "```.m "+"\n.m ".join(firstfive)+"```"

                if ctx.channel.id == 657888883052249088:
                    await ctx.send(message)
                else:
                    botchanel = []
                    try:
                        botchannel = self.client.get_channel(657888883052249088)
                        await botchannel.send(f"{ctx.message.author.mention}: {message}")
                    except:
                        await ctx.send("Please search mokou images in bot-commands")                
                    await ctx.message.delete()

    @mokou.error
    async def clear_error(self, ctx, error):
        await ctx.send(error)

def setup(client):
    client.add_cog(Mokou(client))
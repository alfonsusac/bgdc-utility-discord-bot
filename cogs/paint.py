import discord
from discord.ext import commands
from collections import namedtuple
import json
import datetime

def write_canvas_to_json(Canvas):
    print('adding canvases to canvases.json...')
    with open('./data/canvases.json','r') as f:
        canvases = json.load(f)

    canvases[Canvas.embedID] = Canvas

    with open('./data/canvases.json','w') as f:
        json.dump(canvases, f, indent=4, default=lambda x: x.__dict__)
    print('finished adding canvases to canvases.json!')

def removedata(embedID):
    with open('./data/canvases.json','r') as f:
        canvases = json.load(f)

    canvases.pop(str(embedID))

    with open('./data/canvases.json','w') as f:
        json.dump(canvases, f, indent=4)

class Canvas():
    def __init__(self, author, embedID, size=(8,8), title='', pixels=[], cursor=0):
        self.title = title
        self.size = size
        self.pixel = self.size[0]*self.size[1]
        self.pixels = pixels 
        self.embedID = embedID
        self.cursor = cursor
        self.author = author
        print(f"A canvas is created from {embedID}")

    def addpixel(self, color, author):
        self.pixels[int(self.cursor/self.size[0])][self.cursor%self.size[0]] = color
        self.cursor += 1
        print(self.author)
        self.author.append(author) if author not in self.author else self.author
        print(self.author)
        write_canvas_to_json(self)

    def remame(self, title):
        self.title = title
        return title

def get_canvas(messageid):
    with open('./data/canvases.json','r') as f:
        rawdata = json.load(f)
    canvas = Canvas(rawdata[messageid]["author"],messageid,rawdata[messageid]["size"],title=rawdata[messageid]["title"],pixels=rawdata[messageid]["pixels"],cursor=rawdata[messageid]["cursor"])
    return canvas

def get_number_from_color(emoji):
    colorList = ['⬜','⬛','⬜','🟥','🟧','🟨','🟩','🟦','🟪','lilin']
    colorIdx = [0,1,2,3,4,5,6,7,8,9]
    colorDict = dict(zip(colorList,colorIdx))
    return colorDict[emoji]

def get_color_from_number(idx):
    colorList = ['⬜','⬛','⬜','🟥','🟧','🟨','🟩','🟦','🟪','<:lilin:828522371782148137>']
    return colorList[idx]

def pixeldata_to_emojistring(pixellist,cursor,pixel):
    emojistring = ""
    curr = 0
    for rows in pixellist:
        for i in rows:
            curr += 1
            if curr == cursor+1 and cursor <= pixel:
                emojistring += "🖌"
            else:
                emojistring += get_color_from_number(i)
        emojistring += '\n'
    return emojistring

class Paint(commands.Cog):
    
    def read_json_to_canvas(self):
        with open('./data/canvases.json','r') as f:
            rawdata = json.load(f)
        canvaskeylist = list(rawdata.keys())
        # print(canvaskeylist)
        canvasobjdict = {}
        for key in canvaskeylist:
            canvasobjdict[key] = Canvas(rawdata[key]["author"],key,rawdata[key]["size"],title=rawdata[key]["title"],pixels=rawdata[key]["pixels"],cursor=rawdata[key]["cursor"])
        # print(canvasobjdict.keys())
        return canvasobjdict
    
    def __init__(self, client):
        self.client = client
        self.canvases = self.read_json_to_canvas()
        self.paints = len(self.canvases)
        self.embedTitle = f"untitled canvas #{str(len(self.canvases)+1)}"
        self.embedDescription = "React to the colors to paint a colors\nDouble click if you have already reacted the color\n\n"
        # print(self.canvases.keys())
        # print(type(self.canvases['799682221174161418']))

    @commands.group()
    async def paint(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("To create new canvas, type ```.paint new```")

    @paint.command()
    async def new(self, ctx, size=8):
        
        # Constants
        if size > 8:
            size = 8
        if size < 2:
            size = 2
        squareside = size


        # Creating new Display Array
        bls = "⬜"
        pixels = [[bls]*squareside for i in range(squareside)]
        pixels[0][0] = "🖌"
        tile = ""
        for i in pixels:
            for j in i:
                tile += j
            tile += '\n'

        # Creating new Canvas Data
        pixelsdata = [[0]*squareside for i in range(squareside)]

        # Send new embed
        await ctx.send("Creating new canvas...")
        self.paints += 1
        embed = discord.Embed(title=self.embedTitle, description=self.embedDescription+tile+'\n', color=0xD3D3D3)
        embed.add_field(name="Status", value=f"On going | Contributors: 1", inline=False)
        embed.set_footer(text="BGDCBot")
        embedObj = await ctx.send(embed=embed)

        # Create new Canvas
        newcanvas = Canvas([ctx.message.author.id], embedObj.id, size=(squareside, squareside), pixels=pixelsdata,title=self.embedTitle)
        self.canvases[str(newcanvas.embedID)] = newcanvas
        write_canvas_to_json(newcanvas)
        print(self.canvases.keys())

        # React with Emojis
        emojis = ['⬛','⬜','🟥','🟧','🟨','🟩','🟦','🟪','<:lilin:828522371782148137>']
        for emoji in emojis:
            await embedObj.add_reaction(emoji)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Check if react by user
        if not payload.member.bot:
            print(f"{payload.member.id} Reacted!")
            # Get Channel Object
            channel = self.client.get_channel(payload.channel_id)
            # Get Reaction Object
            reaction = payload.emoji
            messageid = payload.message_id
            # Check if reacted message is in the database of canvases
            if str(messageid) in self.canvases:
                # Get message and canvas object
                msg = await channel.fetch_message(messageid)
                canvas = get_canvas(str(messageid))

                # Add a color to the canvas
                colorIdx = get_number_from_color(reaction.name)
                canvas.addpixel(colorIdx, payload.user_id)
                print(canvas.pixels)

                # Add to Database
                self.canvases[str(canvas.embedID)] = canvas
                write_canvas_to_json(canvas)
                
                print(canvas.author)
                # Send Embed
                new_tile = pixeldata_to_emojistring(canvas.pixels,canvas.cursor,canvas.pixel)
                # If the canvas is done
                if canvas.cursor >= canvas.pixel:
                    # Awaiting Title
                    new_embed = discord.Embed(title=f"{canvas.title}", description="Your artwork is now done!\nType in the chat below to enter your title!\n\n"+new_tile, color=0xD3D3D3)
                    new_embed.add_field(name="Status", value=f"Waiting for title.. | Contributors: {len(canvas.author)}", inline=False)
                    new_embed.set_footer(text="BGDC Paint Bot")
                    new_embedObj = await msg.edit(embed=new_embed)

                    authors = "<@"+"> <@".join([str(elem) for elem in canvas.author])+">"
                    authorsnl = "<@"+">\n<@".join([str(elem) for elem in canvas.author])+">"
                    
                    titlelist = []
                    # memberchecklist = { i:False for i in canvas.author }
                    # def check(message):
                    #     return message.channel == channel
                    for author in canvas.author:
                        tempmsg = await channel.send(f'<@{author}> : Quick! Type the title in the chat below!')
                        titlepart = await self.client.wait_for('message', check=lambda message: message.author.id == author and message.channel == channel)
                        titlelist.append(titlepart.content)
                        await tempmsg.delete()
                        print(titlelist)
                    newtitle = " ".join(titlelist)


                    print(newtitle)

                    now = datetime.datetime.now()
                    print(now.year, now.month, now.day, now.hour, now.minute, now.second)

                    new_embed = discord.Embed(title=f" ", description=f"***{newtitle}***. {now.year}. Pixel on canvas. {canvas.size[0]} in. x {canvas.size[1]} in. Museum of Modern Digital Art\n\n"+new_tile, color=0xD3D3D3)
                    new_embed.add_field(name="Status", value=f"Finished | Contributors: {len(canvas.author)}\n"+authorsnl, inline=False)
                    new_embed.set_footer(text="BGDC Paint Bot")
                    await msg.delete()
                    await channel.send(embed=new_embed)

                    self.canvases.pop(str(canvas.embedID))
                    removedata(str(canvas.embedID))

                else:
                    # Send Embed
                    new_embed = discord.Embed(title=f"{canvas.title}", description="React to the colors to add colors\nDouble click if you have already reacted\n\n"+new_tile, color=0xD3D3D3)
                    new_embed.add_field(name="Status", value=f"On going | Contributors: {len(canvas.author)}", inline=False)
                    new_embed.set_footer(text="BGDC Paint Bot")
                    new_embedObj = await msg.edit(embed=new_embed)
                
def setup(client):
    client.add_cog(Paint(client))

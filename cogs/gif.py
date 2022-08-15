import discord
import requests
import io
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import PIL

class Gif(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def pat(self, ctx, member : discord.Member ):
        await ctx.send(member.id)

        # Saving User PFP into PIL Images
        imagebuffer = io.BytesIO()
        await member.avatar_url.save(imagebuffer, seek_begin=True)
        userpfp = Image.open(imagebuffer)
        w = userpfp.size[0]
        h = userpfp.size[1]

        # Opening Headpat GIF
        hpwidth = 112
        hpheight = 112
        headpatim = []
        for i in range(1,6):
            fn = Image.new('RGBA', (w,h), color=(0,0,0,0))
            im = Image.new('RGBA', (hpwidth,hpheight),(255,0,0,0))
            im.paste(Image.open("./data/gifs/pats/"+str(i)+".gif"),(0,0))
            # im.show()
            # headpatim.append(Image.open("./data/gifs/pats/"+str(i)+".gif"))
            # headpatim.append(Image.open("./data/gifs/pats/"+str(i)+".gif"))
            headpatim.append(im)
            headpatim.append(im)

        headpatim[0].save('data/gifs/pats/template_rescaled.gif',
                            save_all=True, append_images=headpatim[1:], optimize=False, duration=120, loop=0,transparency=0)

        # for frame in range(0,headpat.n_frames):
        finframes = Image.new('RGBA',userpfp.size,color=(0,0,0,0))
        finframes.paste(userpfp.resize((int(w*0.5),int(h))),box=(int(w/2),int(h/2)))
        finframes.paste(headpat.seek(1),(0,0))
        finframes.show()

        imagebuffer.flush()
        # finalimgs = []




def setup(client):
    client.add_cog(Gif(client))


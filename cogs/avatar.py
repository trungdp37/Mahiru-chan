import discord
import datetime
from discord.ext import commands

class Avatar(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @commands.Cog.listener()
    async def on_ready(self):
        print('avatar.py is ready!')
    
    @commands.command()
    async def avatar(self, ctx, member : discord.Member = None):
            if not member:
                member = ctx.message.author    
            now = datetime.datetime.now()                            
            embed_message = discord.Embed(color=discord.Color.green())        
            embed_message.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar)
            embed_message.set_image(url=member.display_avatar)
            embed_message.add_field(name="Avatar", value=f"Một chiếc avatar oách xà lách đến từ {member}.", inline=True)
            embed_message.set_footer(text=f"Datetime | {now:%Y-%m-%d %H:%M}")
            
            await ctx.send(embed=embed_message)
    
async def setup(client):
    await client.add_cog(Avatar(client))
import discord
from discord.ext import commands

class Goodbye(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @commands.Cog.listener()
    async def on_ready(self):
        print('goodbye.py is ready!')
    
    @commands.command(aliases=["b"])
    async def bye(self, ctx):        
        await ctx.send(f"Gặp lại sau nhé!")
    
async def setup(client):
    await client.add_cog(Goodbye(client))
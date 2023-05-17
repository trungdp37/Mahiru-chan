import discord
from discord.ext import commands

class Hello(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @commands.Cog.listener()
    async def on_ready(self):
        print('hello.py is ready!')
    
    @commands.command(aliases=["h"])
    async def hello(self, ctx):        
        await ctx.send(f"Chào bạn!")
    
async def setup(client):
    await client.add_cog(Hello(client))
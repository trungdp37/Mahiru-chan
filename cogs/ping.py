import discord
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @commands.Cog.listener()
    async def on_ready(self):
        print('ping.py is ready!')
    
    @commands.command(aliases=["p"])
    async def ping(self, ctx):
        bot_latency = round(self.client.latency * 1000)
        
        await ctx.send(f"{bot_latency} ms.")
    
async def setup(client):
    await client.add_cog(Ping(client))
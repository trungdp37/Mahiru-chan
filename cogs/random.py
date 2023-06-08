import random
import discord  
from discord.ext import commands

class Randomizer(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('random.py is ready!')
        
    @commands.command(name="choose")
    async def choose(self, ctx, *choices):
        """Chọn một trong các lựa chọn được đưa ra."""
        if not choices:
            await ctx.send("Không thể thực hiện lệnh. Hình như bạn nhập thiếu gì rồi thì phải...")
            return
        await ctx.send(f"Tớ chọn cậu, **{random.choice(choices)}**!")
        
async def setup(client):
    await client.add_cog(Randomizer(client))
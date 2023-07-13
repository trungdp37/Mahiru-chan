import discord
from discord.ext import commands
import json
import math
import asyncio
import random
import datetime

class Level(commands.Cog):
    def __init__(self, client):
        self.client = client 
        self.client.loop.create_task(self.save())
        
        with open("json/users.json", "r") as f:
            self.users = json.load(f)
    
    def level_up(self, author_id):
        current_exp = self.users[author_id]["Experience"]
        current_lvl = self.users[author_id]["Level"]
        
        if current_exp >= math.ceil((6 * (current_lvl ** 4)) / 2.5):
            self.users[author_id]["Level"] += 1
            return True
        else:
            return False 
            
    async def save(self):
        await self.client.wait_until_ready()
        while not self.client.is_closed():
            with open("json/users.json", "w") as f:
                json.dump(self.users, f, indent=4)
                
            await asyncio.sleep(5)
                
    @commands.Cog.listener()
    async def on_ready(self):
        print('level_system.py is ready!')
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.client.user.id:
            return
        
        author_id = str(message.author.id)
        
        if not author_id in self.users:
            
            self.users[author_id] = {}
            self.users[author_id]["Level"] = 1
            self.users[author_id]["Experience"] = 0   
        
        random_number = random.randint(5, 15)
        self.users[author_id]["Experience"] += random_number
        
        """ if self.level_up(author_id):
            lvlup_embed = discord.Embed(title=f"Lên cấp!", color=discord.Color.random())
            lvlup_embed.add_field(name="Chúc mừng", value=f"{message.author.mention} đã lên level {self.users[author_id]['Level']}!")
            
            channel_id = 750745118369251480 # thay ID kênh muốn gửi Embed vào
            channel = message.guild.get_channel(channel_id)
            await channel.send(embed=lvlup_embed) """
            
    @commands.command()
    async def level(self, ctx, user: discord.User = None):
        if user is None:
            user = ctx.author
        elif user is not None:
            user = user
        now = datetime.datetime.now()   
        lvl_embed = discord.Embed(title=f"Level", color=discord.Color.random())
        lvl_embed.add_field(name="Level", value=self.users[str(user.id)]["Level"])
        lvl_embed.add_field(name="Experience", value=f"{self.users[str(user.id)]['Experience']}/{math.ceil((6 * (self.users[str(user.id)]['Level'] ** 4)) / 2.5)}")
        lvl_embed.set_footer(text=f"Datetime | {now:%Y-%m-%d %H:%M}")
        
        await ctx.send(embed=lvl_embed)
           
async def setup(client):
    await client.add_cog(Level(client))
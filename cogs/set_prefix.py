import discord
import json
from discord.ext import commands

class Prefix(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @commands.Cog.listener()
    async def on_ready(self):
        print('set_prefix.py is ready!')   
    
    @commands.command()
    async def setprefix(self, ctx, *, newstr: str):
        with open("json/prefixes.json", "r") as f:
            prefix = json.load(f)
        prefix[str(ctx.guild.id)] = newstr
        
        with open("json/prefixes.json", "w") as f:
            json.dump(prefix, f, indent=4)
        
        await ctx.send(f"Đã chuyển prefix sang {newstr} rồi ạ!")
        
    @setprefix.error
    async def setprefix_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Không thể thực hiện lệnh. Hình như bạn nhập thiếu gì rồi thì phải...")
        
async def setup(client):
    await client.add_cog(Prefix(client))
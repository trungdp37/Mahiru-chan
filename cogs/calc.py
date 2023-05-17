import discord
import math
from discord.ext import commands

class Calc(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @commands.Cog.listener()
    async def on_ready(self):
        print('calc.py is ready!')
    
    @commands.command(aliases=["c"])
    async def calc(self, ctx, *, expression):
        try:
            result = eval(expression)
            await ctx.send(f"Kết quả là {result}.")
        except:
            await ctx.send("Biểu thức này em không thể tính được! Vui lòng nhập một biểu thức khác.")
    
    @calc.error
    async def calc_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Không thể thực hiện lệnh. Hình như bạn nhập thiếu gì rồi thì phải...")
                       
async def setup(client):
    await client.add_cog(Calc(client))
import discord
from discord.ext import commands

from cogs.System.matheval import *

class Calc(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @commands.Cog.listener()
    async def on_ready(self):
        print('calc.py is ready!')
    
    @commands.command(aliases=["c"])
    async def calc(self, ctx, *, expr):
        try:
            expr = expr.replace("^", "**")  # Thay thế toán tử mũ "^" thành "**"
            expr = expr.lower()  # Chuyển các ký tự in hoa sang in thường

            # Tính toán biểu thức và gửi kết quả
            result = eval(expr, {"__builtins__": None}, {"sin": math.sin, "cos": math.cos, "tan": math.tan, "sqrt": math.sqrt, "log10": math.log10, "log2": math.log2, "log": math.log, "pi": math.pi, "e": math.e, "exp": math.exp, "pow": pow, "abs": abs})
            await ctx.send(f"Kết quả là {result}.")

        except:
            await ctx.send("Biểu thức này em không thể tính được! Vui lòng nhập một biểu thức khác.")
    
    @calc.error
    async def calc_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Không thể thực hiện lệnh. Hình như bạn nhập thiếu gì rồi thì phải...")
                       
async def setup(client):
    await client.add_cog(Calc(client))
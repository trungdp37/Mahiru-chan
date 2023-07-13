import datetime
import discord
from discord.ext import commands
from googletrans import Translator

class Translate(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('trans.py is ready!')

    @commands.command(name='trans', aliases=['translate'])
    async def translate_text(self, ctx, *, text):
        translator = Translator()
        translated_text = translator.translate(text, dest='vi').text
        
        now = datetime.datetime.now() 

        embed = discord.Embed(title='Dịch', color=0x00ff00)
        embed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar)
        embed.add_field(name='Tiếng Anh', value=text, inline=False)
        embed.add_field(name='Tiếng Việt', value=translated_text, inline=False)
        embed.set_footer(text=f"Datetime | {now:%Y-%m-%d %H:%M}")
        await ctx.send(embed=embed)
        
        
    @translate_text.error
    async def trans_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Không thể thực hiện lệnh. Hình như bạn nhập thiếu gì rồi thì phải...")

async def setup(client):
    await client.add_cog(Translate(client))
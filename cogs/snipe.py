import discord
from discord.ext import commands


class Snipe(commands.Cog):
    def __init__(self, client):
        self.client = client 
        self.sniped_messages = {}
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('hello.py is ready!') 
        
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at, message.attachments)
        
    @commands.command()
    async def snipe(self, ctx):
        try:
            contents, author, channel_name, time, attachments = self.sniped_messages[ctx.guild.id]
        except:
            await ctx.channel.send("Không có tin nhắn nào bị xoá.")
            return

        embed = discord.Embed(description=contents, timestamp=time)
        embed.set_author(name=f"{author.name}#{author.discriminator}")
        embed.set_footer(text=f"Trong kênh {channel_name}")
    
        if len(attachments) > 0:
            file = attachments[0]
            if file.url.lower().endswith(("jpg", "jpeg", "png", "gif")):
                embed.set_image(url=file.url)

        await ctx.channel.send(embed=embed)
         
        
async def setup(client):
    await client.add_cog(Snipe(client))
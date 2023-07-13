import datetime
import discord
from discord.ext import commands

class ServerInfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def server(self, ctx):
        count = 0
        for member in ctx.guild.members:  # .members was added
          if member.status != discord.Status.offline:
            count += 1
        now = datetime.datetime.now()
        member_count = len(ctx.guild.members)
        embed = discord.Embed(title="Thông tin server", description=f"Tên server: {ctx.guild.name}", color=discord.Color.blue())
        embed.set_thumbnail(url=ctx.guild.icon)
        embed.add_field(name="Số lượng thành viên", value=member_count, inline=False)
        embed.add_field(name="Số lượng member active", value=count, inline=False)
        embed.add_field(name="Ngày thành lập", value=ctx.guild.created_at.strftime("%d/%m/%Y"), inline=False)
        embed.add_field(name="Admin", value=ctx.guild.owner.display_name, inline=False)
        embed.set_footer(text=f"Datetime | {now:%Y-%m-%d %H:%M}")
        
        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(ServerInfo(client))
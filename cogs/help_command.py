import discord
from discord.ext import commands
from operator import attrgetter

class Helpcmd(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.help_fields = [
    {"name": "add", "value": "Tự thêm biểu thức riêng của mình.", "inline": False},
    {"name": "avatar", "value": "Hiện avatar của một user trong server.", "inline": False},
    {"name": "calc", "value": "Máy tính dùng để tính toán biểu thức.", "inline": False},
    {"name": "goodbye", "value": "Đơn giản là tạm biệt thui.", "inline": False},
    {"name": "hello", "value": "Đơn giản là chào ai đó thui.", "inline": False},
    {"name": "help", "value": "Hiện các chức năng của em.", "inline": False},
    {"name": "ban", "value": "Ban một user.", "inline": False},
    {"name": "continue", "value": "Tiếp tục phát nhạc.", "inline": False},
    {"name": "kick", "value": "Kick một user.", "inline": False},
    {"name": "leave", "value": "Cho em rời khỏi voice chat.", "inline": False},
    {"name": "loop", "value": "Lặp bài hát đang phát.", "inline": False},
    {"name": "loopqueue", "value": "Lặp cả danh sách bài hát đang phát.", "inline": False},
    {"name": "mute", "value": "Mute một user.", "inline": False},
    {"name": "pause", "value": "Tạm thời dừng phát nhạc.", "inline": False},
    {"name": "play", "value": "Phát nhạc.", "inline": False},
    {"name": "disconnect", "value": "Cho em rời khỏi voice chat.", "inline": False},
    {"name": "stop", "value": "Dừng phát nhạc.", "inline": False},
    {"name": "unban", "value": "Unban một user.", "inline": False},
    {"name": "resume", "value": "Tiếp tục phát nhạc.", "inline": False},
    {"name": "volume", "value": "Chỉnh volume.", "inline": False},
    {"name": "skip", "value": "Skip tới bài tiếp theo.", "inline": False},
    {"name": "search", "value": "Tìm kiếm bài hát muốn phát.", "inline": False},
    {"name": "nowplaying", "value": "Hiện bài hát đang phát.", "inline": False},
    {"name": "queue", "value": "Hiện danh sách bài hát trong hàng chờ.", "inline": False},
    {"name": "shuffle", "value": "Xáo trộn danh sách hàng chờ.", "inline": False},
    {"name": "ping", "value": "Hiện ping của user.", "inline": False},
    {"name": "setprefix", "value": "Setting lại prefix cho server.", "inline": False},
    {"name": "snipe", "value": "Hiện tin nhắn cua user vừa xoá.", "inline": False},
    {"name": "vocabulary", "value": "Hiện một từ vựng jp ngẫu nhiên.", "inline": False},
] 
        self.sorted_fields = sorted(self.help_fields, key=lambda x: x['name'])
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('help_command.py is ready!')
    
    @commands.command()
    async def help(self, ctx):
        help_embed = discord.Embed(title="Các chức năng mà Mahiru-chan có thể làm:", color=discord.Color.random())
        
        help_embed.set_author(name="Mahiru-chan", icon_url=self.client.user.avatar.url)
        for field in self.sorted_fields:
            help_embed.add_field(name=field['name'], value=field['value'], inline=field['inline'])
        help_embed.set_footer(text= f"Requested by {ctx.author}", icon_url=ctx.author.avatar)

        await ctx.send(embed=help_embed)
    
async def setup(client):
    await client.add_cog(Helpcmd(client))
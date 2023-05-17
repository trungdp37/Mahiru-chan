import discord
import asyncio
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @commands.Cog.listener()
    async def on_ready(self):
        print('moderation.py is ready!')
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, count: int):
        await ctx.channel.purge(limit=count)
        message = await ctx.send(f"Đã xoá {count} tin nhắn.")
        await asyncio.sleep(3) # Chờ 3 giây trước khi xoá tin nhắn
        await message.delete() 
    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason"):
        await ctx.guild.kick(member)
        
        conf_embed = discord.Embed(title=f"Đã kick thành công!", color=discord.Color.red())
        conf_embed.add_field(name="Kicked:", value=f"{ctx.author.mention} đã kick {member.mention} khỏi server.", inline=False)
        conf_embed.add_field(name="Lý do:", value=reason, inline=False)  
        
        await ctx.send(embed = conf_embed)
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason"):
        await ctx.guild.ban(member)
        
        conf_embed = discord.Embed(title=f"Đã ban thành công!", color=discord.Color.red())
        conf_embed.add_field(name="Banned: ", value=f"{ctx.author.mention} đã ban {member.mention} khỏi server.", inline=False)
        conf_embed.add_field(name="Lý do: ", value=reason, inline=False)  
        
        await ctx.send(embed = conf_embed)
        
    @commands.command(name="unban")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id):
        user = discord.Object(id=user_id)
        await ctx.guild.unban(user)
        
        conf_embed = discord.Embed(title=f"Đã unban thành công!", color=discord.Color.dark_embed())
        conf_embed.add_field(name="Unbanned: ", value=f"{ctx.author.mention} đã unban <@{user_id}>.", inline=False)
    
        await ctx.send(embed = conf_embed)
        

    @commands.command()
    @commands.has_permissions(manage_roles=True) 
    async def mute(self, ctx, member: discord.Member, duration : int, *, reason="No reason"):
        if duration <= 0:
            await ctx.send("Thời gian mute phải lớn hơn 0!")
            return
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, speak=False, send_messages=False)

        await member.add_roles(muted_role, reason=reason)
        conf_embed = discord.Embed(title=f"Đã mute thành công!", color=discord.Color.red())
        conf_embed.add_field(name="Muted: ", value=f"{ctx.author.mention} đã mute {member.mention} trong {duration} giây.", inline=False)
        conf_embed.add_field(name="Lý do: ", value=reason, inline=False)  
        
        await ctx.send(embed = conf_embed)
        await asyncio.sleep(duration)
        await member.remove_roles(muted_role, reason="Mute time expired")
        await ctx.send(f"{member.mention} đã được unmute.")
        
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Không thể thực hiện lệnh. Hình như bạn nhập thiếu gì rồi thì phải...")
            
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Không thể thực hiện lệnh. Hình như bạn nhập thiếu gì rồi thì phải...")
            
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Không thể thực hiện lệnh. Hình như bạn nhập thiếu gì rồi thì phải...")
    
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Không thể thực hiện lệnh. Hình như bạn nhập thiếu gì rồi thì phải...")
    
    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Không thể thực hiện lệnh. Hình như bạn nhập thiếu gì rồi thì phải...")
        
async def setup(client):
    await client.add_cog(Moderation(client))
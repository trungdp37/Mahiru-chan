import discord  
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta

class Reminder(commands.Cog):
    def __init__(self, client):
        self.client = client
            
    @commands.Cog.listener()
    async def on_ready(self):
        print('reminder.py is ready!')
        
    @commands.command()
    async def remind(self, ctx, time, *, message):
        time_convert = {"s":1, "m":60, "h":3600, "d":86400}
        remind_time = int(time[:-1]) * time_convert[time[-1]]
        
        await ctx.send(f"Đã đặt hẹn giờ thành công. Em sẽ nhắc nhở sau {time}.")
        await asyncio.sleep(remind_time)
        await ctx.send(f"Tới giờ hẹn rồi nha {ctx.author.mention}. Nội dung: {message}")
        
        
async def setup(client):
    await client.add_cog(Reminder(client))
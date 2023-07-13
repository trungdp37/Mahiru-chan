import discord
import asyncio
import datetime
from discord.ext import commands

class Greeting6(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('greeting_at_6.py is ready!')
        now = datetime.datetime.now()
        then = now+datetime.timedelta(days=1) 
        then.replace(hour=6, minute=0)
        wait_time = (then-now).total_seconds()
        await asyncio.sleep(wait_time)
        channel = self.client.get_channel(921631227717500988)
        await channel.send('Chào buổi tối. Tới giờ làm việc với em rồi đó anh ơi!!!')
    
async def setup(client):
    await client.add_cog(Greeting6(client))
import discord
from discord.ext import commands, tasks
from itertools import cycle
import wavelink
from wavelink.ext import spotify
import os
import asyncio
import json

def get_server_prefix(client, message):
    with open("json/prefixes.json", "r") as f:
        prefix = json.load(f)

    return prefix[str(message.guild.id)]

class Client(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        intents.message_content = True

        super().__init__(intents=intents, command_prefix=get_server_prefix)

    async def on_ready(self):
        print(f'Logged in {self.user} | {self.user.id}')

    async def setup_hook(self):
        sc = spotify.SpotifyClient(
            client_id='93df47bbc35742a0a3841fe77ac0d1be',
            client_secret='3841865cae214a7d967279b62e1bed2c'
        )
        node: wavelink.Node = wavelink.Node(uri='http://localhost:2333', password='youshallnotpass')
        await wavelink.NodePool.connect(client=self, nodes=[node], spotify=sc)

client = Client()

client.remove_command("help")

bot_stats = cycle(["Tán tỉnh Amane-kun", "Làm việc nhà", "Nấu cơm", "Học bài"])

@tasks.loop(hours=4)
async def change_status():
    await client.change_presence(activity=discord.Game(next(bot_stats)))
    
@client.event
async def on_ready():
    print("Ready!")
    change_status.start()


@client.event
async def on_guild_join(guild):
    with open("json/prefixes.json", "r") as f:
        prefix = json.load(f)
            
    prefix[str(guild.id)] = "m!"
        
    with open("json/prefixes.json", "w") as f:
        json.dump(prefix, f, indent=4)
        
@client.event
async def on_guild_remove(guild):
    with open("json/prefixes.json", "r") as f:
        prefix = json.load(f)
            
    prefix.pop(str(guild.id))
        
    with open("json/prefixes.json", "w") as f:
        json.dump(prefix, f, indent=4)
                          
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")
            
async def main():
    async with client:
        await load()
        await client.start("MTEwNTA4MjE4NTkwMTQyNDY4MQ.Gl1X4m.ocuSGmH4sfYpiB0c0nr28NI0jHJqQEx3XQ8S2o")
    
asyncio.run(main()) 



        
        

    
import discord

from discord.ext import commands
 
class Addcmt(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @commands.Cog.listener()
    async def on_ready(self):
        print('add_command.py is ready!')
    
    @commands.command()
    async def add(self, ctx, command : str, *, response : str):
        with open("txt/command.txt", "a", encoding='utf-8') as command_file:
                command_file.write(command + "\n")
        with open("txt/response.txt", "a", encoding='utf-8') as response_file:
                response_file.write(response + "\n")    
        await ctx.send("Đã thêm biểu thức thành công!")
        
            
    @commands.Cog.listener()
    async def on_message(self, message):
        with open("txt/command.txt", "r", encoding='utf-8') as command_file:
            command = [line.strip() for line in command_file.readlines()]
            command1 = message.content
        for word in command:
            if command1 == word or command1.lower() == word or command1.upper() == word:      
                with open("txt/response.txt", "r", encoding='utf-8') as response_file:
                    response = response_file.readlines()
                await message.channel.send(response[command.index(word)])
                
    @add.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Không thể thực hiện lệnh. Hình như bạn nhập thiếu gì rồi thì phải...")
                       
async def setup(client):
    await client.add_cog(Addcmt(client))

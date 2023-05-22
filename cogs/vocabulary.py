import discord
import random
import datetime

from discord.ext import commands
 
class Vocabulary(commands.Cog):
    def __init__(self, client):
        self.client = client 

    @commands.Cog.listener()
    async def on_ready(self):
        print('words.py is ready!')
    
    def read_vocabulary(self, filename):
        with open(filename, encoding='utf-8') as f:
            vocabulary = f.read().splitlines()
        return vocabulary

    def get_word_mean_ex(self, vocabulary, meaning_file):
        word = random.choice(vocabulary)
        with open(meaning_file, encoding='utf-8') as f:
            meaning = f.read().splitlines()
            mean = meaning[vocabulary.index(word)]
        return [word, mean]

    @commands.command(aliases=["v"])
    async def vocabulary(self, ctx):
        vocabulary = self.read_vocabulary("txt/vocabulary.txt")
        meanings = "txt/meaning.txt"

        word, mean = self.get_word_mean_ex(vocabulary, meanings)

        now = datetime.datetime.now()                            
        embed_message = discord.Embed(color=discord.Color.dark_embed())        
        embed_message.add_field(name="Từ vựng", value=word, inline=False)
        embed_message.add_field(name="Nghĩa", value=mean, inline=True)
        embed_message.set_footer(text=f"Datetime | {now:%Y-%m-%d %H:%M}")
         
        await ctx.send(embed=embed_message)                            
async def setup(client):
    await client.add_cog(Vocabulary(client))
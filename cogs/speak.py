import discord
from discord.ext import commands
from gtts import gTTS
 
class Speak(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('speak.py is ready!') 
        
    @commands.command()
    async def speak(self, ctx, *args):
        text = " ".join(args)
        user = ctx.message.author
        if user.voice != None:
            try:
                vc = await user.voice.channel.connect()
            except:
                vc = ctx.voice_client
                
            sound = gTTS(text=text, lang='vi', slow=False)
            sound.save("tts-audio.mp3")
            
            if vc.is_playing():
                vc.stop()
        
            source = await discord.FFmpegOpusAudio.from_probe("tts-audio.mp3", method="fallback")
            vc.play(source)
        else:
            await ctx.send("Vào voice đi đã rồi xài.")
                
    @commands.command()
    async def leave(self, ctx):
        vc = ctx.voice_client

        if vc:
            await vc.disconnect()
            mbed = discord.Embed(title="Ngắt kết nối", color=discord.Color.red())
            await ctx.send(embed=mbed)
        else:
            await ctx.send("Mahiru-chan không ở trong bất kì voice nào!")
        
async def setup(client):
    await client.add_cog(Speak(client))
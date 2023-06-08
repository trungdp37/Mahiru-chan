import discord
from discord.ext import commands
import wavelink
from wavelink.ext import spotify
import asyncio
import random

from cogs.Setup.pagination import *

class Music(commands.Cog):
    def __init__(self, client):
        self.playingTextChannel = 0
        self.client = client
        self.check_loop_queue = False
        self.check_loop_track = False
        self.check_shuffle = False
        self.index_shuffle = False
        self.check_fist_play = False
        self.queue = []
        self.lqueue = []

    @commands.Cog.listener()
    async def on_ready(self):
        print("musics.py is ready!")

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"Node {node.id} is ready!")

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEventPayload):
        player = payload.player
        channel = self.client.get_channel(self.playingTextChannel)
        if len(self.queue) != 0:
            if self.check_shuffle == True:
                next_track = self.index_shuffle
            else:
                next_track = self.queue[0]
            try:
                if isinstance(next_track, wavelink.tracks.YouTubeTrack):
                    await player.play(next_track)

                elif isinstance(next_track, spotify.SpotifyTrack):
                    await player.play(next_track, populate=True)

                else: 
                    return await channel.send(embed=discord.Embed(title=f"Có lỗi khi mở bài tiếp theo **{next_track.title}**", color=discord.Color.red()))
            except:
                return await channel.send(embed=discord.Embed(title=f"Có lỗi khi mở bài tiếp theo **{next_track.title}**", color=discord.Color.red()))
            
        elif len(self.queue) == 0 and self.check_loop_queue == True:
            self.queue = self.lqueue[:]
            self.lqueue = []
            if self.check_shuffle == True:
                next_track = self.index_shuffle
            else:
                next_track = self.queue[0]
            try:
                if isinstance(next_track, wavelink.tracks.YouTubeTrack):
                    await player.play(next_track)

                elif isinstance(next_track, spotify.SpotifyTrack):
                    await player.play(next_track, populate=True)

                else: 
                    return await channel.send(embed=discord.Embed(title=f"Có lỗi khi mở bài tiếp theo **{next_track.title}**", color=discord.Color.red()))
            except:
                return await channel.send(embed=discord.Embed(title=f"Có lỗi khi mở bài tiếp theo **{next_track.title}**", color=discord.Color.red()))

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, payload: wavelink.TrackEventPayload):
        if len(self.queue) != 0:
            if self.check_fist_play == False and self.check_shuffle == True:
                self.queue.pop(0)
                self.check_fist_play = True
            if self.check_loop_queue == True:
                if self.check_shuffle == True:
                    self.index_shuffle = random.choice(range(len(self.queue)))
                    self.queue.pop(self.index_shuffle)
                else:
                    self.lqueue.append(self.queue.pop(0))
            elif self.check_loop_track == False or len(self.queue) > 1:
                if self.check_shuffle == True:
                    self.index_shuffle = random.choice(range(len(self.queue)))
                    self.queue.pop(self.index_shuffle)
                else:
                    self.queue.pop(0)


    @commands.command(name='play')
    async def play_command(self, ctx, *, search: str):
        try:
            if not ctx.voice_client:
                vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            else:
                vc: wavelink.Player = ctx.voice_client
            if search.startswith("https://www.youtube.com/watch?"):
                track = await wavelink.YouTubeTrack.search(search, return_first=True)

                if not vc.is_playing():
                    self.queue.append(track)
                    await vc.play(track)
                else:
                    self.queue.append(track)

                t_sec = int(track.length)/1000
                hour = int(t_sec/3600)
                min = int((t_sec%3600)/60)
                sec = int((t_sec%3600)%60)
                length = f"{hour}giờ {min}phút {sec}giây" if not hour == 0 else f"{min}phút {sec}giây"
                embed = discord.Embed(title=f"Đã thêm bài nhạc!🎶🎶🎶", description=f"**[{track.title}]({track.uri})**", color=discord.Color.red())
                embed.set_author(name=f"Yêu cầu từ {ctx.author.name}", icon_url=ctx.author.avatar)
                embed.set_thumbnail(url = track.thumbnail)
                embed.add_field(name="Kênh 📺:", value=track.author, inline=True)
                embed.add_field(name="Thời lượng 📀:", value=f"{length}", inline=True)

                await ctx.send(embed=embed)

            elif search.startswith("https://www.youtube.com/playlist?"):
                data = await wavelink.YouTubePlaylist.search(search)
                list_track = data.__dict__['tracks']

                list_embed =[]
                for track in list_track:
                    self.queue.append(track)
                    t_sec = int(track.length)/1000
                    hour = int(t_sec/3600)
                    min = int((t_sec%3600)/60)
                    sec = int((t_sec%3600)%60)
                    length = f"{hour}giờ {min}phút {sec}giây" if not hour == 0 else f"{min}phút {sec}giây"
                    embed = discord.Embed(title=f"Đã thêm playlist {data.__dict__['name']}!🎶🎶🎶", description=f"**[{track.title}]({track.uri})**", color=discord.Color.red())
                    embed.set_author(name=f"Yêu cầu từ {ctx.author.name}", icon_url=ctx.author.avatar)
                    embed.set_thumbnail(url = track.thumbnail)
                    embed.add_field(name="Kênh 📺:", value=track.author, inline=True)
                    embed.add_field(name="Thời lượng 📀:", value=f"{length}", inline=True)
                    list_embed.append(embed)

                if not vc.is_playing():
                    await vc.play(list_track[0])

                await Simple().start(ctx, pages=list_embed)

            elif search.startswith("https://open.spotify.com/track"):
                decoded = spotify.decode_url(search)
                vc.autoplay = False
                track = await spotify.SpotifyTrack.search(search)
                if not vc.is_playing():
                    self.queue.append(track)
                    await vc.play(track, populate=True)
                else:
                    self.queue.append(track)
                t_sec = int(track.length)/1000
                hour = int(t_sec/3600)
                min = int((t_sec%3600)/60)
                sec = int((t_sec%3600)%60)
                length = f"{hour}giờ {min}phút {sec}giây" if not hour == 0 else f"{min}phút {sec}giây"
                embed = discord.Embed(title=f"Đã thêm bài hát!🎶🎶🎶", description=f"**{track.title}**", color=discord.Color.red())
                embed.set_author(name=f"Yêu cầu từ {ctx.author.name}", icon_url=ctx.author.avatar)
                embed.set_thumbnail(url = track.images[0])
                embed.add_field(name="Nhạc sĩ 🎤:", value=track.artists, inline=True)
                embed.add_field(name="Album 📚:", value=track.album, inline=True)
                embed.add_field(name="Thời lượng 📀:", value=f"{length}", inline=True)

                await ctx.send(embed=embed)

            elif search.startswith("https://open.spotify.com/playlist"):
                decoded = spotify.decode_url(search)
                list_embed =[]
                async for track in spotify.SpotifyTrack.iterator(query = search, type=spotify.SpotifySearchType.playlist):
                    if not vc.is_playing():
                        self.queue.append(track)
                        await vc.play(track, populate=True)
                    else:
                        self.queue.append(track)
                    t_sec = int(track.length)/1000
                    hour = int(t_sec/3600)
                    min = int((t_sec%3600)/60)
                    sec = int((t_sec%3600)%60)
                    length = f"{hour}giờ {min}phút {sec}giây" if not hour == 0 else f"{min}phút {sec}giây"                       
                    embed = discord.Embed(title=f"Đã thêm playlist!🎶🎶🎶", description=f"**{track.title}**", color=discord.Color.red())
                    embed.set_author(name=f"Yêu cầu từ {ctx.author.name}", icon_url=ctx.author.avatar)
                    embed.set_thumbnail(url = track.images[0])
                    embed.add_field(name="Nhạc sĩ 🎤:", value=track.artists, inline=True)
                    embed.add_field(name="Album 📚:", value=track.album, inline=True)
                    embed.add_field(name="Thời lượng 📀:", value=f"{length}", inline=True)
                    list_embed.append(embed)

                await Simple().start(ctx, pages=list_embed)

            elif search.startswith("https://open.spotify.com/album"):
                decoded = spotify.decode_url(search)
                list_embed =[]
                async for track in spotify.SpotifyTrack.iterator(query = search, type=spotify.SpotifySearchType.album):
                    if not vc.is_playing():
                        await vc.play(track, populate=True)
                        self.queue.append(track)
                    else:
                        self.queue.append(track)
                    t_sec = int(track.length)/1000
                    hour = int(t_sec/3600)
                    min = int((t_sec%3600)/60)
                    sec = int((t_sec%3600)%60)
                    length = f"{hour}giờ {min}phút {sec}giây" if not hour == 0 else f"{min}phút {sec}giây"            
                    embed = discord.Embed(title=f"Đã thêm album!🎶🎶🎶", description=f"**{track.title}**", color=discord.Color.red())
                    embed.set_author(name=f"Yêu cầu từ {ctx.author.name}", icon_url=ctx.author.avatar)
                    embed.set_thumbnail(url = track.images[0])
                    embed.add_field(name="Nhạc sĩ 🎤:", value=track.artists, inline=True)
                    embed.add_field(name="Album 📚:", value=track.album, inline=True)
                    embed.add_field(name="Thời lượng 📀:", value=f"{length}", inline=True)
                    list_embed.append(embed)

                await Simple().start(ctx, pages=list_embed)

            else:
                track = await wavelink.YouTubeTrack.search(search, return_first=True)
                if not vc.is_playing():
                    self.queue.append(track)
                    await vc.play(track)
                else:
                    self.queue.append(track)
                t_sec = int(track.length)/1000
                hour = int(t_sec/3600)
                min = int((t_sec%3600)/60)
                sec = int((t_sec%3600)%60)
                length = f"{hour}giờ {min}phút {sec}giây" if not hour == 0 else f"{min}phút {sec}giây"               
                embed = discord.Embed(title=f"Đã thêm bài nhạc vào danh sách chờ!🎶🎶🎶", description=f"**[{track.title}]({track.uri})**", color=discord.Color.red())
                embed.set_author(name=f"Yêu cầu từ {ctx.author.name}", icon_url=ctx.author.avatar)
                embed.set_thumbnail(url = track.thumbnail)
                embed.add_field(name="Kênh 📺:", value=track.author, inline=True)
                embed.add_field(name="Thời lượng 📀:", value=f"{length}", inline=True)

                await ctx.send(embed=embed)
        
        except:
            mbed = discord.Embed(title=f"Có lỗi khi mở bài này!", color=discord.Color.red())
            await ctx.send(embed=mbed)

    @commands.command(name="disconnect")
    async def disconnect_command(self, ctx):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)

        if player is None:
            return await ctx.send("Mahiru-chan không ở trong bất kì voice nào!")
        
        await player.disconnect()
        mbed = discord.Embed(title="Ngắt kết nối", color=discord.Color.red())
        await ctx.send(embed=mbed)

    @commands.command(name="stop")
    async def stop_command(self, ctx):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)

        if player is None:
            return await ctx.send("Mahiru-chan không ở trong bất kì voice nào!")
        
        if player.is_playing():
            await player.stop()
            embed = discord.Embed(title="Đã dùng phát nhạc!", color=discord.Color.red())
            return await ctx.send(embed=embed)
        else:
            return await ctx.send("Chưa có gì để chạy sao stop?")
        
    @commands.command(name="pause")
    async def pause_command(self, ctx):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)

        if player is None:
            return await ctx.send("Mahiru-chan không ở trong bất kì voice nào!")
        
        if not player.is_paused():
            if player.is_playing():
                await player.pause()
                embed = discord.Embed(title="Đã dừng nhạc!", color=discord.Color.red())
                return await ctx.send(embed=embed)
            else:
                return await ctx.send("Chưa có gì để chạy sao pause?")
        else:
            return await ctx.send("Nhạc đã dừng!")
    
    @commands.command(name="resume", aliases=["continue"])
    async def resume_command(self, ctx):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)

        if player is None:
            return await ctx.send("Mahiru-chan không ở trong bất kì voice nào!")
        
        if player.is_paused():
            await player.resume()
            embed = discord.Embed(title="Tiếp tục phát!", color=discord.Color.red())
            return await ctx.send(embed=embed)
        else:
            if len(self.queue) != 0:
                next_track = self.queue[0]
                if isinstance(next_track, wavelink.tracks.YouTubeTrack):
                    await player.play(next_track)
                    t_sec = int(next_track.length)/1000
                    hour = int(t_sec/3600)
                    min = int((t_sec%3600)/60)
                    sec = int((t_sec%3600)%60)
                    length = f"{hour}giờ {min}phút {sec}giây" if not hour == 0 else f"{min}phút {sec}giây"
                    embed = discord.Embed(title=f"Đã chơi bài!🎶🎶🎶", description=f"**[{next_track.title}]({next_track.uri})**", color=discord.Color.red())
                    embed.set_author(name=f"Yêu cầu từ {ctx.author.name}", icon_url=ctx.author.avatar)
                    embed.set_thumbnail(url = next_track.thumbnail)
                    embed.add_field(name="Kênh 📺:", value=next_track.author, inline=True)
                    embed.add_field(name="Thời lượng 📀:", value=f"{length}", inline=True)
                    await ctx.send(embed=embed)

                elif isinstance(next_track, spotify.SpotifyTrack):
                    await player.play(next_track, populate=True)
                    t_sec = int(next_track.length)/1000
                    hour = int(t_sec/3600)
                    min = int((t_sec%3600)/60)
                    sec = int((t_sec%3600)%60)
                    length = f"{hour}giờ {min}phút {sec}giây" if not hour == 0 else f"{min}phút {sec}giây"
                    embed = discord.Embed(title=f"Đã chơi bài!🎶🎶🎶", description=f"**{next_track.title}**", color=discord.Color.red())
                    embed.set_author(name=f"Yêu cầu từ {ctx.author.name}", icon_url=ctx.author.avatar)
                    embed.set_thumbnail(url = next_track.images[0])
                    embed.add_field(name="Nhạc sĩ 🎤:", value=next_track.artists, inline=True)
                    embed.add_field(name="Album 📚:", value=next_track.album, inline=True)
                    embed.add_field(name="Thời lượng 📀:", value=f"{length}", inline=True)
                    await ctx.send(embed=embed)
                else: 
                    await ctx.send("Có lỗi khi chơi bài này!💫")
            else:
                return await ctx.send("Nhạc đã dừng")

    @commands.command(name="volume")
    async def volume_command(self, ctx, to : int):
        if to > 1000:
            return await ctx.send("Âm lượng chỉ ở giữa 0 -> 1000")
        elif to < 1:
            return await ctx.send("Âm lượng chỉ ở giữa 0 -> 1000")

        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)
        await player.set_volume(to)

        embed = discord.Embed(title=f"Thay đổi âm lượng thành {to}!", color=discord.Color.red())
        await ctx.send(embed=embed)

    @commands.command(name="skip")
    async def skip_command(self, ctx):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)

        if len(self.queue) != 0:
            next_track = self.queue[0]
            try:
                if isinstance(next_track, wavelink.tracks.YouTubeTrack):
                    await player.play(next_track)
                    t_sec = int(next_track.length)/1000
                    hour = int(t_sec/3600)
                    min = int((t_sec%3600)/60)
                    sec = int((t_sec%3600)%60)
                    length = f"{hour}giờ {min}phút {sec}giây" if not hour == 0 else f"{min}phút {sec}giây"
                    embed = discord.Embed(title=f"Đã chơi bài!🎶🎶🎶", description=f"**[{next_track.title}]({next_track.uri})**", color=discord.Color.red())
                    embed.set_author(name=f"Yêu cầu từ {ctx.author.name}", icon_url=ctx.author.avatar)
                    embed.set_thumbnail(url = next_track.thumbnail)
                    embed.add_field(name="Kênh 📺:", value=next_track.author, inline=True)
                    embed.add_field(name="Thời lượng 📀:", value=f"{length}", inline=True)
                    await ctx.send(embed=embed)

                elif isinstance(next_track, spotify.SpotifyTrack):
                    await player.play(next_track, populate=True)
                    t_sec = int(next_track.length)/1000
                    hour = int(t_sec/3600)
                    min = int((t_sec%3600)/60)
                    sec = int((t_sec%3600)%60)
                    length = f"{hour}giờ {min}phút {sec}giây" if not hour == 0 else f"{min}phút {sec}giây"
                    embed = discord.Embed(title=f"Đã chơi bài!🎶🎶🎶", description=f"**{next_track.title}**", color=discord.Color.red())
                    embed.set_author(name=f"Yêu cầu từ {ctx.author.name}", icon_url=ctx.author.avatar)
                    embed.set_thumbnail(url = next_track.images[0])
                    embed.add_field(name="Nhạc sĩ 🎤:", value=next_track.artists, inline=True)
                    embed.add_field(name="Album 📚:", value=next_track.album, inline=True)
                    embed.add_field(name="Thời lượng 📀:", value=f"{length}", inline=True)
                    await ctx.send(embed=embed)
                else: 
                    await ctx.send("Có lỗi khi chơi bài này!💫")
                
            except:
                return await ctx.reply(embed=discord.Embed(title="Có lỗi khi chơi bài này!💫", color=discord.Color.red()))
        else:
            await ctx.reply("Hàng chờ không có gì cả!💫")

    @commands.command(name="search")
    async def search_command(self, ctx, *, search: str):
        try:
            tracks = await wavelink.YouTubeTrack.search(search)
        except:
            return await ctx.reply(embed=discord.Embed(title="Có lỗi khi tìm kiếm!", color=discord.Color.red()))

        if tracks is None:
            return await ctx.reply("Không tìm thấy")

        mbed = discord.Embed(
            title="Kết quả tìm kiếm: ",
            description=("\n".join(f"**{i+1}. {t.title}**" for i, t in enumerate(tracks[:5]))),
            color = discord.Color.red()
        )
        msg = await ctx.reply(embed=mbed)

        emojis_list = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '❌']
        emojis_dict = {
            '1️⃣': 0,
            "2️⃣": 1,
            "3️⃣": 2,
            "4️⃣": 3,
            "5️⃣": 4,
            "❌": -1
        }

        for emoji in list(emojis_list[:min(len(tracks), len(emojis_list))]):
            await msg.add_reaction(emoji)

        def check(res, user):
            return(res.emoji in emojis_list and user == ctx.author and res.message.id == msg.id)

        try:
            reaction, _ = await self.client.wait_for("reaction_add", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await msg.delete()
            return
        else:
            await msg.delete()

        try:
            if emojis_dict[reaction.emoji] == -1: return
            choosed_track = tracks[emojis_dict[reaction.emoji]]
        except:
            return

        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client

        if not vc.is_playing() or not vc.is_paused():
            try:
                self.queue.append(choosed_track)
                await vc.play(choosed_track)

                t_sec = int(choosed_track.length)/1000
                hour = int(t_sec/3600)
                mins = int((t_sec%3600)/60)
                sec = int((t_sec%3600)%60)
                length = f"{hour}giờ {mins}phút {sec}giây" if not hour == 0 else f"{mins}phút {sec}giây"
                embed = discord.Embed(title=f"Đã thêm bài nhạc!🎶🎶🎶", description=f"**[{choosed_track.title}]({choosed_track.uri})**", color=discord.Color.red())
                embed.set_author(name=f"Yêu cầu từ {ctx.author.name}", icon_url=ctx.author.avatar)
                embed.set_thumbnail(url = choosed_track.thumbnail)
                embed.add_field(name="Kênh 📺:", value=choosed_track.author, inline=True)
                embed.add_field(name="Thời lượng 📀:", value=f"{length}", inline=True)

                await ctx.send(embed=embed)
            except:
                return await ctx.reply(embed=discord.Embed(title="Có lỗi khi chơi track này!", color=discord.Color.red()))
        else:
            self.queue.append(choosed_track)

    @commands.command(name="nowplaying", aliases=["now_playing", "np"])
    async def now_playing_command(self, ctx):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)

        if player is None:
            return await ctx.reply("Mahiru-chan không ở trong bất kì voice nào!")

        if player.is_playing():
            current_track = player.current
            if isinstance(current_track, wavelink.tracks.YouTubeTrack):
                t_sec = int(current_track.length)/1000
                hour = int(t_sec/3600)
                min = int((t_sec%3600)/60)
                sec = int((t_sec%3600)%60)
                length = f"{hour}giờ {min}phút {sec}giây" if not hour == 0 else f"{min}phút {sec}giây"
                embed = discord.Embed(title=f"Đã chơi bài!🎶🎶🎶", description=f"**[{current_track.title}]({current_track.uri})**", color=discord.Color.red())
                embed.set_author(name=f"Yêu cầu từ {ctx.author.name}", icon_url=ctx.author.avatar)
                embed.set_thumbnail(url = current_track.thumbnail)
                embed.add_field(name="Kênh 📺:", value=current_track.author, inline=True)
                embed.add_field(name="Thời lượng 📀:", value=f"{length}", inline=True)
                await ctx.send(embed=embed)

            elif isinstance(current_track, spotify.SpotifyTrack):
                t_sec = int(current_track.length)/1000
                hour = int(t_sec/3600)
                min = int((t_sec%3600)/60)
                sec = int((t_sec%3600)%60)
                length = f"{hour}giờ {min}phút {sec}giây" if not hour == 0 else f"{min}phút {sec}giây"
                embed = discord.Embed(title=f"Đã chơi bài!🎶🎶🎶", description=f"**{current_track.title}**", color=discord.Color.red())
                embed.set_author(name=f"Yêu cầu từ {ctx.author.name}", icon_url=ctx.author.avatar)
                embed.set_thumbnail(url = current_track.images[0])
                embed.add_field(name="Nhạc sĩ 🎤:", value=current_track.artists, inline=True)
                embed.add_field(name="Album 📚:", value=current_track.album, inline=True)
                embed.add_field(name="Thời lượng 📀:", value=f"{length}", inline=True)
                await ctx.send(embed=embed)
            else: 
                await ctx.send("Có lỗi khi lấy thông tin!💫")
        else:
            await ctx.reply("đã chạy bài nào đâu!💫")
            
    @commands.command(name="queue")
    async def queue_command(self, ctx):
        list_embed = []
        if len(self.queue) == 0: 
             await ctx.send(embed=discord.Embed(title="Hàng chờ rỗng!💫", color=discord.Color.red()))
        else:
            for current_track in self.queue:
                if isinstance(current_track, wavelink.tracks.YouTubeTrack):
                    t_sec = int(current_track.length)/1000
                    hour = int(t_sec/3600)
                    min = int((t_sec%3600)/60)
                    sec = int((t_sec%3600)%60)
                    length = f"{hour}giờ {min}phút {sec}giây" if not hour == 0 else f"{min}phút {sec}giây"
                    embed = discord.Embed(title=f"Đã chơi bài!🎶🎶🎶", description=f"**[{current_track.title}]({current_track.uri})**", color=discord.Color.red())
                    embed.set_author(name=f"Yêu cầu từ {ctx.author.name}", icon_url=ctx.author.avatar)
                    embed.set_thumbnail(url = current_track.thumbnail)
                    embed.add_field(name="Kênh 📺:", value=current_track.author, inline=True)
                    embed.add_field(name="Thời lượng 📀:", value=f"{length}", inline=True)
                    list_embed.append(embed)

                elif isinstance(current_track, spotify.SpotifyTrack):
                    t_sec = int(current_track.length)/1000
                    hour = int(t_sec/3600)
                    min = int((t_sec%3600)/60)
                    sec = int((t_sec%3600)%60)
                    length = f"{hour}giờ {min}phút {sec}giây" if not hour == 0 else f"{min}phút {sec}giây"
                    embed = discord.Embed(title=f"Đã chơi bài!🎶🎶🎶", description=f"**{current_track.title}**", color=discord.Color.red())
                    embed.set_author(name=f"Yêu cầu từ {ctx.author.name}", icon_url=ctx.author.avatar)
                    embed.set_thumbnail(url = current_track.images[0])
                    embed.add_field(name="Nhạc sĩ 🎤:", value=current_track.artists, inline=True)
                    embed.add_field(name="Album 📚:", value=current_track.album, inline=True)
                    embed.add_field(name="Thời lượng 📀:", value=f"{length}", inline=True)
                    list_embed.append(embed)
            await Simple().start(ctx, pages=list_embed)


    @commands.command(name="loop", aliases=["lp"])
    async def looptrack_command(self, ctx):
        if not ctx.voice_client:
            return await ctx.send(embed=discord.Embed(title="Mahiru-chan không có trong voice!💫", color=discord.Color.red()))
        elif not ctx.author.voice:
            return await ctx.send(embed=discord.Embed(title="Bạn đâu có trong voice!💫", color=discord.Color.red()))

        if self.check_loop_track == False:
            self.check_loop_track = True
            return await ctx.send(embed=discord.Embed(title="Đã mở lặp bài!💫", color=discord.Color.red()))
        else:
            self.check_loop_track = False
            return await ctx.send(embed=discord.Embed(title="Đã tắt lặp hàng chờ!💫", color=discord.Color.red()))
        
    @commands.command(name="loopqueue", aliases=["lpq"])
    async def loopqueue_command(self, ctx):
        if not ctx.voice_client:
            return await ctx.send(embed=discord.Embed(title="Mahiru-chan không có trong voice!💫", color=discord.Color.red()))
        elif not ctx.author.voice:
            return await ctx.send(embed=discord.Embed(title="Bạn đâu có trong voice!💫", color=discord.Color.red()))

        if self.check_loop_queue == False:
            self.check_loop_queue = True
            return await ctx.send(embed=discord.Embed(title="Đã mở lặp hàng chờ!💫", color=discord.Color.red()))
        else:
            self.check_loop_queue = False
            return await ctx.send(embed=discord.Embed(title="Đã tắt lặp hàng chờ!💫", color=discord.Color.red()))
        
    @commands.command(name="shuffle", aliases=["mix"])
    async def loopqueue_command(self, ctx):
        if not ctx.voice_client:
            return await ctx.send(embed=discord.Embed(title="Mahiru-chan không có trong voice!💫", color=discord.Color.red()))
        elif not ctx.author.voice:
            return await ctx.send(embed=discord.Embed(title="Bạn đâu có trong voice!💫", color=discord.Color.red()))

        if self.check_shuffle == False:
            self.check_shuffle = True
            return await ctx.send(embed=discord.Embed(title="Đã mở xáo trộn hàng chờ!💫", color=discord.Color.red()))
        else:
            self.check_shuffle = False
            return await ctx.send(embed=discord.Embed(title="Đã tắt xáo trộn hàng chờ!💫", color=discord.Color.red()))
        
async def setup(client):
    await client.add_cog(Music(client))
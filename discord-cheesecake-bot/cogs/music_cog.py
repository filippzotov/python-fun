import discord
from discord.ext import commands

from youtube_dl import YoutubeDL

# from youtube_dl import YoutubeDL


class music_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.is_playing = False
        self.is_paused = False

        self.music_queue = []
        self.YDL_OPTIONS = {"format": "bestaudio"}  # "noplaylist": "True"
        self.FFMPEG_OPTIONS = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn",
        }

        self.vc = None

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                if "&list=" in item:
                    info = ydl.extract_info(item, download=False)["entries"]
                else:
                    info = ydl.extract_info("ytsearch:%s" % item, download=False)[
                        "entries"
                    ]
            except Exception:
                return False
        urls = []
        for video in info:
            urls.append({"source": video["formats"][0]["url"], "title": video["title"]})
        return urls

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]["source"]

            self.music_queue.pop(0)
            self.vc.play(
                discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS),
                after=lambda e: self.play_next(),
            )
        else:
            self.is_playing = False

    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]["source"]
            title = self.music_queue[0][0]["title"]
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()
                if self.vc == None:
                    await ctx.send("Could not connect to the voice channel")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])

            self.music_queue.pop(0)
            await ctx.send(f"Now playing: {title}")
            self.vc.play(
                discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS),
                after=lambda e: self.play_next(),
            )

        else:
            self.is_playing = False

    @commands.command(name="play")
    async def play(self, ctx, *args):
        query = " ".join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("Connect to a voice channel!")
        elif self.is_paused:
            self.vc.resume()
        else:
            songs = self.search_yt(query)
            for song in songs:
                if type(song) == type(True):
                    await ctx.send(
                        "Could not download the song. Incorrect format, try a different keyword"
                    )
                    break
                else:
                    await ctx.send("Song added to the queue")
                    self.music_queue.append([song, voice_channel])

            if self.is_playing == False and len(self.music_queue):
                await self.play_music(ctx)

    @commands.command(name="pause")
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()

    @commands.command(name="resume")
    async def pause(self, ctx, *args):
        if self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()

    @commands.command(name="skip")
    async def skip(self, ctx, *args):
        if self.vc != None and self.vc:
            self.vc.stop()
            await self.play_music(ctx)

    @commands.command(name="clear")
    async def clear(self, ctx, *args):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("Music queue cleared")

    @commands.command(name="leave")
    async def leave(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()


async def setup(bot):
    await bot.add_cog(music_cog(bot))

import discord
from discord.ext import commands
import asyncio
import youtube_dl

tube = youtube_dl.YoutubeDL()


class Video:
    """docstring for Video cherche pas à comprendre"""

    def __init__(self, link):
        video = tube.extract_info(link, download=False)
        format_ = video["formats"][0]
        self.name = video['title']
        self.url = video['webpage_url']
        self.stream_url = format_["url"]

    def __str__(self):
        return self.name


class MusicCogs(commands.Cog):
    """docstring for WebCogs"""

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.url_akito = 'https://cdn.discordapp.com/avatars/537430027479023627/8d60edbed8d2fa62e543dd086fefddb9.webp?size=1024'
        self.get = discord.utils.get
        self.musics = {}

    @commands.command()
    async def skip(self, ctx):
        client = ctx.guild.voice_client
        client.stop()

    def play_song(self, client, queue, music):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(music.stream_url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"), 1.5)   
        def next(_):
            if len(queue) > 0:
                music2 = queue[0]
                del queue[0]
                self.play_song(client, queue, music2)
            else:
                asyncio.run_coroutine_threadsafe(client.disconnect(), self.bot.loop)
        client.play(source, after=next)


    @commands.command()
    async def queue(self, ctx):
        embed = discord.Embed(title=f"** la queue de {ctx.guild.name}**", description='Musics')
        if ctx.guild in [*self.musics.keys()] and len(self.musics[ctx.guild]) > 0:
            value = "\n".join([i.name for i in self.musics[ctx.guild]])
        else:
            value = "la queue est vide"
        embed.add_field(name="les musics", value=value)
        embed.set_footer(text="akitologique", icon_url=self.url_akito)
        embed.set_thumbnail(url="https://th.bing.com/th/id/OIP.lkVlOtVvcbOVnLxiefC0CwHaFj?pid=Api&rs=1")
        embed.color = discord.Color(0Xff751a)
        await ctx.send(embed=embed)


    @commands.command()
    async def play(self, ctx, url):
        client = ctx.guild.voice_client
        if client and client.channel:
            video = Video(url)
            self.musics[ctx.guild].append(video)
            await ctx.send(f"la musique {video.name} a été ajouté dans la queue de chansons")
        else:
            channel = ctx.author.voice.channel
            video = Video(url)
            self.musics[ctx.guild] = []
            client = await channel.connect()
            await ctx.channel.send(f"la music {video.name} a commencé bonne séance")
            self.play_song(client, self.musics[ctx.guild], video)


    @commands.command()
    async def pause(self, ctx):
        client = ctx.guild.voice_client
        if not client.is_paused():
            client.pause()
        else:
            ctx.send("le bot est dèjà en pause")


    @commands.command()
    async def continu(self, ctx):
        client = ctx.guild.voice_client
        if client.is_paused():
            client.resume()
        else:
            ctx.send("le bot est dèjà en marche")


    @commands.command(name='stop')
    async def disconnect(self, ctx):
        client = ctx.guild.voice_client
        await client.disconnect()

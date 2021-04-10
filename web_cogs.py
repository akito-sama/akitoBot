import discord
from discord.ext import commands
import requetes
import mal
import translators as ts
import random


class WebCogs(commands.Cog):
    """docstring for WebCogs"""

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.languages =  ['af', 'am', 'ar', 'az', 'be', 'bg', 'bn', 'bs', 'ca', 'ceb', 'co', 'cs', 'cy', 'da', 'de', 'el', 'en', 'eo', 'es', 'et', 'eu', 'fa', 'fi', 'fr', 'fy', 'ga', 'gd', 'gl', 'gu', 'ha', 'haw', 'hi', 'hmn', 'hr', 'ht', 'hu', 'hy', 'id', 'ig', 'is', 'it', 'iw', 'ja', 'jw', 'ka', 'kk', 'km', 'kn', 'ko', 'ku', 'ky', 'la', 'lb', 'lo', 'lt', 'lv', 'mg', 'mi', 'mk', 'ml', 'mn', 'mr', 'ms', 'mt', 'my', 'ne', 'nl', 'no', 'ny', 'or', 'pa', 'pl', 'ps', 'pt', 'ro', 'ru', 'rw', 'sd', 'si', 'sk', 'sl', 'sm', 'sn', 'so', 'sq', 'sr', 'st', 'su', 'sv', 'sw', 'ta', 'te', 'tg', 'th', 'tk', 'tl', 'tr', 'tt', 'ug', 'uk', 'ur', 'uz', 'vi', 'xh', 'yi', 'yo', 'zh-CN', 'zh-TW', 'zu']
        self.url_akito = 'https://cdn.discordapp.com/avatars/537430027479023627/1b276d12906ca8a20e182ce3b366075b.webp?size=1024'

    @commands.command()
    async def wiki(self, ctx, *, text):
        string, image, url = requetes.wiki_search(text)
        embed = discord.Embed(title=f'**{text}**', color=0Xff751a, url=url)
        for i in self.__separe(string, 700):
            embed.add_field(name='\u200b', value=i, inline=False)
        embed.set_thumbnail(url=(f'https:{image}'))
        embed.set_footer(text="akitologique from wikipédia", icon_url=self.url_akito)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('💡')

    @commands.command()
    async def anime(self, ctx, *, text):
        try:
            anime, lang = text.split(' !')
        except:
            anime = text
            lang = "fr"
        anime = mal.Anime(mal.AnimeSearch(text, timeout=2).results[0].mal_id)
        embed = self.anime_embed(anime, lang)
        await ctx.send(embed=embed)

    @commands.command(name="randanime")
    async def random_anime(self, ctx, lang="fr"):
        nbr_anime = random.randint(1, 7612)
        anime = mal.Anime(nbr_anime)
        embed = self.anime_embed(anime, lang)
        await ctx.send(embed=embed)

    def anime_embed(self, anime, lang) -> discord.Embed:
        image = anime.image_url
        embed = discord.Embed(title=f'**{anime.title}**', color=0Xff751a, url=anime.url)
        embed.set_thumbnail(url=image)
        translate_syno, status, genres, main_char = ts.google(f"{anime.synopsis}****{anime.status}****{', '.join(anime.genres)}****{anime.characters[0].name}", 'en', lang).split("****")
        embed.add_field(name="**Synopsis**", value=f"{self.limite(translate_syno[:1000])}", inline=False)
        embed.add_field(name="**Nombre d'épisodes**", value=f"{anime.episodes}", inline=True)
        embed.add_field(name="**Genre**", value=genres, inline=True)
        embed.add_field(name="**Main character**", value=main_char)
        embed.add_field(name="**Score d'animé**", value=f"score :{anime.score}\nrank : {anime.rank}\npopularité: {anime.popularity}", inline=True)
        embed.add_field(name="**Status**", value=status, inline=True)
        embed.add_field(name="**Studios**", value=f"{', '.join(anime.studios)}", inline=True)
        embed.set_footer(text="Akitologique from MyAnimeList", icon_url=self.url_akito)
        return embed

    @commands.command()
    async def laros(self, ctx, *text):
        text = '_'.join(text)
        result, url = requetes.larousse(text)
        if isinstance(result, dict):
            embed = discord.Embed(title=f'__**{text}**__', descriprion=f"infos sur {text}", color=0Xff751a, url=url)
            (embed.add_field(name="__**Definitions**__", value='\n'.join(result['definition'][0:5]), inline=False)) if result['definition'] else None
            (embed.add_field(name="__**Exemples**__", value='\n'.join(result['exemple'][0:5]), inline=False)) if result['exemple'] else None
            (embed.add_field(name="__**Synonymes**__", value=('-'.join(result['synonymes'][0:5])), inline=False)) if result['synonymes'] else None
            embed.set_thumbnail(url='https://inti-revista.org/img/88ee1b0b5ffb5d79d9fb7192358ea0f9.png')
        elif isinstance(result, tuple):
            embed = discord.Embed(title='Erreur', descriprion="on a pas trouvé le mot que tu voulais :frowning:", color=0Xff751a)
            embed.set_thumbnail(url='https://th.bing.com/th/id/OIP.yFj56Xg-kXA5DH4HdpbnaQHaDt?w=321&h=174&c=7&o=5&pid=1.7')
            embed.add_field(name="__**Mot en relation**__", value="\n".join(i for i, j in result), inline=False)
        else:
            embed = discord.Embed(title='Error **404**', descriprion="page non trouvé", color=0Xff751a)
            embed.set_thumbnail(url='https://th.bing.com/th/id/OIP.IETjvTQTvCOFM0QmIBdhwgHaDZ?w=301&h=160&c=7&o=5&pid=1.7')
        embed.set_footer(text="akitologique from larousse.com", icon_url=self.url_akito)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('💡')

    @commands.command()
    async def conjugate(self, ctx, *verbe):
        temps = (" ".join(verbe[-2].split('-'))) if verbe[-2].lower() != "plus-que-parfait" else "plus-que-parfait"
        mode = verbe[-1]
        verbe = " ".join(verbe[:-2])
        a, description = requetes.larousse_conjug(verbe, temps, mode)
        if not a:
            embed = discord.Embed(title='Error **404**', descriprion="page non trouvé", color=0Xff751a)
            embed.set_thumbnail(url='https://th.bing.com/th/id/OIP.IETjvTQTvCOFM0QmIBdhwgHaDZ?w=301&h=160&c=7&o=5&pid=1.7')
            await ctx.send(embed=embed)
            return
        time, *verbes = a
        embed = discord.Embed(title=verbe, descriprion="le {verbe} au {time}", color=0Xff751a)
        embed.add_field(name=f'**__Conjugaison__** {verbe} au {time}', value=''.join(verbes))
        embed.set_thumbnail(url='https://th.bing.com/th/id/OIP.tXrdt78-XjVXIBwOoF1ERAHaHo?w=172&h=180&c=7&o=5&pid=1.7')
        embed.add_field(name='__description__', value=description, inline=False)
        embed.set_footer(text="akitologique from wikipédia", icon_url=self.url_akito)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('💡')


    def __separe(self, string, nbr):
        liste = []
        string2 = ''
        counter = 0
        is_time = False
        for i in string:
            string2 += i
            counter += 1
            if counter == nbr:
                is_time = True
            if i == ' ' and is_time:
                liste.append(string2)
                string2 = ''
                counter = 0
                is_time = False
        liste.append(string2)
        return liste

    def limite(self, string):
        limite = 1000 if len(string) >= 1000 else len(string)
        string[:limite]
        if limite != len(string):
            for i in range(limite, limite + 24):
                string += string[i]
                if string[i] == ' ':
                    break
        return string

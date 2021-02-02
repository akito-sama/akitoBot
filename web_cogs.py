import discord
from discord.ext import commands
import requetes


class WebCogs(commands.Cog):
    """docstring for WebCogs"""

    def __init__(self, bot: commands.Bot):
        super(WebCogs, self).__init__()
        self.bot = bot
        self.url_akito = 'https://cdn.discordapp.com/avatars/537430027479023627/8d60edbed8d2fa62e543dd086fefddb9.webp?size=1024'

    @commands.command()
    async def wiki(self, ctx, *text):
        text = " ".join(text)
        string, image, url = requetes.wiki_search(text)
        embed = discord.Embed(title=f'**{text}**', color=0Xff751a)
        for i in self.__separe(string, 600):
            embed.add_field(name='infos', value=i, inline=False)
        embed.set_thumbnail(url=(f'https:{image}') if not image.startswith('http') else image)
        embed.set_footer(text="akitologique", icon_url=self.url_akito)
        await ctx.send(embed=embed)

    @commands.command()
    async def laros(self, ctx, *text):
        text = ' '.join(text)
        result, url = requetes.larousse(text)
        if isinstance(result, dict):
            embed = discord.Embed(title=f'__**{text}**__', descriprion=f"infos sur {text}", color=0Xff751a, url=url)
            embed.add_field(name="__**Definitions**__", value='\n'.join(result['exemple']), inline=False)
            embed.add_field(name="__**Exemples**__", value='\n'.join(result['exemple']), inline=False)
            embed.add_field(name="__**Synonymes**__", value='-'.join(result['synonymes']), inline=False)
            embed.set_thumbnail(url='https://inti-revista.org/img/88ee1b0b5ffb5d79d9fb7192358ea0f9.png')
        elif isinstance(result, tuple):
            embed = discord.Embed(title='Erreur', descriprion="on a pas trouvé le mot que tu voulais :frowning:", color=0Xff751a)
            embed.set_thumbnail(url='https://th.bing.com/th/id/OIP.yFj56Xg-kXA5DH4HdpbnaQHaDt?w=321&h=174&c=7&o=5&pid=1.7')
            embed.add_field(name="__**Mot en relation**__", value="\n".join(i for i, j in result), inline=False)
        else:
            embed = discord.Embed(title='Error **404**', descriprion="page non trouvé", color=0Xff751a)
            embed.set_thumbnail(url='https://th.bing.com/th/id/OIP.IETjvTQTvCOFM0QmIBdhwgHaDZ?w=301&h=160&c=7&o=5&pid=1.7')
        embed.set_footer(text="akitologique", icon_url=self.url_akito)
        await ctx.send(embed=embed)


    @commands.command()
    async def conjugate(self, ctx, *verbe):
        temps = " ".join(verbe[-1].split('-'))
        verbe = " ".join(verbe[:-1])
        a = requetes.larousse_conjug(verbe, temps)
        if not a:
            embed = discord.Embed(title='Error **404**', descriprion="page non trouvé", color=0Xff751a)
            embed.set_thumbnail(url='https://th.bing.com/th/id/OIP.IETjvTQTvCOFM0QmIBdhwgHaDZ?w=301&h=160&c=7&o=5&pid=1.7')
            await ctx.send(embed=embed)
            return
        time, *verbes = a
        embed = discord.Embed(title=verbe, descriprion="le {verbe} au {time}", color=0Xff751a)
        embed.add_field(name=f'**__Conjugaison__** {verbe} au {time}', value=''.join(verbes))
        embed.set_thumbnail(url='https://th.bing.com/th/id/OIP.tXrdt78-XjVXIBwOoF1ERAHaHo?w=172&h=180&c=7&o=5&pid=1.7')
        await ctx.send(embed=embed)


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

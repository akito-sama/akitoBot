import discord
from discord.ext import commands
import random
import asyncio
from pendu import dictionnaire as dicto, liste

class GameCogs(commands.Cog):
    """docstring for WebCogs"""

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.url_akito = 'https://cdn.discordapp.com/avatars/537430027479023627/8d60edbed8d2fa62e543dd086fefddb9.webp?size=1024'
        self.get = discord.utils.get


    @commands.command()
    async def pfc(self, ctx):
        embed = discord.Embed(title="the game is started", description="le jeu de pierre feuille ciseau")
        embed.add_field(name="**défis**", value="chose your destiny :thumbsup:")
        embed.color = discord.Color(0Xff751a)
        message = await ctx.channel.send(embed=embed)
        list_emojis = ('🪨', '📜', '✂️')
        dico_issues = {
        "tu as gagné": ({"🪨": "✂️", "✂️": "📜", "📜": "🪨"}, "thumbsup"),
        "tu as perdu": ({"✂": "🪨", "📜": "✂️", "🪨": "📜"}, "frowning"),
        "egalité": ({"✂": "✂", "🪨": "🪨", "📜": "📜"}, "expressionless")
        }

        for emoji_ in list_emojis:
            await message.add_reaction(emoji_)
        try:
            reaction, user = await self.bot.wait_for("reaction_add", check=lambda rea, user: user == ctx.message.author and rea.message.id == message.id and rea.emoji in list_emojis, timeout=10)
            emoji = str(reaction.emoji)
            issue = random.choice(('tu as gagné', 'tu as perdu', 'égalité'))
            bot_choice = dico_issues[issue][0][emoji]
            description = f"le bot a choisi {bot_choice} et toi tu as choisi {emoji} donc {issue} :{dico_issues[issue][1]}:"
            embed = discord.Embed(title="**Result**", description=description)
            embed.color = discord.Color(0Xff751a)
            msg = await ctx.send(embed=embed)
        except:
            msg = await ctx.channel.send("les 10 secondes se sont ecoulé")
        await msg.add_reaction('💡')
        await message.add_reaction('💡')

    @commands.command()
    async def pendu(self, ctx):
        sob = discord.utils.get(ctx.guild.emojis, name='sobAnime')
        sob = sob if sob else ""
        is_win = False
        dico = {True: "tu as gagné bravo :thumbsup:", False: "tu as perdu :frowning:"}
        theme = random.choice([*dicto.keys()])
        mot = list(random.choice(dicto[theme]).lower())
        bienvenue = await ctx.channel.send(f"salut c'est akito le jeu du pendu a commencé\nle thème du mots est `{theme}`")
        mot_cache = ['-' for i in range(len(mot))]
        errors_nbr = 0
        dessin = await ctx.channel.send(liste[0])
        message = await ctx.channel.send(f"voici le mot : {''.join(mot_cache)}")
        try:
            while errors_nbr != 5 and mot != mot_cache:
                await message.edit(content=f"voici le mot : {''.join(mot_cache)}")
                lettr = await self.bot.wait_for("message", check=lambda msg: ctx.message.author == msg.author and ctx.channel == msg.channel, timeout=60)
                lett = lettr.content
                await lettr.delete()
                if len(lett) == 1:
                    if lett not in mot_cache and lett in mot:
                        list_ = self.indexs(mot, lett)
                        for i in list_:
                            mot_cache[i] = lett
                        if mot == mot_cache:
                            is_win = True
                    else:
                        await ctx.channel.send("le lettre n'éxiste pas dans mots", delete_after=1)
                        errors_nbr += 1
                        await dessin.edit(content=liste[errors_nbr])
                else:
                    await ctx.channel.send("désolé mais la lettre doit contenir une seul lettre", delete_after=1)

        except:
            msg = await ctx.channel.send(f"le temps akitologique s'est écoulé\n{sob}")
            await msg.add_reaction('💡')

        winner = await ctx.channel.send(f"{dico[is_win]} et le mot était ...")
        iterable = iter((3, 2, 1, ''.join(mot)))
        msg = await ctx.send(str(next(iterable)))
        for i in range(3):
            await asyncio.sleep(1)
            await msg.edit(content=str(next(iterable)))
        for i in (dessin, message, bienvenue, msg, winner):
            await i.add_reaction('💡')

    def indexs(self, liste: list, element):
        j = []
        for i in range(len(liste)):
            if liste[i] == element:
                j.append(i)
        return j

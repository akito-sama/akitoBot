from discord.ext import commands, tasks
import discord, asyncio, random, youtube_dl
from pendu import liste
from formats import dictionnaire as dicto
from math_parse import calculate
from secret import token


class Akito():
    pass

bot = commands.Bot(command_prefix="!", description="le bot akitologique", help_command=None)
bot.remove_command("help")
rules_ = "les regles sont :\npas d'insultes\npas de moqueries\ns'amuser avec la communité"
get = discord.utils.get
tube = youtube_dl.YoutubeDL()
musics = {}
akito = Akito()

class Video:
    """docstring for Video cherche pas à comprendre"""
    def __init__(self, link):
        video = tube.extract_info(link, download=False)
        format_ = video["formats"][0]
        self.name = video['title']
        self.url = video['webpage_url']
        self.stream_url = format_["url"]

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="en train d'être akitologique", type=discord.ActivityType.custom))
    print("akito est pret pour faire de l'akitologie")

@bot.event
async def on_message(message):
    try:
        liste = ["slm", "hello", "bonjour", "ohayo", "salam", "hi"]
        if message.content.split()[0] in liste and message.author == bot.get_user(537430027479023627) and message.guild.id == 716083740836888587:
            await message.channel.send(f"{message.content.split()[0]} mon createur akito")
        elif message.content in liste:
            await message.channel.send("je t'aime pas toi ")
    except:
        ...
    await bot.process_commands(message)


@bot.event
async def on_member_join(member):
    emoji = get(bot.guild.emojis, name="hehe")
    channel = await bot.get_channel(746085597357146273)
    channel.send(f"bienvenu à toi {member} je te souhaite un bon acceuil akitologique {emoji} ici veillez lire les règles svp\n et mettre un :white_check_mark: dans les reactions stp")


@bot.event
async def on_raw_reaction_add(payload):
    pass

@bot.command()
async def skip(ctx):
    client = ctx.guild.voice_client
    client.stop()

def play_song(client, queue, music):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(music.stream_url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"), 1.5)   
    def next(_):
        if len(queue) > 0:
            music2 = queue[0]
            del queue[0]
            play_song(client, queue, music2)
        else:
            asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)
    client.play(source, after=next)


@bot.command()
async def queue(ctx):
    embed = discord.Embed(title=f"** la queue de {ctx.guild.name}**", description='Musics')
    if ctx.guild in [*musics.keys()] and len(musics[ctx.guild]) > 0:
        value = "\n".join([i.name for i in musics[ctx.guild]])
    else:
        value = "la queue est vide"
    embed.add_field(name="les musics", value=value)
    embed.set_footer(text="akitologique", icon_url=akito_image_url)
    embed.set_thumbnail(url="https://th.bing.com/th/id/OIP.lkVlOtVvcbOVnLxiefC0CwHaFj?pid=Api&rs=1")
    await ctx.send(embed=embed)


@bot.command()
async def play(ctx, url):
    client = ctx.guild.voice_client
    if client and client.channel:
        video = Video(url)
        musics[ctx.guild].append(video)
        await ctx.send(f"la musique {video.name} a été ajouté dans la queue de chansons")
    else:
        channel = ctx.author.voice.channel
        video = Video(url)
        musics[ctx.guild] = []
        client = await channel.connect()
        await ctx.channel.send(f"la music {video.name} a commencé bonne séance")
        play_song(client, musics[ctx.guild], video)


@bot.command()
async def pause(ctx):
    client = ctx.guild.voice_client
    if not client.is_paused():
        client.pause()
    else:
        ctx.send("le bot est dèjà en pause")


@bot.command()
async def continu(ctx):
    client = ctx.guild.voice_client
    if client.is_paused():
        client.resume()
    else:
        ctx.send("le bot est dèjà en marche")


bot.command()
async def disconnect(ctx):
    client = ctx.guild.voice_client
    await client.disconnect()


@bot.command()
async def infos(ctx):
    server = ctx.guild
    embed = discord.Embed(title=f"------------ server {server.name} ------------", description="les infos du serveur")
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    server_info = f""" nbr of membres : {server.member_count}
nbr of text channel : {len(server.text_channels)}
nbr of voice channel : {len(server.voice_channels)}
description : {server.description}
"""
    embed.set_footer(text="akitologique", icon_url=akito.avatar)
    embed.add_field(name="__infos__", value=server_info)
    embed.set_thumbnail(url=server.icon_url)
    embed.color = discord.Color(0Xff751a)
    await ctx.channel.send(embed=embed)


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, nbr, member: discord.Member=None,*reason):
    reason = " ".join(reason)
    await ctx.channel.send("in deleting ...")
    messages = await ctx.channel.history(limit=int(nbr) + 2).flatten()
    for message in messages:
        if message.author == member or member == None:
            await message.delete()
    if reason:
        await ctx.channel.send(f"les messages ont été supprimé par reason : {reason}")


@bot.command(name="akito")
async def me(ctx):
    dico = {False: "smile", True: "heart"}
    embed = discord.Embed(title=f"** Mon createur Akito :{dico[ctx.author.name == 'akito']}: **", description="ce n'est pas un être humain")
    embed.set_thumbnail(url=akito.avatar)
    embed.set_footer(text="akitologique", icon_url=akito.avatar)
    await ctx.send(embed=embed)


@bot.command()
async def avatar(ctx, member: discord.Member=None):
    member = ctx.author if not member else member
    if isinstance(member, discord.Member):
        if not str(member.activity) == "None":
            embed = discord.Embed(title=f"{member.name}", description=f"{member.activity}")
        else:
            embed = discord.Embed(title=f"{member.name}")
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)
    else:
        await ctx.send(member.avatar_url)



@bot.command()
async def say(ctx, nbr=1, *text):
    text = " ".join(text)
    for i in '_'*int(nbr):
        await ctx.channel.send(text)


@bot.command()
async def pfc(ctx):
    embed = discord.Embed(title="the game is started", description="le jeu de pierre feuille ciseau")
    embed.add_field(name="**défis**", value="chose your destiny :thumbsup:")
    embed.color = discord.Color(0Xff751a)
    message = await ctx.channel.send(embed=embed)
    rock = get(ctx.message.guild.emojis, name="rock")
    paper = get(ctx.message.guild.emojis, name="paper")
    scisor = get(ctx.message.guild.emojis, name="ciseaux")
    list_emojis = [rock, paper, scisor]
    for emoji_ in list_emojis:
        await message.add_reaction(emoji_)
    try:
        emoji, user = await bot.wait_for("reaction_add", check=lambda rea, user: user == ctx.message.author and rea.message.id == message.id and rea.emoji in list_emojis, timeout=10)
        emoji = emoji.emoji
        choice = random.choice(list_emojis)
        if (choice == rock and emoji == paper) or (choice == paper and emoji == scisor) or (choice == scisor and emoji == rock): 
            answer = f"le bot a choisi le {choice} et tu as choisi le {emoji} bien joué tu as gagné :thumbsup:"
        elif choice == emoji:
        	answer = f"le bot a choisi le {choice} et tu as choisi le {emoji} donc egalité :neutral_face:"
        else:
            answer = f"le bot a choisi le {choice} et tu as choisi le {emoji} bonne chance la prochaine fois :frowning:"
        embed = discord.Embed(title="**Result**", description=answer)
        embed.color = discord.Color(0Xff751a)
        await ctx.send(embed=embed)
    except:
        await ctx.channel.send("les 10 secondes se sont ecoulé")


def indexs(liste: list, element):
    j = []
    for i in range(len(liste)):
        if liste[i] == element:
            j.append(i)
    return j


@bot.command()
async def pendu(ctx):
    sob = discord.utils.get(ctx.guild.emojis, name='sobAnime')
    is_win = False
    dico = {True: "tu as gagné bravo :thumbsup:", False: "tu as perdu :frowning:"}
    await ctx.channel.send("salut c'est akito le jeu du pendu a commencé")
    theme = random.choice([*dicto.keys()])
    mot = list(random.choice(dicto[theme]).lower())
    await ctx.channel.send(f"le thème du mots est `{theme}`")
    mot_cache = ['-' for i in range(len(mot))]
    errors_nbr = 0
    dessin = await ctx.channel.send(liste[0])
    message = await ctx.channel.send(f"voici le mot : {''.join(mot_cache)}")
    try:
        while errors_nbr != 5 and mot != mot_cache:
            await message.edit(content=f"voici le mot : {''.join(mot_cache)}")
            lettr = await bot.wait_for("message", check=lambda msg: ctx.message.author == msg.author and ctx.channel == msg.channel, timeout=60)
            lett = lettr.content
            if len(lett) == 1:
                if lett not in mot_cache and lett in mot:
                    list_ = indexs(mot, lett)
                    for i in list_:
                        mot_cache[i] = lett
                    if mot == mot_cache:
                        is_win = True
                else:
                    b = await ctx.channel.send("le lettre n'éxiste pas dans mots", delete_after=1)
                    await b.delete()
                    errors_nbr += 1
                    await dessin.edit(content=liste[errors_nbr])
            else:
                await ctx.channel.send("désolé mais la lettre doit contenir une seul lettre", delete_after=1)
            await lettr.delete()
    except:
        await ctx.channel.send(f"le temps akitologique s'est écoulé")
        await ctx.channel.send(f"{sob}")

    await ctx.channel.send(f"{dico[is_win]} et le mot était ...")
    for i in range(3):
        await asyncio.sleep(1)
        await ctx.channel.send(f"{abs(i - 3)} ...", delete_after=0.5)
    await ctx.channel.send(f"**{''.join(mot)}**")


@bot.command()
async def rules(ctx):
    embed = discord.Embed(title="__**Rules**__", description=rules_)
    embed.color = discord.Color(0Xff751a)
    embed.set_thumbnail(url="https://dockdogs.com/wp-content/uploads/2014/08/rule-icon.png")
    await ctx.channel.send(embed=embed)

@bot.command(name="calculate")
async def calculat(ctx, *operation):
    operation = " ".join(operation)
    embed = discord.Embed(title="**__Operation__**", description=operation)
    embed.set_author(name=ctx.author.nick, icon_url=ctx.author.avatar_url)
    embed.color = discord.Color(0Xff751a)
    try:
        result = calculate(operation)
        embed.set_thumbnail(url="https://th.bing.com/th/id/OIP.-h37unfw4U8Fz14M7cwb0QHaD2?pid=Api&rs=1")
        embed.add_field(name="__**Result**__", value=result)
    except:
        embed.set_thumbnail(url="https://th.bing.com/th/id/OIP.iJZ0AGMvTlZd54hJ76YjAAHaDo?pid=Api&rs=1")
        embed.add_field(name="**Error**", value="cette command n'est pas fini donc elle est pleine de beug")
    await ctx.send(embed=embed)

@bot.command(name="close")
async def close_bot(ctx):
    embed = discord.Embed()
    embed.color = discord.Color(0Xff751a)
    embed.set_author(name=ctx.author.nick, icon_url=ctx.author.avatar_url)
    if ctx.author.id == 537430027479023627:
        embed.set_thumbnail(url="https://th.bing.com/th/id/OIP.j03BRzxVYjrPAftq_weMWgAAAA?pid=Api&rs=1")
        embed.add_field(name="**ETAT**", value="je suis eteint")
        embed.title = "__Eteint__"
        await ctx.send(embed=embed)
        await bot.logout()
        await bot.close()
    else:
        embed.add_field(name="**ERROR**", value="vous ne pouvez pas utiliser cette command")
        await ctx.send(embed=embed)

@bot.command(name="kimi")
async def help(ctx):
    me = ctx.guild.get_member(785865184253837322)
    embed = discord.Embed(title="__**Me**__", description="moi je ne suis qu'un bot fait par un inhumain")
    embed.set_thumbnail(url=me.avatar_url)
    embed.color = discord.Color(0Xff751a)
    embed.add_field(name="commands :", value="""
__**!infos**__ : permet de get les infos du serveur
__**!rules**__ : permet d'envoyer les règles du serveur
__**!pendu**__ : c'est le jeu du pendu
__**!pfc**__ : joue à pierre feuille ciseau avec moi
__**!kimi**__ : envoie ce que tu lis maintenant
__**!say**__ : permet de spam mais ne l'utilisez pas beaucoup ok :frowning:
__**!avatar**__ : permet de voir ta pdp ou celle d'un membre
__**!akito**__ : permet de savoir plus sur mon créateur (ou pas beaucoup en vrai)
__**!clear**__ : permet de supprimer un nombre de message
__**!play**__ : permet de lire les musiques de youtube à l'aide de l'url si la musique est dèjà lancé alors la musique est ajouté dans la queue
__**!queue**__ : permet de voir les musique de la queue
__**!pause**__ : permet de mettre la musique en pause
__**!continu**__ : permet de reprendre la musique mit en pause
__**!disconnect**__ :  permet de deconnecter le bot du salon de musique
__**!skip**__ : permet de sauter la musique courante et aller vers la prochaine musique dans la queue
""")
    akito.member = bot.get_user(537430027479023627)
    akito.avatar = akito.member.avatar_url
    embed.set_footer(text="akitologique", icon_url=akito.avatar)
    await ctx.send(embed=embed)

bot.run(token)

from discord.ext import commands, tasks
import discord
from math_parse import calculate
from secret import token
import web_cogs, games, music
import translators as ts


bot = commands.Bot(command_prefix="!!", description="le bot akitologique", help_command=None)
bot.remove_command("help")
rules_ = "les regles sont :\npas d'insultes\npas de moqueries\ns'amuser avec la communité"
get = discord.utils.get
cogs = (web_cogs.WebCogs(bot), games.GameCogs(bot), music.MusicCogs(bot))


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="en train d'être akitologique", type=discord.ActivityType.custom))
    print("akito est pret pour faire de l'akitologie")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    salutation = ("slm", "hello", "bonjour", "ohayo", "salam", "hi", "salut")
    work = any(tuple(message.content.lower().startswith(i.lower()) for i in salutation))
    if work and message.author.id == 537430027479023627:
        await message.channel.send(f"salut mon createur akito ❤")
    elif work:
        await message.channel.send("je t'aime pas toi")
    if message.content.startswith("!!"):
        await message.add_reaction('💡')
    await bot.process_commands(message)


@bot.event
async def on_member_join(member):
    emoji = get(bot.guild.emojis, name="hehe")
    channel = await bot.get_channel(746085597357146273)
    channel.send(f"bienvenu à toi {member} je te souhaite un bon acceuil akitologique {emoji} ici veillez lire les règles svp\n et mettre un :white_check_mark: dans les reactions stp")


@bot.event
async def on_reaction_add(reaction: discord.Reaction, user):
    if str(reaction.emoji) == '💡' and bot.user in await reaction.users().flatten() and user != bot.user :
        await reaction.message.delete()


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
    embed.set_footer(text="akitologique", icon_url=cog.url_akito)
    embed.add_field(name="__infos__", value=server_info)
    embed.set_thumbnail(url=server.icon_url)
    embed.color = discord.Color(0Xff751a)
    msg = await ctx.channel.send(embed=embed)
    await msg.add_reaction('💡')


@bot.event
async def on_command_error(ctx, error):
    embed = discord.Embed(title='Error **404**', descriprion="une erreur a été produite", color=0Xff751a)
    embed.set_thumbnail(url='https://th.bing.com/th/id/OIP.IETjvTQTvCOFM0QmIBdhwgHaDZ?w=301&h=160&c=7&o=5&pid=1.7')
    embed.set_footer(text="akitologique", icon_url=cog.url_akito)
    if isinstance(error, commands.MissingRequiredArgument):
        message = 'désolé mais tu as oublié un argument donc tu peux recommencer en mettant le bon argument'
    elif isinstance(error, commands.CommandNotFound):
        message = "j'ai l'impréhesion que cette commande n'existe pas mais tout existe et n'existe pas selon l'akitologie\nvu la theorie de la realité personnel :)"
    elif isinstance(error, commands.MissingPermissions):
        message = "tu n'a pas les permissions de cette commande"
    else:
        message = f"une erreur s'est produite"
    embed.add_field(name='__type :__ ', value=message)
    message = await ctx.send(embed=embed)
    await message.add_reaction('💡')


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, nbr, member: discord.Member = None, *reason):
    reason = " ".join(reason)
    await ctx.channel.send("in deleting ...", delete_after=0.5)
    messages = await ctx.channel.history(limit=int(nbr) + 2).flatten()
    for message in messages:
        if message.author == member or member is None:
            await message.delete()
    if reason:
        msg = await ctx.channel.send(f"les messages ont été supprimé par reason : {reason}")
        await msg.add_reaction('💡')


@bot.command(name="akito")
async def me(ctx):
    dico = {False: "smile", True: "heart"}
    embed = discord.Embed(title=f"** Mon createur Akito :{dico[ctx.author.name == 'akito']}: **", description="ce n'est pas un être humain")
    embed.set_thumbnail(url=cog.url_akito)
    embed.set_footer(text="akitologique", icon_url=cog.url_akito)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('💡')


@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = ctx.author if not member else member
    if not str(member.activity) == "None":
        embed = discord.Embed(title=f"{member.name}", description=f"{member.activity}")
    else:
        embed = discord.Embed(title=f"{member.name}")
    embed.set_thumbnail(url=member.avatar_url)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('💡')


@bot.command()
async def say(ctx, nbr=1, *text):
    text = " ".join(text)
    nbr = 10 if nbr >= 10 else nbr
    for i in '_' * int(nbr):
        await ctx.channel.send(text)


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
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("💡")


@bot.command(name="close")
async def close_bot(ctx):
    if ctx.author.id == 537430027479023627:
        embed = discord.Embed()
        embed.color = discord.Color(0Xff751a)
        embed.set_author(name=ctx.author.nick, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url="https://th.bing.com/th/id/OIP.j03BRzxVYjrPAftq_weMWgAAAA?pid=Api&rs=1")
        embed.add_field(name="**ETAT**", value="je suis eteint")
        embed.title = "__Eteint__"
        msg = await ctx.send(embed=embed)
        msg.add_reaction('💡')
        await bot.logout()
        await bot.close()


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
    embed.set_footer(text="akitologique", icon_url=cog.url_akito)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("💡")


@bot.command()
async def update(ctx):
    if ctx.author.id == 537430027479023627:
        for cog in cogs:
            cog.url_akito = ctx.author.avatar_url
        await ctx.send(f"c'est changé :blush: en {ctx.author.avatar_url}")

# run le bot
for cog in cogs:
    bot.add_cog(cog)
bot.run(token)

#Discord Simplon Bot
#Author: RAPHAEL.L
#Fabrique: Cannes 06
#Formation: Dev Data#1
#Language: Python

import discord, os, random, emoji, nest_asyncio, asyncio, simplon_lib as sl, google_query
from discord.ext import commands
from discord.ext.commands import CommandNotFound

bot = commands.Bot(command_prefix='!')
footer_embed = ':link: [Rejoingnez le Projet!](https://discord.gg/zgKJwGh) | Simplon#InCodeWeTrust'

##Commande du bot qui affiche l'aide(les commandes)
@bot.command(name='aide')
async def aide(ctx):
    bot_cmd = ('**!s_veille "RECHERCHE"** - Affiche les 5 premiers lien en rapport avec la recherche demandé\n'
    '**!s_sondage "TITRE" "DESCRIPTION(optionnel)" "EMOJI(optionnel)"** - Créer un sondage avec le titre, la description & les emoji choisi\n'
    '**!s_places** - Génère les places de chaque apprenant aléatoirement.\n'
    '**!s_app** - Génère **UN** apprenant aléatoirement')
    embedVar = discord.Embed(title="Aide Bot Simplon:", description="Affichage des commandes pour l'utilisation du Bot Simplon", url=f"https://simplonline.co", color=0xdf0000)
    embedVar.set_author(name="Simplon'Bot", icon_url=ctx.guild.icon_url)
    embedVar.set_thumbnail(url="https://simplon.co/images/logo-simplon.png")
    embedVar.add_field(name="__Commandes:__", value=bot_cmd, inline=False)
    embedVar.add_field(name="\u200b", value=footer_embed, inline=False)
    embedVar.set_footer(text="developped by R.L. / Simplon 2020")
    await ctx.channel.send(embed=embedVar)
    await ctx.message.delete()

##Commande du bot qui lance la génération aléatoire des places pour chaque apprenant
@bot.command(name='s_places')
async def random_places(ctx):
    members = list(ctx.guild.members)
    random.shuffle(members)
    embedVar = discord.Embed(title="Emplacements des Apprenants:", description="Tirage aux sort des places pour chaque apprenant", url=f"https://simplonline.co", color=0xdf0000)
    embedVar.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
    embedVar.set_thumbnail(url="https://simplon.co/images/logo-simplon.png")
    embedVar.add_field(name="__Apprenants:__", value=sl.RandomStudentsPlaces(members), inline=False)
    embedVar.add_field(name="** **", value=footer_embed, inline=False)
    embedVar.set_footer(text="developped by R.L. / Simplon 2020")
    await ctx.channel.send(embed=embedVar)
    await ctx.message.delete()

##Commande du bot qui lance la génération aléatoire d'un apprenant
@bot.command(name='s_app')
async def random_student(ctx):
    students = sl.getStudents(list(ctx.guild.members))
    random_student = random.choice(students)
    student_name = random_student.name if not random_student.nick else random_student.nick
    embedVar = discord.Embed(title="Apprenants Aléatoire:", description="Tirage aux sort d'un apprenant", url=f"https://simplonline.co", color=0xdf0000)
    embedVar.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
    embedVar.set_thumbnail(url="https://simplon.co/images/logo-simplon.png")
    embedVar.add_field(name="__Apprenant Séléctionné:__", value="**"+student_name+"**", inline=False)
    embedVar.add_field(name="** **", value=footer_embed, inline=False)
    embedVar.set_footer(text="developped by R.L. / Simplon 2020")
    await ctx.channel.send(embed=embedVar)
    await ctx.message.delete()

##Commande du bot pour faire une recherche rapide sur un sujet de veille demandé
@bot.command(name='s_veille')
async def test(ctx, keyword):
    waiting_msg = await ctx.send("Recherche en cour... :face_with_monocle: ["+keyword+"]")
    embedVar = discord.Embed(title="Sujet de veille: \""+keyword+"\"", description="Recherche rapide des liens en rapport avec le sujet de Veille", url=f"https://simplonline.co", color=0xdf0000)
    embedVar.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
    embedVar.set_thumbnail(url="https://simplon.co/images/logo-simplon.png")
    embedVar.add_field(name="__Liens trouvés:__", value="**"+google_query.googleQuery(keyword)+"**", inline=False)
    embedVar.add_field(name="** **", value=footer_embed, inline=False)
    embedVar.set_footer(text="developped by R.L. / Simplon 2020")
    await waiting_msg.delete()
    await ctx.channel.send(embed=embedVar)
    await ctx.message.delete()

##Commande du bot pour lancé un nouveau Sondage avec parametre (Question, Smileys, Temps en Heure)
@bot.command(name='s_sondage')
async def sondage(ctx, question=None, description="Sondage", react='', limitReact="NON"):
    reactions = ''.join(c for c in react if c in emoji.UNICODE_EMOJI)
    if question == None:
        await ctx.author.send("Vous devez donner un intitulé a votre sondage.")
        return
    if not reactions and limitReact.upper() == "OUI":
        await ctx.author.send("Emoji's invalide.(Utilser jusqu'a 10 emoji entre guillemets, ex: ✅❌)")
        return
    if len(reactions) > 10:
        await ctx.author.send("Le nombre maximal d'Emoji est limité a 10.")
        return
    if(len(reactions) != len(react)):
        await ctx.author.send("Certains emojis séléctionnés ne sont pas compatible, elles n'apparaitrons pas.\nSi vous n'avez pas activé la limitation d'Emoji vous pouvez la rajouter manuellement après la création du Sondage.")
    await ctx.message.delete()

    dateYMD = await sl.checkDateTime(bot, ctx, True)
    dateHMS = await sl.checkDateTime(bot, ctx, False, True)
    timerExpire = await sl.isDateExpired(dateYMD+' '+dateHMS)
    if (True if timerExpire < 0 else False):
        await ctx.auhor.send(":x: La Date est expiré. Veuillez saisir une date valide.")
        dateYMD = await sl.checkDateTime(bot, ctx, True)
        dateHMS = await sl.checkDateTime(bot, ctx, False, True)

    async def getReactUsers(init=False):
        author_name = ctx.message.author.name if not ctx.message.author.nick else ctx.message.author.nick
        updateEmbedVar = discord.Embed(title="**"+question+"**", description=description+"\nAuteur: "+ author_name, url=f"https://simplonline.co", color=0xdf0000)
        updateEmbedVar.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        updateEmbedVar.set_thumbnail(url="https://simplon.co/images/logo-simplon.png")
        if not init:
            cache_msg = discord.utils.get(bot.cached_messages, id=react_message.id)
            for reaction in cache_msg.reactions:
                userLst = "\u200b"
                async for user in reaction.users():
                    if user.bot == False:
                        userLst += ("<@"+str(user.id)+">\n")
                if reaction.emoji in reactions or limitReact.upper() == "NON":
                    updateEmbedVar.add_field(name="Votes **"+reaction.emoji+"** ("+str(userLst.count("\n"))+")", value=userLst, inline=True)
        updateEmbedVar.add_field(name="** **", value=footer_embed, inline=False)
        updateEmbedVar.set_footer(text="developped by R.L. / Simplon 2020 | Le sondage sera cloturé le {0}.".format(dateYMD+' à '+dateHMS))
        return updateEmbedVar

    react_message = await ctx.send(embed=await getReactUsers(True))
    for reaction in reactions:
        await react_message.add_reaction(reaction)
    await react_message.edit(embed=await getReactUsers())

    def checkReact(reaction, user):
      return user.bot == False and (str(reaction.emoji) in reactions or limitReact.upper() == "NON")

    pollOpen = True
    while pollOpen == True:
        try:
            pending_tasks = [bot.wait_for('reaction_add', timeout=timerExpire,check=checkReact), bot.wait_for('reaction_remove', timeout=timerExpire,check=checkReact)]
            done_tasks, pending_tasks = await asyncio.wait(pending_tasks, return_when=asyncio.FIRST_COMPLETED)

            for task in done_tasks:
                reaction, user = await task
                await react_message.edit(embed=await getReactUsers())
        except asyncio.TimeoutError:
           # await ctx.send('Poll fermé!')
           pollOpen = False



##Si la commande entré par l'utilisateur n'existe pas, on anticipe l'erreur
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    print(error)

##Event Log de l'execution du Bot
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name="#In Code We Trust(!aide)"))

bot.run(os.environ['token'])

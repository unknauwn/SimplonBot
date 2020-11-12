#Discord Simplon Bot
#Author: RAPHAEL.L
#Fabrique: Cannes 06
#Formation: Dev Data#1
#Language: Python

import discord, os, random, emoji, nest_asyncio, asyncio, simplon_lib as sl, google_query
from discord.ext import commands
from discord.ext.commands import CommandNotFound

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)
footer_embed = ':link: [Rejoignez le Projet!](https://discord.gg/zgKJwGh) | Simplon#InCodeWeTrust'

##Commande du bot qui affiche l'aide(les commandes)
@bot.command(name='aide')
async def aide(ctx):
    bot_cmd = ('**!s_veille "RECHERCHE"** - Affiche les 5 premiers liens en rapport avec la recherche demandée\n'
    '**!s_sondage "TITRE" "DESCRIPTION"** *(optionnel)* **"EMOJI"** *(optionnel)* **"OUI/NON"** *(optionnel, empêche les utilisateurs d\'ajouter de nouveaux Emoji)* - Créer un sondage avec le titre, la description & les emoji choisi\n'
    '**!s_places** - Génère les places de chaque apprenant aléatoirement.\n'
    '**!s_app** - Génère **UN** apprenant aléatoirement\n'
    '**!s_rand "MIN" "MAX"** - Génère **UN** nombre aléatoirement entre le MIN et le MAX spécifié(Par defaut entre 1 et 5)\n'
    '**!s_groupes "NUM_PAR_GROUPE"** - Génère des groupes aléatoires d\'apprenants(Par defaut 5 par groupe)')
    embedVar = discord.Embed(title="Aide Bot Simplon:", description="Affichage des commandes pour l'utilisation du Bot Simplon", url=f"https://simplonline.co", color=0xdf0000)
    embedVar.set_author(name="Simplon'Bot", icon_url=ctx.guild.icon_url)
    embedVar.set_thumbnail(url="https://simplon.co/images/logo-simplon.png")
    embedVar.add_field(name="__Commandes:__", value=bot_cmd, inline=False)
    embedVar.add_field(name="\u200b", value=footer_embed, inline=False)
    embedVar.set_footer(text="developped by R.L. / Simplon 2020")
    await ctx.channel.send(embed=embedVar)
    await ctx.message.delete()

##Commande du bot pour faire un random
@bot.command(name='s_rand')
async def random_number(ctx, minnum = "1", maxnum="5"):
    if minnum.isdecimal() == False or maxnum.isdecimal() == False:
        await ctx.author.send(":x: Les valeurs doivent être des nombres entiers.")
        await ctx.message.delete()
        return
    number = random.randint(int(minnum), int(maxnum))
    embedVar = discord.Embed(title="Génération d'un nombre aléatoirement", description="Génére un nombre aléatoirement entre {} et {}:".format(minnum, maxnum), url=f"https://simplonline.co", color=0xdf0000)
    embedVar.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
    embedVar.set_thumbnail(url="https://simplon.co/images/logo-simplon.png")
    embedVar.add_field(name="__Resultat:__", value=number, inline=False)
    embedVar.add_field(name="** **", value=footer_embed, inline=False)
    embedVar.set_footer(text="developped by R.L. / Simplon 2020")
    await ctx.channel.send(embed=embedVar)
    await ctx.message.delete()

##Commande du bot qui lance la génération aléatoire des places pour chaque apprenant
@bot.command(name='s_places')
async def random_places(ctx):
    members = list(ctx.guild.members)
    random.shuffle(members)
    embedVar = discord.Embed(title="Emplacements des Apprenants:", description="Tirage au sort des places pour chaque apprenant", url=f"https://simplonline.co", color=0xdf0000)
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
    embedVar = discord.Embed(title="Apprenant Aléatoire", description="Séléction aléatoire d'un apprenant", url=f"https://simplonline.co", color=0xdf0000)
    embedVar.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
    embedVar.set_thumbnail(url="https://simplon.co/images/logo-simplon.png")
    embedVar.add_field(name="__Apprenant Séléctionné:__", value="**"+student_name+"**", inline=False)
    embedVar.add_field(name="** **", value=footer_embed, inline=False)
    embedVar.set_footer(text="developped by R.L. / Simplon 2020")
    await ctx.channel.send(embed=embedVar)
    await ctx.message.delete()

##Commande du bot qui lance une génération aléatoire de groupes d'apprenants
@bot.command(name='s_groupes')
async def random_groups(ctx, num_groups="4"):
    if num_groups.isdecimal() == False:
        await ctx.author.send(":x: Le nombre de groupe doit etre un nombre entier.")
        await ctx.message.delete()
        return
    members = list(ctx.guild.members)
    random.shuffle(members)
    students_group = sl.RandomStudentsGroups(members, int(num_groups))
    embedVar = discord.Embed(title="Liste des Groupes:", description="Génération aléatoire de groupe contenant {} d'apprenant(s)".format(num_groups), url=f"https://simplonline.co", color=0xdf0000)
    embedVar.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
    embedVar.set_thumbnail(url="https://simplon.co/images/logo-simplon.png")
    for index, group in enumerate(students_group):
        embedVar.add_field(name="__Groupes {}:__".format(index+1), value='\n'.join([sl.getEmojiByIndex((i+1)+index*int(num_groups))+' : **'+u.name+'**' for i, u in enumerate(group) if not u.bot]), inline=False)
    embedVar.add_field(name="** **", value=footer_embed, inline=False)
    embedVar.set_footer(text="developped by R.L. / Simplon 2020")
    await ctx.channel.send(embed=embedVar)
    await ctx.message.delete()

##Commande du bot pour faire une recherche rapide sur un sujet de veille demandé
@bot.command(name='s_veille')
async def veille(ctx, keyword):
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
async def sondage(ctx, question=None, description="Sondage Rapide\nRéagissez avec des Emoji's cohérent.", react='', limitReact="non"):
    reactions = ''.join(c for c in react if c in emoji.UNICODE_EMOJI)
    if question == None:
        await ctx.author.send("Vous devez donner un intitulé a votre sondage.")
        return
    if not reactions and limitReact.lower() == "oui":
        await ctx.author.send("Emoji's invalide.(Utilser jusqu'a 10 emoji entre guillemets, ex: ✅❌)")
        return
    if len(reactions) > 10:
        await ctx.author.send("Le nombre maximal d'Emoji est limité a 10.")
        return
    if(len(reactions) != len(react.replace(' ',''))):
        await ctx.author.send("Certains emojis séléctionnés ne sont pas compatible, elles n'apparaitrons pas.\nSi vous n'avez pas activé la limitation d'Emoji vous pouvez la rajouter manuellement après la création du Sondage.")
    await ctx.message.delete()

    author_name = (ctx.message.author.name if not ctx.message.author.nick else ctx.message.author.nick)
    dateYMD = await sl.checkDateTime(bot, ctx, True)
    dateHMS = await sl.checkDateTime(bot, ctx, False, True)
    timerExpire = await sl.isDateExpired(dateYMD+' '+dateHMS)
    while (True if timerExpire < 0 else False):
        await ctx.author.send(":x: La Date est expiré. Veuillez saisir une date valide.")
        dateYMD = await sl.checkDateTime(bot, ctx, True)
        dateHMS = await sl.checkDateTime(bot, ctx, False, True)

    ## On créer la fonction qui permet de recuperer le nombre de reaction total & l'objet Reaction qui contient les data d'user pour chaque reactions
    async def getUsersReact():
        user_react = {"total_user": 0, "user_react":[]}
        try:
            cache_msg = discord.utils.get(bot.cached_messages, id=react_message.id)
            for reaction in cache_msg.reactions:
                users = await reaction.users().flatten()
                users = [u for u in users if not u.bot]
                user_react["total_user"] += len(users)
                user_react["user_react"].append(reaction)
            return user_react
        except NameError:
            return user_react

    ## On créer la fonction qui permet de créer/mettre a jour l'embed du sondage
    async def makeEmbedPoll():
        user_react_data = await getUsersReact()
        timerExpire = await sl.isDateExpired(dateYMD+' '+dateHMS)
        updateEmbedVar = discord.Embed(title="**"+question+"**", description=description, url=f"https://simplonline.co", color=0xdf0000)
        updateEmbedVar.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        updateEmbedVar.set_thumbnail(url="https://simplon.co/images/logo-simplon.png")
        updateEmbedVar.add_field(name="**:speaking_head: Auteur**", value=author_name, inline=True)
        updateEmbedVar.add_field(name="**:busts_in_silhouette: Participation(s)**", value=user_react_data["total_user"], inline=True)
        updateEmbedVar.add_field(name=(":lock:" if timerExpire <= 0 else ":unlock:")+" **Etat**", value=("Fermé" if timerExpire <= 0 else "Ouvert"), inline=True)
        for reaction in user_react_data["user_react"]:
            usersLst = "\u200b"
            users = await reaction.users().flatten()
            usersLst += '\n'.join(["<@"+str(u.id)+">" for u in users if not u.bot])
            if reaction.emoji in reactions or limitReact.lower() == "non":
                updateEmbedVar.add_field(name=reaction.emoji+" **("+str(usersLst.count("\n")+1)+")**", value=usersLst, inline=True)
        updateEmbedVar.add_field(name="** **", value=footer_embed, inline=False)
        updateEmbedVar.set_footer(text="developped by R.L. / Simplon 2020 | Le sondage sera cloturé le {0}.".format(dateYMD+' à '+dateHMS[:-3]))
        return updateEmbedVar

    react_message = await ctx.send(embed=await makeEmbedPoll())
    for reaction in reactions:
        await react_message.add_reaction(reaction)
    await react_message.edit(embed=await makeEmbedPoll())

    def checkReact(reaction, user):
      return user.bot == False and (str(reaction.emoji) in reactions or limitReact.lower() == "non")

    pollOpen = True
    while pollOpen == True:
        try:
            pending_tasks = [bot.wait_for('reaction_add', timeout=timerExpire,check=checkReact), bot.wait_for('reaction_remove', timeout=timerExpire,check=checkReact)]
            done_tasks, pending_tasks = await asyncio.wait(pending_tasks, return_when=asyncio.FIRST_COMPLETED)

            for task in done_tasks:
                reaction, user = await task
                await react_message.edit(embed=await makeEmbedPoll())
        except asyncio.TimeoutError:
           await react_message.edit(embed=await makeEmbedPoll())
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

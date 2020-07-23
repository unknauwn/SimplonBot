#Discord Simplon Bot
#Author: RAPHAEL.L 06
#Language: Python

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import os
import random
#Utiliser pour les tests en local
#import nest_asyncio
#import asyncio
#from dotenv import load_dotenv
#nest_asyncio.apply()
#load_dotenv()

bot = commands.Bot(command_prefix='!')

#@bot.command(name='test')
#async def test(ctx):
    #DoSomething

##Commande du bot qui affiche l'aide(les commandes)
@bot.command(name='aide')
async def aide(ctx):
    bot_cmd = '**!roll_places** - Génère les places de chaque apprenant aléatoirement.\n**!roll_app** - Génère **UN** apprenant aléatoirement'
    embedVar = discord.Embed(title="Aide Bot Simplon:", description="Affichage des commandes pour l'utilisation du Bot Simplon", url=f"https://simplonline.co", color=0xdf0000)
    embedVar.set_author(name="Simplon'Bot", icon_url=ctx.guild.icon_url)
    embedVar.add_field(name="__Commandes:__", value=bot_cmd, inline=True)
    embedVar.set_thumbnail(url="https://simplon.co/images/logo-simplon.png")
    embedVar.set_footer(text="Simplon")
    await ctx.channel.send(embed=embedVar)
    await ctx.message.delete()

##Commande du bot qui lance la génération aléatoire des places pour chaque apprenant
@bot.command(name='roll_places')
async def random_places(ctx):
    members = list(ctx.guild.members)
    random.shuffle(members)
    embedVar = discord.Embed(title="Emplacements des Apprenants:", description="Tirage aux sort des places pour chaque apprenants", url=f"https://simplonline.co", color=0xdf0000)
    embedVar.set_author(name="Simplon'Bot", icon_url=ctx.guild.icon_url)
    embedVar.add_field(name="__Apprenants:__", value=RandomStudentsPlaces(members), inline=True)
    embedVar.set_thumbnail(url="https://simplon.co/images/logo-simplon.png")
    embedVar.set_footer(text="Simplon")
    await ctx.channel.send(embed=embedVar)
    await ctx.message.delete()

##Commande du bot qui lance la génération aléatoire d'un apprenant
@bot.command(name='roll_app')
async def random_studend(ctx):
    students = getStudents(list(ctx.guild.members))
    random_student = random.choice(students)
    student_name = random_student.name if not random_student.nick else random_student.nick
    embedVar = discord.Embed(title="Emplacements des Apprenants:", description="Tirage aux sort d'un apprenant", url=f"https://simplonline.co", color=0xdf0000)
    embedVar.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
    embedVar.add_field(name="__Apprenant Séléctionné:__", value="**"+student_name+"**", inline=True)
    embedVar.set_thumbnail(url="https://simplon.co/images/logo-simplon.png")
    embedVar.set_footer(text="Simplon Cannes DevData#1")
    await ctx.channel.send(embed=embedVar)
    await ctx.message.delete()


##Si la commande entré par l'utilisateur n'existe pas, on anticipe l'erreur
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

##Event Log de l'execution du Bot
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name="#In Code We Trust(!aide)"))

##Retourne uniquement les liste des Apprenants par leur Roles
def getStudents(students):
    students_ = []
    for student in students:
        for role in student.roles:
            if role.name in ["Admin_Test", "Apprenants"]:
                students_.append(student)
    return students_

##Retourne une liste mélangé d'apprenants trié par ordre croissant avec affichage du N°
def RandomStudentsPlaces(students):
    students = getStudents(students)
    New_Students='';
    for student in range(len(students)):
        name = students[student].name if not students[student].nick else students[student].nick
        New_Students += getEmojiByIndex(student+1)+' : **'+name+'**\n'
    return New_Students

##Retourne la position (int) avec des emoji numeric de manière dynamique
def getEmojiByIndex(index):
    Emo_Number = [":zero:", ":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:"]
    number = ''
    if index <10:
        number = Emo_Number[0]+Emo_Number[index]
    else:
        for num in map(int, str(index)):
            number += Emo_Number[num]
    return number


bot.run(os.environ['token'])

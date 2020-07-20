import nest_asyncio
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from dotenv import load_dotenv
from random import shuffle

nest_asyncio.apply()
load_dotenv()

TOKEN = 'NzM0NjY1Njc3OTM1MzQ1Njc0.XxVBWg.J1SVUphf_pyfIQ33PXyTsCb9O_Y'

bot = commands.Bot(command_prefix='!')

#@bot.command(name='test')
#async def test(ctx):
    #DoSomething


##Commande du bot qui lance la génération aléatoire
@bot.command(name='init_places')
async def random(ctx):
    members = list(ctx.guild.members)
    shuffle(members)
    embedVar = discord.Embed(title="Emplacements des Apprenants:", description="Tirage aux sorts des places pour chaque Apprenants", url=f"https://simplonline.co", color=0xdf0000)
    embedVar.set_author(name="Simplon'Bot", icon_url=ctx.guild.icon_url)
    embedVar.add_field(name="students_data", value=RandomStudent(members), inline=True)
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
    await bot.change_presence(activity=discord.Game(name="#In Code We Trust"))

##Retourne uniquement les liste des Apprenants par leur Roles
def getStudents(students):
    students_ = []
    for student in students:
        for role in student.roles:
            if role.name in ["Admin_Test", "Apprenants"]:
                students_.append(student)
    return students_

##Retourne une liste mélangé d'apprenants trié par ordre croissant avec affichage du N°
def RandomStudent(students):
    students = getStudents(students)
    New_Students='';
    Emo_Number = [":zero:", ":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:",
    ":one::one:", ":one::two:", ":one::three:", ":one::four:", ":one::five:", ":one::six:", ":one::seven:", ":one::eight:", ":one::nine:",
    ":two::one:", ":two::two:", ":two::three:", ":two::four:", ":two::five:", ":two::six:", ":two::seven:", ":two::eight", ":two::nine:", ":three::three:"]
    for student in range(len(students)):
        name = students[student].name if not students[student].nick else students[student].nick
        New_Students += Emo_Number[student]+" : "+name+'\n'
    return New_Students



bot.run(TOKEN)

#Discord Simplon Bot
#Author: RAPHAEL.L
#Fabrique: Cannes 06
#Formation: Dev Data#1
#Language: Python
#Fonctions diverses

import datetime, time

##Retourne uniquement les liste des Apprenants par leur Roles
def getStudents(students):
    students_new = []
    roleFilter = ["Admin_Test", "Apprenants"]
    for student in students:
        if (False if not [x for x in student.roles if x.name in roleFilter] else True) == True:
            students_new.append(student)
    return students_new

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

##Retourne la différence entre 2 dates en secondes
async def isDateExpired(dateS):
    datetimeFormat = '%d-%m-%Y %H:%M:%S'
    dateStart = datetime.datetime.now()
    dateEnd = dateS
    time_dif = datetime.datetime.strptime(dateEnd,datetimeFormat) - dateStart
    time_sec = int(time_dif.total_seconds())
    return time_sec

##Vérifie si la date(DD-MM-AAAA) & l'heure(HH:MM) entré par l'utilsateur sont valide
async def checkDateTime(bot, ctx, checkDate=False, checkTime=False):
    def pred(m):
        return m.author == ctx.message.author and m.channel == ctx.message.channel
    if checkDate:
        message = await ctx.send("{0}\nEntrez une Date de fin(**ex: JJ-MM-AAAA**): ".format(ctx.message.author.mention))
        msg = await bot.wait_for('message', check=pred)
        await msg.delete()
        try:
            datetime.datetime.strptime(msg.content, '%d-%m-%Y')
            await message.delete()
            return msg.content
        except ValueError:
            err = await ctx.author.send(":x: Format de date invalide, Format autorisé **ex: JJ-MM-AAAA**")
            return await checkDateTime(bot,ctx, True)
    if checkTime:
        message = await ctx.send("{0}\nEntrez une Heure de fin(**ex: HH:MM**): ".format(ctx.message.author.mention))
        msg = await bot.wait_for('message', check=pred)
        await msg.delete()
        try:
            datetime.datetime.strptime(msg.content, '%H:%M')
            await message.delete()
            return msg.content+':00'
        except ValueError:
            err = await ctx.author.send(":x: Format d'Heure invalide, Format autorisé **ex: HH:MM**")
            return await checkDateTime(bot, ctx, False, True)

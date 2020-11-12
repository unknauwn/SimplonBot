#Discord Simplon Bot
#Author: RAPHAEL.L
#Fabrique: Cannes 06
#Formation: Dev Data#1
#Language: Python
#Fonctions diverses

import datetime, time, pytz
fr = pytz.timezone('Europe/Paris')
##Retourne uniquement les liste mélangée des Apprenants par leur Rôles
def getStudents(students):
    students_new = []
    roleFilter = ["Admin_Test", "Apprenants"]
    for student in students:
        if (False if not [x for x in student.roles if x.name in roleFilter] else True) == True:
            students_new.append(student)
    return students_new

##Retourne une liste mélangée d'apprenants triée par ordre croissant avec affichage du N°
def RandomStudentsPlaces(students):
    students = getStudents(students)
    New_Students='';
    for student in range(len(students)):
        name = students[student].name if not students[student].nick else students[student].nick
        New_Students += getEmojiByIndex(student+1)+' : **'+name+'**\n'
    return New_Students

##Retourne une liste mélangée d'apprenants triée par ordre croissant avec affichage du N°
def RandomStudentsGroups(students, max_groups):
    students = getStudents(students)
    return [students[i:i + max_groups] for i in range(1, len(students), max_groups)]

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
    dateStart = datetime.datetime.now(fr).strftime(datetimeFormat)
    dateEnd = dateS
    time_dif = datetime.datetime.strptime(dateEnd,datetimeFormat) - datetime.datetime.strptime(dateStart, datetimeFormat)
    time_sec = int(time_dif.total_seconds())
    return time_sec

##Vérifie si la date(DD-MM-AAAA) & l'heure(HH:MM) entré par l'utilsateur sont valide
async def checkDateTime(bot, ctx, checkDate=False, checkTime=False):
    def pred(m):
        return m.author == ctx.message.author and m.channel == ctx.message.channel
    if checkDate:
        message = await ctx.send("{0}\n:calendar: Entrez une Date de fin(**ex: JJ-MM-AAAA**): \n**pass** *pour la date du jour par defaut*".format(ctx.message.author.mention))
        msg = await bot.wait_for('message', check=pred)
        await msg.delete()
        try:
            msg_reply = msg.content
            if msg_reply.lower() == "pass":
                msg_reply = datetime.datetime.today().strftime("%d-%m-%Y")
            datetime.datetime.strptime(msg_reply, '%d-%m-%Y')
            await message.delete()
            return msg_reply
        except ValueError:
            err = await ctx.author.send(":x: Format de date invalide, Format autorisé **ex: JJ-MM-AAAA**")
            await message.delete()
            return await checkDateTime(bot,ctx, True)
    if checkTime:
        message = await ctx.send("{0}\n:clock1: Entrez une Heure de fin(**ex: HH:MM**): \n**pass** *pour l'heure actuelle +1 par defaut*".format(ctx.message.author.mention))
        msg = await bot.wait_for('message', check=pred)
        await msg.delete()
        try:
            msg_reply = msg.content
            if msg_reply.lower() == "pass":
                msg_reply = (datetime.datetime.now(fr)+datetime.timedelta(hours=1)).strftime("%H:%M")
            datetime.datetime.strptime(msg_reply, '%H:%M')
            await message.delete()
            return msg_reply+':00'
        except ValueError:
            err = await ctx.author.send(":x: Format d'Heure invalide, Format autorisé **ex: HH:MM**")
            await message.delete()
            return await checkDateTime(bot, ctx, False, True)

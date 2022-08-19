import discord
import asyncio
import sqlite3
import os
import json

import time
import datetime
from datetime import datetime

from discord.ext import commands

###################################
###########
#
#   MADE BY RAID 
#   Raid #9074
#   discord.gg/VSD7M5t
#
###########
###################################

#------PER EFFETTUARE MODIFICHE CONTATTARE RAID------

dataeora = time.strftime("%d %b %Y")
dataeora = dataeora.upper()

#---CONFIG FETCH---
with open("../config.json") as f:
    f = json.load(f)
    

PREFIX = f.get("PREFIX")
GUILD_ID = f.get("GUILD_ID")
TOKEN = f.get("TOKEN")

BOTIMAGE = "https://cdn.discordapp.com/attachments/746084694956703775/746463724780650596/rpU7mfZ.png"
RAIDIMAGE = "https://cdn.discordapp.com/attachments/689601069025722369/745777331335069716/immagine.jpg"
DISCORDINVITE = "discord.gg/VSD7M5t"
THUMBNAIL = "https://cdn.discordapp.com/attachments/746084694956703775/746508188529983578/logbot.png"


intents = discord.Intents(messages=True, members= True, guilds=True, reactions= True)

client = commands.Bot(command_prefix=PREFIX, help_command=None, case_insensitive = 1, intents =intents)

DIRECTORY = os.path.dirname(os.path.abspath(__file__))
DIRECTORYDATABASE = DIRECTORY + "\\database\\database.db" # should be using path join :)


@client.event
async def on_ready():
    db = sqlite3.connect(f"{DIRECTORYDATABASE}")

    db.execute  ("""
    CREATE TABLE IF NOT EXISTS "Server" (
    "idstanzalog" INTEGER UNIQUE,
    "nomestanzalog" TEXT,
    "guild_id" INTEGER UNIQUE NOT NULL);""")

    # Not the best handler lmao
    try:
        db.execute(f"INSERT INTO Server (guild_id) VALUES ({GUILD_ID})")
    except:
        pass

    db.commit()
    db.close()

    activity = discord.Activity(name="users activity", type=discord.ActivityType.watching)
    await client.change_presence(status=discord.Status.do_not_disturb, activity=activity, afk=False)
    print ("Logs Bot online!")



@client.event
async def on_command_error(ctx, error):
    print (f"Something's wrong with » {ctx.command.name}")
    print (error)


@client.event
async def on_command(ctx):
    print (f"{ctx.command.name} has been invoked")


@client.event
async def on_command_completion(ctx):
    print (f"{ctx.command.name} has been invoked successfully")



@client.event
async def on_member_join(member):

    db = sqlite3.connect(f"{DIRECTORYDATABASE}")
    c = db.cursor()
    c.execute(f"SELECT idstanzalog FROM discordlog WHERE guild_id={member.guild.id};")

    try:
        for row in c.fetchall():
            idstanzalog = row[0]
                
        idstanzalogdb = client.get_channel(idstanzalog)

        if (member.bot == False):
            embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"{member.mention} è **entrato** nel server!\n\n**ID** » {member.id}\n\n**Entrato il** » {dataeora}\n**Creazione account** » {member.created_at} UTC")
            await idstanzalogdb.send(embed=embed)
        elif (member.bot == True):
            embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Il **BOT** {member.mention} è **entrato** nel server!\n\n**ID** » {member.id}\n\n**Entrato il** » {dataeora}")
            await idstanzalogdb.send(embed=embed)
        elif (member.system == True):
            embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"L'**User System**{member.mention} è **entrato** nel server!\n\n**ID** » {member.id}\n\n**Entrato il** » {dataeora}")
            await idstanzalogdb.send(embed=embed)
    except:
        embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Si è verificato un **errore** sconosciuto.")
        await idstanzalogdb.send(embed=embed)


    print(f"{member.name} è appena entrato nel server {member.guild.name}, orario UTC: {member.joined_at}, id: {member.id}")
    
    c.close()
    db.close()


@client.event
async def on_member_remove(member):

    db = sqlite3.connect(f"{DIRECTORYDATABASE}")
    c = db.cursor()
    c.execute(f"SELECT idstanzalog FROM discordlog WHERE guild_id={member.guild.id};")

    for row in c.fetchall():
        idstanzalog = row[0]
                
    idstanzalogdb = client.get_channel(idstanzalog)

    async for entry in member.guild.audit_logs(limit=1, oldest_first=False):
        action = ('{0.action}'.format(entry))
        trovakick = action.find("kick") 
        trovaban = action.find("ban")

        nomemembro = ('{0.target.mention}'.format(entry))
        idmembro = ('{0.target.id}'.format(entry))
        personachehaeffettuatoazione = ('{0.user.mention}'.format(entry))
        motivobanokick = ('{0.reason}'.format(entry))

    if (trovakick != -1):

        if (member.bot == False):
            if (motivobanokick == "None"):
                embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"{member.mention} è stato **espulso**!\n\n**Espulso da** » {personachehaeffettuatoazione}\n**Motivo** » Non specificato\n\n**Espulso il** » {dataeora}\n\n**ID Utente** » {member.id}\n")
                await idstanzalogdb.send(embed=embed)
                print(f"{member.name} è stato **espulso** dal server!\n\n**Espulso il** » {dataeora}\n**ID** » {member.id}\n")
            else:
                embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"{member.mention} è stato **espulso**!\n\n**Espulso da** » {personachehaeffettuatoazione}\n**Motivo** » {motivobanokick}\n**Espulso il** » {dataeora}\n\n**ID Utente** » {member.id}\n")
                await idstanzalogdb.send(embed=embed)
                print(f"{member.name} è stato **espulso** dal server!\n\n**Espulso il** » {dataeora}\n**ID** » {member.id}\n")
        elif (member.bot == True):
            if (motivobanokick == "None"):
                embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Il **BOT** {member.mention} è stato **espulso**!\n\n**Espulso da** » {personachehaeffettuatoazione}\n**Motivo** » Non specificato\n\n**Espulso il** » {dataeora}\n\n**ID Utente** » {member.id}\n")
                await idstanzalogdb.send(embed=embed)
                print(f"{member.name} è stato **espulso** dal server!\n\n**Espulso il** » {dataeora}\n**ID** » {member.id}\n")
            else:
                embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Il **BOT** {member.mention} è stato **espulso**!\n\n**Espulso da** » {personachehaeffettuatoazione}\n**Motivo** » {motivobanokick}\n**Espulso il** » {dataeora}\n\n**ID Utente** » {member.id}\n")
                await idstanzalogdb.send(embed=embed)
                print(f"{member.name} è stato **espulso** dal server!\n\n**Espulso il** » {dataeora}\n**ID** » {member.id}\n")
        elif (member.system == True):
            if (motivobanokick == "None"):
                embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"L'**User System**{member.mention} è stato **espulso**!\n\n**Espulso da** » {personachehaeffettuatoazione}\n**Motivo** » Non specificato\n\n**Espulso il** » {dataeora}\n\n**ID Utente** » {member.id}\n")
                await idstanzalogdb.send(embed=embed)
                print(f"{member.name} è stato **espulso** dal server!\n\n**Espulso il** » {dataeora}\n**ID** » {member.id}\n")
            else:
                embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"L'**User System**{member.mention} è stato **espulso**!\n\n**Espulso da** » {personachehaeffettuatoazione}\n**Motivo** » {motivobanokick}\n**Espulso il** » {dataeora}\n\n**ID Utente** » {member.id}\n")
                await idstanzalogdb.send(embed=embed)
                print(f"{member.name} è stato **espulso** dal server!\n\n**Espulso il** » {dataeora}\n**ID** » {member.id}\n")


    elif (trovaban != -1):

        if (member.bot == False):
            if (motivobanokick == "None"):
                embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"{member.mention} è stato **bannato**!\n\n**Bannato da** » {personachehaeffettuatoazione}\n**Motivo** » Non specificato\n\n**Bannato il** » {dataeora}\n\n**ID Utente** » {idmembro}")
                await idstanzalogdb.send(embed=embed)
                print(f"{member.name} è stato **bannato** dal server!\n\n**Bannato il** » {dataeora}\n**ID** » {member.id}\n")
            else:
                embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"{member.mention} è stato **bannato**!\n\n**Bannato da** » {personachehaeffettuatoazione}\n**Motivo** » {motivobanokick}\n\n**Bannato il** » {dataeora}\n\n**ID Utente** » {idmembro}")
                await idstanzalogdb.send(embed=embed)
                print(f"{member.name} è stato **bannato** dal server!\n\n**Bannato il** » {dataeora}\n**ID** » {member.id}\n")
        elif (member.bot == True):
            if (motivobanokick == "None"):
                embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Il **BOT** {member.mention} è stato **bannato**!\n\n**Bannato da** » {personachehaeffettuatoazione}\n**Motivo** » Non specificato\n\n**Bannato il** » {dataeora}\n\n**ID Utente** » {idmembro}")
                await idstanzalogdb.send(embed=embed)
                print(f"{member.name} è stato **espulso** dal server!\n\n**Espulso il** » {dataeora}\n**ID** » {member.id}\n")
            else:
                embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Il **BOT** {member.mention} è stato **bannato**!\n\n**Bannato da** » {personachehaeffettuatoazione}\n**Motivo** » {motivobanokick}\n\n**Bannato il** » {dataeora}\n\n**ID Utente** » {idmembro}")
                await idstanzalogdb.send(embed=embed)
                print(f"{member.name} è stato **espulso** dal server!\n\n**Espulso il** » {dataeora}\n**ID** » {member.id}\n")
        elif (member.system == True):
            if (motivobanokick == "None"):
                embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"L'**User System**{member.mention} è stato **bannato**!\n\n**Bannato da** » {personachehaeffettuatoazione}\n**Motivo** » Non specificato\n\n**Bannato il** » {dataeora}\n\n**ID Utente** » {idmembro}")
                await idstanzalogdb.send(embed=embed)
                print(f"{member.name} è stato **bannato** dal server!\n\n**Bannato il** » {dataeora}\n**ID** » {member.id}\n")
            else:
                embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"L'**User System**{member.mention} è stato **bannato**!\n\n**Bannato da** » {personachehaeffettuatoazione}\n**Motivo** » {motivobanokick}\n\n**Bannato il** » {dataeora}\n\n**ID Utente** » {idmembro}")
                await idstanzalogdb.send(embed=embed)
                print(f"{member.name} è stato **bannato** dal server!\n\n**Bannato il** » {dataeora}\n**ID** » {member.id}\n")

    else:
        if (member.bot == False):
            embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"{member.mention} è **uscito** dal server!\n\n**Uscito il** » {dataeora}\n**ID** » {member.id}\n")
            await idstanzalogdb.send(embed=embed)
            print(f"{member.name} è appena uscito dal server {member.guild.name}, uscito il: {dataeora}, ID: {member.id}")
        elif (member.bot == True):
            embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Il **BOT** {member.mention} è **uscito** dal server!\n\n**Uscito il** » {dataeora}\n**ID** » {member.id}\n")
            await idstanzalogdb.send(embed=embed)
            print(f"{member.name} è appena uscito dal server {member.guild.name}, uscito il: {dataeora}, ID: {member.id}")
        elif (member.system == True):
            embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"L'**User System**{member.mention} è **uscito** dal server!\n\n**Uscito il** » {dataeora}\n**ID** » {member.id}\n")
            await idstanzalogdb.send(embed=embed)
            print(f"{member.name} è appena uscito dal server {member.guild.name}, uscito il: {dataeora}, ID: {member.id}")

    c.close()
    db.close()


@client.event
async def on_guild_channel_create(channel):

    try:
        db = sqlite3.connect(f"{DIRECTORYDATABASE}")
        c = db.cursor()
        c.execute(f"SELECT idstanzalog FROM discordlog WHERE guild_id={channel.guild.id};")

        for row in c.fetchall():
            idstanzalog = row[0]
                    
        idstanzalogdb = client.get_channel(idstanzalog)
        
        async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create, oldest_first=False):
            creatorestanza = ('{0.user.mention}'.format(entry))
            idstanza = ('{0.target.id}'.format(entry))

        if (str(channel.type) == "text"):
            embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"E' stato **creato** un canale **__testuale__** chiamato » {channel.mention}\n\n**Creatore** » {creatorestanza}\n**Creato il** » {dataeora}\n\n**ID Canale** » {idstanza}")
            await idstanzalogdb.send(embed=embed)
        elif (str(channel.type) == "voice"):
            embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"E' stato **creato** un canale **__vocale__** chiamato » {channel}\n**Creatore** » {creatorestanza}\n**Creato il** » {dataeora}\n\n**ID Canale** » {idstanza}")
            await idstanzalogdb.send(embed=embed)
        elif (str(channel.type) == "news"):
            embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"E' stato **creato** un canale **__annunci__** chiamato » {channel.mention}**Creatore** » {creatorestanza}\n**Creato il** » {dataeora}\n\n**ID Canale** » {idstanza}")
            await idstanzalogdb.send(embed=embed)

        c.close()
        db.close()

    except:
        embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Si è verificato un **errore** sconosciuto.")
        await idstanzalogdb.send(embed=embed)
    

@client.event
async def on_guild_channel_delete(channel):

    try:
        db = sqlite3.connect(f"{DIRECTORYDATABASE}")
        c = db.cursor()
        c.execute(f"SELECT idstanzalog FROM discordlog WHERE guild_id={channel.guild.id};")

        for row in c.fetchall():
            idstanzalog = row[0]
        
        idstanzalogdb = client.get_channel(idstanzalog)

        async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete, oldest_first=False):
            eliminatorestanza = ('{0.user.mention}'.format(entry))
            nomestanzaeliminata = ('{0.before.name}'.format(entry))


        if (str(channel.type) == "text"):
            embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"E' stato **eliminato** un canale **__testuale__** chiamato » #{nomestanzaeliminata}\n\n**Eliminatore** » {eliminatorestanza}\n**Eliminato il** » {dataeora}")
            await idstanzalogdb.send(embed=embed)
        elif (str(channel.type) == "voice"):
            embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"E' stato **eliminato** un canale **__vocale__** chiamato » #{nomestanzaeliminata}\n\n**Eliminatore** » {eliminatorestanza}\n**Eliminato il** » {dataeora}")
            await idstanzalogdb.send(embed=embed)
        elif (str(channel.type) == "news"):
            embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"E' stato **eliminato** un canale **__annunci__** chiamato » #{nomestanzaeliminata}\n\n**Eliminatore** » {eliminatorestanza}\n**Eliminato il** » {dataeora}")
            await idstanzalogdb.send(embed=embed)


        c.close()
        db.close()

    except:
        embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Si è verificato un **errore** sconosciuto.")
        await idstanzalogdb.send(embed=embed)


@client.event
async def on_guild_role_create(role):

    try:

        db = sqlite3.connect(f"{DIRECTORYDATABASE}")
        c = db.cursor()
        c.execute(f"SELECT idstanzalog FROM discordlog WHERE guild_id={role.guild.id};")

        for row in c.fetchall():
            idstanzalog = row[0]
                    
        idstanzalogdb = client.get_channel(idstanzalog)

        async for entry in role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_create, oldest_first=False):
            creatoreruolo =  ('{0.user.mention}'.format(entry))
            idruolo = ('{0.target.id}'.format(entry))


        if (role.managed == True):
            embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"É stato **creato** un nuovo **ruolo**!\n\n**Creatore** » {role.name} | Integrazione\n**Creato il** » {dataeora}\n\n**ID Ruolo** » {idruolo}\n")
            await idstanzalogdb.send(embed=embed)
        else:
            embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"É stato **creato** un nuovo **ruolo**!\n\n**Creatore** » {creatoreruolo}\n**Creato il** » {dataeora}\n\n**ID Ruolo** » {idruolo}")
            await idstanzalogdb.send(embed=embed)

        c.close()
        db.close()

    except:
        embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Si è verificato un **errore** sconosciuto.")
        await idstanzalogdb.send(embed=embed)


@client.event
async def on_guild_role_delete(role):

    try:

        db = sqlite3.connect(f"{DIRECTORYDATABASE}")
        c = db.cursor()
        c.execute(f"SELECT idstanzalog FROM discordlog WHERE guild_id={role.guild.id};")

        for row in c.fetchall():
            idstanzalog = row[0]
                            
        idstanzalogdb = client.get_channel(idstanzalog)

        async for entry in role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete, oldest_first=False):
            print ('{0.user.mention} ha eliminato {0.before.name}'.format(entry))
            eliminatoreruolo =  ('{0.user.mention}'.format(entry))
            nomeruoloeliminato = ('{0.before.name}'.format(entry))

            embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"É stato **eliminato** il **ruolo** » {nomeruoloeliminato}!\n\n**Eliminatore** » {eliminatoreruolo}\n**Eliminato il** » {dataeora}")
            await idstanzalogdb.send(embed=embed)

    except:
        embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Si è verificato un **errore** sconosciuto.")
        await idstanzalogdb.send(embed=embed)
    
    c.close()
    db.close()



@client.event
async def on_guild_unavailable(guild):

    try:

        db = sqlite3.connect(f"{DIRECTORYDATABASE}")
        c = db.cursor()
        c.execute(f"SELECT idstanzalog FROM discordlog WHERE guild_id={guild.id};")

        for row in c.fetchall():
            idstanzalog = row[0]
                                
        idstanzalogdb = client.get_channel(idstanzalog)

        embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Attualmente i **servers** di **Discord** stanno avendo **problemi**.")
        await idstanzalogdb.send(embed=embed)

    except:
        embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Si è verificato un **errore** sconosciuto.")
        await idstanzalogdb.send(embed=embed)

    c.close()
    db.close()

    
@client.event
async def on_member_unban(guild, user):

    try:

        db = sqlite3.connect(f"{DIRECTORYDATABASE}")
        c = db.cursor()
        c.execute(f"SELECT idstanzalog FROM discordlog WHERE guild_id={guild.id};")

        for row in c.fetchall():
            idstanzalog = row[0]
                                
        idstanzalogdb = client.get_channel(idstanzalog)

        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.unban, oldest_first=False):
            sbannatoda = ('{0.user.mention}'.format(entry))


        embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"{user.mention} è stato **sbannato**!\n\n**Sbannato da** » {sbannatoda}\n**Sbannato il** » {dataeora}\n\n**ID Utente** » {user.id}")
        await idstanzalogdb.send(embed=embed)

    except:
        embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Si è verificato un **errore** sconosciuto.")
        await idstanzalogdb.send(embed=embed)

    c.close()
    db.close()


@client.event
async def on_invite_create(invite):

    try:
        db = sqlite3.connect(f"{DIRECTORYDATABASE}")
        c = db.cursor()
        c.execute(f"SELECT idstanzalog FROM discordlog WHERE guild_id={invite.guild.id};")

        for row in c.fetchall():
            idstanzalog = row[0]
                                
        idstanzalogdb = client.get_channel(idstanzalog)

        if (invite.max_uses == 0):
            invite.max_uses = "Nessun limite"

        if (invite.max_age == 0):
            if (invite.temporary == True):
                embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"É stato **creato** un **invito**!\n\n**Creato da** » {invite.inviter.mention}\n**Creato il** » {dataeora}\n\n**Usi Massimi** » {invite.max_uses}\n**Scadenza** » Mai\n**__Invito temporaneo__**\n\n**ID Creatore** » {invite.inviter.id}")
                await idstanzalogdb.send(embed=embed)
            else:
                embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"É stato **creato** un **invito**!\n\n**Creato da** » {invite.inviter.mention}\n**Creato il** » {dataeora}\n\n**Usi Massimi** » {invite.max_uses}\n**Scadenza** » Mai\n\n**ID Utente** » {invite.inviter.id}")
                await idstanzalogdb.send(embed=embed)
        elif (invite.max_age != 0):
            if (invite.temporary == True):
                embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"É stato **creato** un **invito**!\n\n**Creato da** » {invite.inviter.mention}\n**Creato il** » {dataeora}\n\n**Usi Massimi** » {invite.max_uses}\n**Scadenza** » {invite.max_age // 60} (*s*)\n**__Invito temporaneo__**\n\n**ID Utente** » {invite.inviter.id}")
                await idstanzalogdb.send(embed=embed)
            else:
                if (invite.max_age == 1800):
                    embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"É stato **creato** un **invito**!\n\n**Creato da** » {invite.inviter.mention}\n**Creato il** » {dataeora}\n\n**Usi Massimi** » {invite.max_uses}\n**Scadenza** » 30 minuti\n\n**ID Utente** » {invite.inviter.id}")
                    await idstanzalogdb.send(embed=embed)
                elif (invite.max_age == 3600):
                    embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"É stato **creato** un **invito**!\n\n**Creato da** » {invite.inviter.mention}\n**Creato il** » {dataeora}\n\n**Usi Massimi** » {invite.max_uses}\n**Scadenza** » 1 ora\n\n**ID Utente** » {invite.inviter.id}")
                    await idstanzalogdb.send(embed=embed)
                elif(invite.max_age == 21600):
                    embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"É stato **creato** un **invito**!\n\n**Creato da** » {invite.inviter.mention}\n**Creato il** » {dataeora}\n\n**Usi Massimi** » {invite.max_uses}\n**Scadenza** » 6 ore\n\n**ID Utente** » {invite.inviter.id}")
                    await idstanzalogdb.send(embed=embed)
                elif (invite.max_age == 43200):
                    embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"É stato **creato** un **invito**!\n\n**Creato da** » {invite.inviter.mention}\n**Creato il** » {dataeora}\n\n**Usi Massimi** » {invite.max_uses}\n**Scadenza** » 12 ore\n\n**ID Utente** » {invite.inviter.id}")
                    await idstanzalogdb.send(embed=embed)
                elif (invite.max_age == 86400):
                    embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"É stato **creato** un **invito**!\n\n**Creato da** » {invite.inviter.mention}\n**Creato il** » {dataeora}\n\n**Usi Massimi** » {invite.max_uses}\n**Scadenza** » 1 giorno\n\n**ID Utente** » {invite.inviter.id}")
                    await idstanzalogdb.send(embed=embed)

    except:
        embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Si è verificato un **errore** sconosciuto.")
        await idstanzalogdb.send(embed=embed)

    c.close()
    db.close()


@client.event
async def on_invite_delete(invite):

    try:

        db = sqlite3.connect(f"{DIRECTORYDATABASE}")
        c = db.cursor()
        c.execute(f"SELECT idstanzalog FROM discordlog WHERE guild_id={invite.guild.id};")

        for row in c.fetchall():
            idstanzalog = row[0]
                                    
        idstanzalogdb = client.get_channel(idstanzalog)

        async for entry in invite.guild.audit_logs(limit=1, action=discord.AuditLogAction.invite_delete, oldest_first=False):
            eliminatoreinvito =  ('{0.user.mention}'.format(entry))


        embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"É stato **eliminato** un **invito**!\n\n**Eliminato da** » {eliminatoreinvito}\n**Eliminato il** » {dataeora}")
        await idstanzalogdb.send(embed=embed)

    except:
        embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Si è verificato un **errore** sconosciuto.")
        await idstanzalogdb.send(embed=embed)

    c.close()
    db.close()


@client.event
async def on_guild_role_update(before: discord.Role, after: discord.Role):



    db = sqlite3.connect(f"{DIRECTORYDATABASE}")
    c = db.cursor()
    c.execute(f"SELECT idstanzalog FROM discordlog WHERE guild_id={before.guild.id};")

    for row in c.fetchall():
        idstanzalog = row[0]
                                    
    idstanzalogdb = client.get_channel(idstanzalog)

    async for entry in before.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_update, oldest_first=False):
        modificatoreruolo = ('{0.user.mention}'.format(entry))


    cambiamenti = []
    separatore = "\n"

    if (before.name != after.name):
        cambiamenti.append(f"• Ha cambiato il nome da **{before.name}** a **{after.name}**")
        cambionomeavvenuto = True
    else:
        cambionomeavvenuto = False

    if (before.mentionable != after.mentionable):
        if (after.mentionable == True):
            cambiamenti.append(f"• Menzionabile")
        else:
            cambiamenti.append(f"• Non menzionabile")

    #hoist
    if (before.hoist != after.hoist):
        if (after.hoist == True):
            cambiamenti.append(f"• Separato dagli altri ruoli")
        else:
            cambiamenti.append(f"• Non separato dagli altri ruoli")

    #position
    if (before.position != after.position):
        cambiamenti.append(f"• Posizione cambiata da **{before.position}** a **{after.position}**")
    
    #managed
    if (before.managed != after.managed):
        if (after.managed == True):
            cambiamenti.append(f"• Gestito da un'integrazione")
        else:
            cambiamenti.append(f"• Non gestito da un'integrazione")

    #color
    if (before.color != after.color):
        cambiamenti.append(f"• Colore cambiato da **{before.color.value}** a **{after.color.value}**")

    #administrator
    if (before.permissions.administrator != after.permissions.administrator):
        if (after.permissions.administrator == True):
            cambiamenti.append(f"• Tutti i permessi (*Amministratore*)")
        else:
            cambiamenti.append(f"• Non ha tutti i permessi (*Amministratore*)")

    #kick_members
    if (before.permissions.kick_members != after.permissions.kick_members):
        if (after.permissions.kick_members == True):
            cambiamenti.append(f"• Può espellere i membri")
        else:
            cambiamenti.append(f"• Non può espellere i membri")

    #ban_members
    if (before.permissions.ban_members != after.permissions.ban_members):
        if (after.permissions.ban_members == True):
            cambiamenti.append(f"• Può bannare i membri")
        else:
            cambiamenti.append(f"• Non può bannare i membri")

    #manage_channels
    if (before.permissions.manage_channels != after.permissions.manage_channels):
        if (after.permissions.manage_channels == True):
            cambiamenti.append(f"• Gestisce i canali")
        else:
            cambiamenti.append(f"• Non gestisce i canali")

    #manage_guild
    if (before.permissions.manage_guild != after.permissions.manage_guild):
        if (after.permissions.manage_guild == True):
            cambiamenti.append(f"• Gestisce il server")
        else:
            cambiamenti.append(f"• Non gestisce il server")

    #manage_messages
    if (before.permissions.manage_messages != after.permissions.manage_messages):
        if (after.permissions.manage_messages == True):
            cambiamenti.append(f"• Gestisce i messaggi")
        else:
            cambiamenti.append(f"• Non gestisce i messaggi")

    #manage_roles
    if (before.permissions.manage_roles != after.permissions.manage_roles):
        if (after.permissions.manage_roles == True):
            cambiamenti.append(f"• Gestisce i ruoli")
        else:
            cambiamenti.append(f"• Non gestisce i ruoli")

    #manage_nicknames
    if (before.permissions.manage_nicknames != after.permissions.manage_nicknames):
        if (after.permissions.manage_nicknames == True):
            cambiamenti.append(f"• Gestisce i soprannomi")
        else:
            cambiamenti.append(f"• Non gestisce i soprannomi")

    #manage_webhooks
    if (before.permissions.manage_webhooks != after.permissions.manage_webhooks):
        if (after.permissions.manage_webhooks == True):
            cambiamenti.append(f"• Gestisce i Webhooks")
        else:
            cambiamenti.append(f"• Non gestisce i Webhooks")

    #manage_emojis
    if (before.permissions.manage_emojis != after.permissions.manage_emojis):
        if (after.permissions.manage_emojis == True):
            cambiamenti.append(f"• Gestisce gli emoji")
        else:
            cambiamenti.append(f"• Non gestisce gli emoji")

    #mute_members
    if (before.permissions.mute_members != after.permissions.mute_members):
        if (after.permissions.mute_members == True):
            cambiamenti.append(f"• Può silenziare gli utenti")
        else:
            cambiamenti.append(f"• Non può silenziare gli utenti")

    #deafen_members
    if (before.permissions.deafen_members != after.permissions.deafen_members):
        if (after.permissions.deafen_members == True):
            cambiamenti.append(f"• Può silenziare l'audio degli utenti")
        else:
            cambiamenti.append(f"• Non può silenziare l'audio degli utenti")

    #move_members
    if (before.permissions.move_members != after.permissions.move_members):
        if (after.permissions.move_members == True):
            cambiamenti.append(f"• Può spostare gli utenti")
        else:
            cambiamenti.append(f"• Non può spostare gli utenti")

    #hoist (registro attività)
    if (before.permissions.view_audit_log != after.permissions.view_audit_log):
        if (after.permissions.view_audit_log == True):
            cambiamenti.append(f"• Può visualizzare il registro attività")
        else:
            cambiamenti.append(f"• Non può visualizzare il registro attività")

    #add_reactions
    if (before.permissions.add_reactions != after.permissions.add_reactions):
        if (after.permissions.add_reactions == True):
            cambiamenti.append(f"• Può aggiungere reazioni")
        else:
            cambiamenti.append(f"• Non può aggiungere reazioni")

    #priority_speaker
    if (before.permissions.priority_speaker != after.permissions.priority_speaker):
        if (after.permissions.priority_speaker == True):
            cambiamenti.append(f"• Priorità di parola")
        else:
            cambiamenti.append(f"• Non ha la priorità di parola")

    #send_tts_messages
    if (before.permissions.send_tts_messages != after.permissions.send_tts_messages):
        if (after.permissions.send_tts_messages == True):
            cambiamenti.append(f"• Può usare la sintesi vocale")
        else:
            cambiamenti.append(f"• Non può usare la sintesi vocale")
  
    #view_guild_insights
    if (before.permissions.view_guild_insights != after.permissions.view_guild_insights):
        if (after.permissions.view_guild_insights == True):
            cambiamenti.append(f"• Può vedere l'attività del server (*insights*)")
        else:
            cambiamenti.append(f"• Non può vedere l'attivita del server (*insights*)")

    #attach_files (allegare i file)
    if (before.permissions.attach_files != after.permissions.attach_files):
        if (after.permissions.attach_files == True):
            cambiamenti.append(f"• Può allegare i file")
        else:
            cambiamenti.append(f"• Non può allegare i file")

    #embed_links (Incorporare i link)
    if (before.permissions.embed_links != after.permissions.embed_links):
        if (after.permissions.embed_links == True):
            cambiamenti.append(f"• Può incorporare i link")
        else:
            cambiamenti.append(f"• Non può incorporare i link")

    #read_message_history (leggere la cronologia dei messaggi)
    if (before.permissions.read_message_history != after.permissions.read_message_history):
        if (after.permissions.read_message_history == True):
            cambiamenti.append(f"• Può leggere la cronologia dei messaggi")
        else:
            cambiamenti.append(f"• Non può leggere la cronologia dei messaggi")

    #read_messages (can read messages from all or specific text channels)
    if (before.permissions.read_messages != after.permissions.read_messages):
        if (after.permissions.read_messages == True):
            cambiamenti.append(f"• Può leggere i messaggi di uno o più canali")
        else:
            cambiamenti.append(f"• Non può leggere i messaggi di uno o più canali")

    #mention_everyone
    if (before.permissions.mention_everyone != after.permissions.mention_everyone):
        if (after.permissions.mention_everyone == True):
            cambiamenti.append(f"• Può menzionare tutti")
        else:
            cambiamenti.append(f"• Non può menzionare tutti")

    #external_emojis
    if (before.permissions.external_emojis != after.permissions.external_emojis):
        if (after.permissions.external_emojis == True):
            cambiamenti.append(f"• Può usare emjoi esterni")
        else:
            cambiamenti.append(f"• Non può usare emoji esterni")

    #connect
    if (before.permissions.connect != after.permissions.connect):
        if (after.permissions.connect == True):
            cambiamenti.append(f"• Può connettersi ai canali vocali")
        else:
            cambiamenti.append(f"• Non può connettersi ai canali vocali")

    #speak
    if (before.permissions.speak != after.permissions.speak):
        if (after.permissions.speak == True):
            cambiamenti.append(f"• Può parlare nei canali vocali")
        else:
            cambiamenti.append(f"• Non può parlare nei canali vocali")

    #use_voice_activation
    if (before.permissions.use_voice_activation != after.permissions.use_voice_activation):
        if (after.permissions.use_voice_activation == True):
            cambiamenti.append(f"• Può usare l'attivazione vocale")
        else:
            cambiamenti.append(f"• Non può usare l'attivazione vocale")

    #change_nickname
    if (before.permissions.change_nickname != after.permissions.change_nickname):
        if (after.permissions.change_nickname == True):
            cambiamenti.append(f"• Può cambiare il proprio nickname")
        else:
            cambiamenti.append(f"• Non può cambiare il proprio nickname")

    #create_instant_invite
    if (before.permissions.create_instant_invite != after.permissions.create_instant_invite):
        if (after.permissions.create_instant_invite == True):
            cambiamenti.append(f"• Può creare inviti")
        else:
            cambiamenti.append(f"• Non può creare inviti")

    #stream
    if (before.permissions.stream != after.permissions.stream):
        if (after.permissions.stream == True):
            cambiamenti.append(f"• Può trasmettere")
        else:
            cambiamenti.append(f"• Non può trasmettere")

    #send_messages
    if (before.permissions.send_messages != after.permissions.send_messages):
        if (after.permissions.send_messages == True):
            cambiamenti.append(f"• Può inviare messaggi")
        else:
            cambiamenti.append(f"• Non può inviare messaggi")

    if (cambionomeavvenuto == False):
        embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"É stato **modificato** un **ruolo**!\n\n**Nome ruolo** » {after.mention}\n\n**Modificato da** » {modificatoreruolo}\n**Modificato il** » {dataeora}\n**Numero modifiche** » {len(cambiamenti)}\n\n{separatore.join(cambiamenti)}")
        await idstanzalogdb.send(embed=embed)
    else:
        embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"É stato **modificato** un **ruolo**!\n\n**Modificato da** » {modificatoreruolo}\n**Modificato il** » {dataeora}\n**Numero modifiche** » {len(cambiamenti)}\n\n{separatore.join(cambiamenti)}")
        await idstanzalogdb.send(embed=embed)

    c.close()
    db.close()

def prova(guild: discord.Guild):
    db = sqlite3.connect(f"{DIRECTORYDATABASE}")
    c = db.cursor()
    c.execute(f"SELECT idstanzalog FROM discordlog WHERE guild_id={guild};")

    for row in c.fetchall():
        dato = row[0]

    prova = client.get_channel(dato)
    return prova

    c.close()
    db.close()


@client.event
async def on_guild_update(before: discord.Guild, after: discord.Guild):

    db = sqlite3.connect(f"{DIRECTORYDATABASE}")
    c = db.cursor()
    c.execute(f"SELECT idstanzalog FROM discordlog WHERE guild_id={before.id};")

    for row in c.fetchall():
        idstanzalog = row[0]

    idstanzalogdb = client.get_channel(idstanzalog)


    async for entry in before.audit_logs(limit=1, action=discord.AuditLogAction.guild_update, oldest_first=False):
        modificatore = ('{0.user.mention}'.format(entry))

    cambiamenti = []
    separatore = "\n"

    if (before.name != after.name):
        cambiamenti.append(f"• Ha cambiato il nome da **{before.name}** a **{after.name}**")

    if (before.region != after.region):
        #Traduzione ita regione precedente
        if (str(before.region) == "eu_central"):
            before.region = "Europa centrale"
        elif (str(before.region) == "eu_west"):
            before.region = "Europa Ovest"
        elif (str(before.region) == "europe"):
            before.region = "Europa"
        elif (str(before.region) == "us_central"):
            before.region = "Stati Uniti"
        elif (str(before.region) == "us_west"):
            before.region = "Stati Uniti Ovest"
        elif (str(before.region) == "us_east"):
            before.region = "Stati Uniti Est"
        elif (str(before.region) == "us_south"):
            before.region = "Stati Uniti Sud"
        elif (str(before.region) == "hongkong"):
            before.region = "Hong Kong"
        elif (str(before.region) == "india"):
            before.region = "India"
        elif (str(before.region) == "japan"):
            before.region = "Giappone"
        elif (str(before.region) == "russia"):
            before.region = "Russia"
        elif (str(before.region) == "singapore"):
            before.region = "Singapore"
        elif (str(before.region) == "southafrica"):
            before.region = "SudAfrica"
        elif (str(before.region) == "south_korea"):
            before.region = "Corea del Sud"
        elif (str(before.region) == "sydney"):
            before.region = "Sydney"
        elif (str(before.region) == "brazil"):
            before.region = "Brasile"
        elif (str(before.region) == "london"):
            before.region = "Londra"
           
        #Traduzione ita nuova regione scelta
        if (str(after.region) == "eu_central"):
            after.region = "Europa centrale"
        elif (str(after.region) == "eu_west"):
            after.region = "Europa Ovest"
        elif (str(after.region) == "europe"):
            after.region = "Europa"
        elif (str(after.region) == "us_central"):
            after.region = "Stati Uniti"
        elif (str(after.region) == "us_west"):
            after.region = "Stati Uniti Ovest"
        elif (str(after.region) == "us_east"):
            after.region = "Stati Uniti Est"
        elif (str(after.region) == "us_south"):
            after.region = "Stati Uniti Sud"
        elif (str(after.region) == "hongkong"):
            after.region = "Hong Kong"
        elif (str(after.region) == "india"):
            after.region = "India"
        elif (str(after.region) == "japan"):
            after.region = "Giappone"
        elif (str(after.region) == "russia"):
            after.region = "Russia"
        elif (str(after.region) == "singapore"):
            after.region = "Singapore"
        elif (str(after.region) == "southafrica"):
            after.region = "SudAfrica"
        elif (str(after.region) == "south_korea"):
            after.region = "Corea del Sud"
        elif (str(after.region) == "sydney"):
            after.region = "Sydney"
        elif (str(after.region) == "brazil"):
            after.region = "Brasile"
        elif (str(after.region) == "london"):
            after.region = "Londra"
        cambiamenti.append(f"• Ha cambiato la regione da **{before.region}** a **{after.region}**")

    if (before.emojis != after.emojis):
        cambiamenti.append(f"• Emoji aggiornati")
    
    if (before.afk_timeout != after.afk_timeout):
        cambiamenti.append(f"• Ha cambiato il timeout __AFK__ da **{before.afk_timeout//60}** a **{after.afk_timeout//60}** (minuti)")

    if (before.afk_channel != after.afk_channel):
        if (before.afk_channel == None):
            cambiamenti.append(f"• Ha cambiato il canale AFK da **Nessuno** a @**{after.afk_channel}**")
        elif (after.afk_channel == None):
            cambiamenti.append(f"• Ha cambiato il canale AFK da @**{before.afk_channel}** a **Nessuno**")
        else:
            cambiamenti.append(f"• Ha cambiato il canale AFK da @**{before.afk_channel}** a @**{after.afk_channel}**")


    if (before.icon != after.icon):
        cambiamenti.append(f"• Ha cambiato l'icona")


    if (before.owner_id != after.owner_id):
        cambiamenti.append(f"• Owner server cambiato da {before.owner.mention} a {after.owner.mention}")


    if (before.max_presences != after.max_presences):
        cambiamenti.append(f"• Massimo presenze cambiato da {before.max_presences} a {after.max_presences}")


    if (before.banner != after.banner):
        cambiamenti.append(f"• Banner aggiornato")

    if (before.description != after.description):
        cambiamenti.append(f"• Descrizione aggiornata")

    if (int(before.mfa_level) != int(after.mfa_level)):
        if (int(after.mfa_level) == 1):
            cambiamenti.append(f"• Autenticazione a __2__ __fattori__ attivata")
        else:
            cambiamenti.append(f"• Autenticazione a __2__ __fattori__ disattivata")

    if (before.verification_level != after.verification_level):
        #Traduzione ita before.verifcation_level
        if (str(before.verification_level) == "none"):
            beforeverification_level = "Nessuno"
        elif (str(before.verification_level) == "low"):
            beforeverification_level = "Basso"
        elif (str(before.verification_level) == "medium"):
            beforeverification_level = "Medio"
        elif (str(before.verification_level) == "high"):
            beforeverification_level = "Alto"
        elif (str(before.verification_level) == "extreme"):
            beforeverification_level = "Massimo"
        #Traduzione ita after.verifcation_level
        if (str(after.verification_level) == "none"):
            afterverification_level = "Nessuno"
        elif (str(after.verification_level) == "low"):
            afterverification_level = "Basso"
        elif (str(after.verification_level) == "medium"):
            afterverification_level = "Medio"
        elif (str(after.verification_level) == "high"):
            afterverification_level = "Alto"
        elif (str(after.verification_level) == "extreme"):
            afterverification_level = "Massimo"
        cambiamenti.append(f"• Livello di verifica cambiato da **{beforeverification_level}** a **{afterverification_level}**")
    
    #C'è un problema, leggi il txt
    if (before.explicit_content_filter != after.explicit_content_filter):
        if (str(after.explicit_content_filter) == "disabled"):
            afterexplicit_content_filter = "Non controllare i contenuti"
        elif (str(after.explicit_content_filter) == "no_role"):
            afterexplicit_content_filter = "Controlla i contenuti dei membri senza un ruolo"
        elif (str(after.explicit_content_filter) == "all_members"):
            afterexplicit_content_filter = "Controlla i contenuti di tutti i membri"
        cambiamenti.append(f'• Filtro contenuti cambiato in **»** "**{afterexplicit_content_filter}**"')

    if (before.max_video_channel_users != after.max_video_channel_users):
        cambiamenti.append(f"• Massimo di membri in un canale video cambiato da {before.max_video_channel_users} a **{after.max_video_channel_users}**")

    if (before.default_notifications != after.default_notifications):
        if (str(after.default_notifications) == "NotificationLevel.all_messages"):
            afterdefault_notifications = "Tutti i messaggi"
        elif (str(after.default_notifications) == "NotificationLevel.only_mentions"):
            afterdefault_notifications = "Solo @menzioni"
        cambiamenti.append(f"• Notifiche cambiate in » **{afterdefault_notifications}**")


    if (('VANITY_URL' in before.features) != ('VANITY_URL' in after.features)):
        cambiamenti.append(f"• Vanity URL cambiato")
        

    if (('ANIMATED_ICON' in before.features) != ('ANIMATED_ICON' in after.features)):
        cambiamenti.append(f"• Icona animata cambiata")

    if (before.splash != after.splash):
        cambiamenti.append(f"• Invito splash cambiato")

    if (before.premium_tier != after.premium_tier):
        cambiamenti.append(f"• Tier premium cambiato da **{before.premium_tier}** a **{after.premium_tier}**")

    if (before.premium_subscription_count != after.premium_subscription_count):
        cambiamenti.append(f"• Numero di Nitro Boost cambiato in **{after.premium_subscription_count}**")

    if (before.preferred_locale != after.preferred_locale):
        cambiamenti.append(f"• Lingua preferita cambiata da **{before.preferred_locale}** a **{after.preferred_locale}**")

    if (before.discovery_splash != after.discovery_splash):
        cambiamenti.append(f"• Discovery Splash aggiornata")

    if (before.categories != after.categories):
        cambiamenti.append(f"• Categoria aggiornata")

    if (before.system_channel != after.system_channel):
        if (before.system_channel == None):
            cambiamenti.append(f"• Canale messaggi di sistema cambiato da **Nessuno** a {after.system_channel.mention}")
        elif (after.system_channel == None):
            cambiamenti.append(f"• Canale messaggi di sistema cambiato da **{before.system_channel.mention}** a **Nessuno**")
        else:
            cambiamenti.append(f"• Canale messaggi di sistema cambiato da **{before.system_channel.mention}** a {after.system_channel.mention}")

    if (before.system_channel_flags != after.system_channel_flags):
        if (before.system_channel_flags.join_notifications != after.system_channel_flags.join_notifications):
            if (after.system_channel_flags.join_notifications == True):
                cambiamenti.append(f"• Invia un messaggio di benvenuto quando qualcuno si **unisce** al server")
            else:
                cambiamenti.append(f"• Non inviare un messaggio di benvenuto quando qualcuno si **unisce** al server")
        if (before.system_channel_flags.premium_subscriptions != after.system_channel_flags.premium_subscriptions):
            if (after.system_channel_flags.premium_subscriptions == True):
                cambiamenti.append(f"• Invia un messaggio quando qualcuno **potenzia** il server")
            else:
                 cambiamenti.append(f"• Non inviare un messaggio quando qualcuno **potenzia** il server")


    if (before.rules_channel != after.rules_channel):
        if (before.rules_channel == None):
            cambiamenti.append(f"• Canale regolamento cambiato da **Nessuno** a {after.rules_channel.mention}")
        elif (after.rules_channel == None):
            cambiamenti.append(f"• Canale regolamento cambiato da {before.rules_channel.mention} a **Nessuno**")
        else:
            cambiamenti.append(f"• Canale regolamento cambiato da {before.rules_channel.mention} a {after.rules_channel.mention}")


    if (before.public_updates_channel != after.public_updates_channel):
        if (before.public_updates_channel == None):
            cambiamenti.append(f"• Canale aggiornamenti da Discord cambiato da **Nessuno** a {after.public_updates_channel.mention}")
        elif (after.public_updates_channel == None):
            cambiamenti.append(f"• Canale aggiornamenti da Discord cambiato da {before.public_updates_channel.mention} a **Nessuno**")
        else:
            cambiamenti.append(f"• Canale aggiornamenti da Discord cambiato da {before.public_updates_channel.mention} a {after.public_updates_channel.mention}")


    if (before.emoji_limit != after.emoji_limit):
        cambiamenti.append(f"• Limite emoji cambiato da {before.emoji_limit} a {after.emoji_limit}")

    if (before.bitrate_limit != after.bitrate_limit):
        cambiamenti.append(f"• Limite bitrate cambiato da {before.bitrate_limit} a {after.bitrate_limit}")

    if (before.filesize_limit != after.filesize_limit):
        cambiamenti.append(f"• Limite grandezza file cambiato da {before.filesize_limit} a {after.filesize_limit}")

    if (before.member_count != after.member_count):
        cambiamenti.append(f"• Numero membri » **{after.member_count}**")

    if (len(cambiamenti) != 0):
        embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"É stato **modificato** il **server**!\n\n**Modificato da** » {modificatore}\n**Modificato il** » {dataeora}\n**Modifiche apportate** » {len(cambiamenti)}\n\n{separatore.join(cambiamenti)}")
        await idstanzalogdb.send(embed=embed)

    c.close()
    db.close()

@client.event
async def on_voice_state_update(member, before, after):

    db = sqlite3.connect(f"{DIRECTORYDATABASE}")
    c = db.cursor()
    c.execute(f"SELECT idstanzalog FROM discordlog WHERE guild_id={member.guild.id};")

    for row in c.fetchall():
        idstanzalog = row[0]

    idstanzalogdb = client.get_channel(idstanzalog)

    if (before.mute != after.mute):
        await idstanzalogdb.send(f"{member.mention} è stato mutato da uno staffer!")

 






















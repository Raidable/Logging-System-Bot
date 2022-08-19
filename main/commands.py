import discord
import asyncio
import random
import sqlite3


from events import client, PREFIX, RAIDIMAGE, BOTIMAGE, THUMBNAIL, DISCORDINVITE, DIRECTORYDATABASE, GUILD_ID
from discord.ext import commands



    
#Comando ping
@client.command(enabled=1)
async def ping(ctx):
    embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"**Ping Log** » ``{round(client.latency * 1000)}ms``")
    await ctx.send(embed=embed)


#Comando prefix
@client.command(aliases=['prefisso'], enabled=1)
async def prefix(ctx):
    embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"**Il prefisso di Log è** » ``{PREFIX}``")
    await ctx.send(embed=embed)

@client.command(enabled=1)
async def setup(ctx):
    embed = discord.Embed(title=f"**⚙️⠀ Setup LogBot ⠀🤖**\n", colour=discord.Colour(0xD40D29), description=f"\n```» Come imposto la stanza in cui arriveranno tutti i logs?```\n**➔**⠀{PREFIX}impostacanale **#canale**\n⠀")
    embed.set_thumbnail(url=f"{THUMBNAIL}")
    embed.set_footer(text=f"Made by Raid » {DISCORDINVITE} ", icon_url=f"{RAIDIMAGE}")
    
    await ctx.send(embed=embed) 




@client.command(enabled=1, aliases= ['setchannel', 'sc'])
@commands.has_permissions(manage_guild=True)
async def impostacanale(ctx, stanza: discord.TextChannel):

    db = sqlite3.connect(f"{DIRECTORYDATABASE}")
    c = db.cursor()
    c.execute(f"SELECT id_stanza_risultati FROM Server WHERE guild_id={GUILD_ID}")

    for row in c.fetchall():
        id_stanza_log_nel_db = row[0]

    try:
        if (id_stanza_log_nel_db == stanza.id):
            embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"> Quel canale è gia **impostato**!")
            await ctx.send(embed=embed)
        elif (id_stanza_log_nel_db != stanza.id and ctx.guild.id == 476499098841776128): 
            db.execute(f"UPDATE Server SET nome_stanza_risultati='{stanza}', id_stanza_risultati={stanza.id};")
            db.commit()
            embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"> Canale **Logs** impostato **correttamente**!\n> Canale scelto **»** {stanza.mention}")
            await ctx.send(embed=embed)

        c.close()
        db.close()
    except:
        embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Si è verificato un **errore**, assicurati di aver eseguito il comando **correttamente**!")
        await ctx.send(embed=embed)
    

@client.command(enabled=1) 
@commands.has_permissions(manage_guild=True)
async def cambiacanale(ctx, vecchiastanza: discord.TextChannel, nuovastanza: discord.TextChannel):
    idvecchiastanzadapulire = (f"{vecchiastanza.mention}")
    idnuovastanzadapulire = (f"{nuovastanza.mention}")

    puliziavecchioid = idvecchiastanzadapulire.replace('<', "")
    puliziavecchioid2 = puliziavecchioid.replace('>', "")
    vecchioidpulito = puliziavecchioid2.replace('#', "")   #ID VECCHIO PULITO

    pulizianuovoid = idnuovastanzadapulire.replace('<', "")
    pulizianuovoid2 = pulizianuovoid.replace('>', "")
    nuovoidpulito = pulizianuovoid2.replace('#', "") #ID NUOVO PULITO

    db = sqlite3.connect(f"{DIRECTORYDATABASE}")

    #Fetch dell'id della stanza in cui vengono inviati i logs (da database)
    c = db.cursor()
    c.execute(f"SELECT idstanzalog FROM discordlog WHERE guild_id={ctx.guild.id}")

    for row in c.fetchall():
        idstanzalogdb = row[0]

    try:
        if (str(idstanzalogdb) == vecchioidpulito):
            db.execute(f"UPDATE discordlog SET idstanzalog={nuovoidpulito} WHERE idstanzalog={vecchioidpulito} AND guild_id={ctx.guild.id}")
            db.execute(f"UPDATE discordlog SET nomestanzalog='{nuovastanza}' WHERE nomestanzalog='{vecchiastanza}' AND guild_id={ctx.guild.id}")
            db.commit()
            embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Canale **Log** cambiato **correttamente**!")
            await ctx.send(embed=embed)
            c.close()
            db.close()
        elif (str(idstanzalogdb) != vecchioidpulito):
            embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Il primo canale menzionato **deve** essere il canale dei **logs**!")
            await ctx.send(embed=embed)
    except sqlite3.IntegrityError:
            embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Si è verificato un **errore**, assicurati di aver eseguito il comando **correttamente**!")
            await ctx.send(embed=embed)
    except sqlite3.OperationalError:
            embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Si è verificato un **errore**, ricorda di **taggare** in modo corretto i canali dei **log**!")
            await ctx.send(embed=embed)
    except UnboundLocalError:
        embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Attualmente **non** è impostato un canale per i **logs**.")
        await ctx.send(embed=embed)
    except:
        embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Si è verificato un **errore**, assicurati di aver eseguito il comando **correttamente**!")
        await ctx.send(embed=embed)


@client.command()
async def canalelogs(ctx):
    try:
        db = sqlite3.connect(f"{DIRECTORYDATABASE}")

        #Estrazione dell'id della stanza in cui vengono inviati i logs (da database)
        c = db.cursor()
        c.execute(f"SELECT idstanzalog FROM discordlog WHERE guild_id={ctx.guild.id};")

        for row in c.fetchall():
            idstanzalog = row[0]
                
        menzioneidstanzalog = client.get_channel(idstanzalog)
        
        if (idstanzalog == None):
            embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Attualmente **non** è impostato un canale per i **logs**.")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"L'attuale canale dei **logs** è **»** {menzioneidstanzalog.mention}")
            await ctx.send(embed=embed)

    except UnboundLocalError:
        embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Attualmente **non** è impostato un canale per i **logs**.")
        await ctx.send(embed=embed)
    except sqlite3.OperationalError:
        embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Attualmente **non** è impostato un canale per i **logs**.")
        await ctx.send(embed=embed)
    except:
        embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Si è verificato un **errore**.")
        await ctx.send(embed=embed)

    c.close()
    db.close()


@client.command()
@commands.has_permissions(manage_guild=True)
async def reset (ctx, arg=None):
    if (arg == "all"):
        db = sqlite3.connect(f"{DIRECTORYDATABASE}")
        db.execute(f"DELETE FROM discordlog WHERE guild_id={ctx.guild.id};")
        db.commit()
        db.close()
        embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Reset di LogsBot avvenuto con **successo**!")
        await ctx.send(embed=embed)
    elif (arg==None):
        embed = discord.Embed(title=f"**⚠️⠀ Reset LogsBot ⠀🤖**\n", colour=discord.Colour(0xD40D29), description=f"```» Sei sicuro di voler resettare LogsBot?```\n**➔**⠀  {PREFIX}reset **all**\n⠀")
        embed.set_thumbnail(url=f"{THUMBNAIL}")
        embed.set_footer(text=f"Made by Raid » {DISCORDINVITE} ", icon_url=f"{RAIDIMAGE}")
        await ctx.send(embed=embed) 
    else:
        embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Comando **reset** eseguito in modo **scorretto**!")
        await ctx.send(embed=embed)




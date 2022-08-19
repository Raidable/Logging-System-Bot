import discord

from commands import *
from events import PREFIX



@impostacanale.error
async def impostacanale_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Non disponi dei **permessi** per eseguire questo comando!")
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f'**Il comando deve essere eseguito in questo modo**:\n\n**➔**⠀ ⠀{PREFIX}impostacanale **#canalelog**')
        await ctx.send(embed=embed)
    elif isinstance(error, commands.ArgumentParsingError):
        embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Hai sbagliato a **menzionare** il canale, **esegui** il comando in questo modo:\n\n**➔** ⠀ {PREFIX}impostacanale **#canale**")
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Hai sbagliato a **menzionare** il canale, **esegui** il comando in questo modo:\n\n**➔** ⠀ {PREFIX}impostacanale **#canale**")
        await ctx.send(embed=embed)


@cambiacanale.error
async def cambiacanale_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f'**Il comando deve essere eseguito in questo modo**:\n\n**➔**⠀ ⠀{PREFIX}cambiacanale **#vecchiocanale** **#nuovocanale**')
        await ctx.send(embed=embed)
    elif isinstance(error, commands.ArgumentParsingError):
        embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Hai sbagliato a **menzionare** il canale, **esegui** il comando in questo modo:\n\n**➔**⠀ ⠀{PREFIX}cambiacanale **#vecchiocanale** **#nuovocanale**")
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Hai sbagliato a **menzionare** il canale, **esegui** il comando in questo modo:\n\n**➔** ⠀ {PREFIX}cambiacanale **#vecchiocanale** **#nuovocanale**")
        await ctx.send(embed=embed)

@reset.error
async def reset_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(colour=discord.Colour(0xD40D29), description=f"Devi essere amministratore per eseguire questo comando!")
        await ctx.send(embed=embed)


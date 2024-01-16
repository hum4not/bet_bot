import discord
from discord.ext import commands
import random
import os

version = "BETA"
intents=discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)
running_games = []

tokenz = "YOUR TOKEN"

async def write_a_game(file_name, file_2name, file_bet):
    with open(f'running_games/{file_name}.txt', 'w') as f:
        f.write(f'{file_2name}SPLIT{file_bet}')
    print(f"Logged a game: {file_name} vs {file_2name} - BET: {file_bet}")
async def search_who(file_name):
    File_object = open(rf"{file_name}","r")
    return File_object.readlines().split("SPLIT")[1]
async def search_bet(file_name):
    ...

@client.event
async def on_ready():
    print(f"Hello, you are running {version} version of the casino bot!\nPrefix: {client.command_prefix}")
    print(f"https://discord.com/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot")

#@client.event
#async def on_message(message):
#    print(f"[LOGS] {message.author}: {message.content}")

@client.command()
async def say(ctx,*,tosay):
    await ctx.send(f"{ctx.message.author} said:\n```{tosay}```")

@client.command()
async def fg(ctx,tojoin: discord.Member = None,*,bet: int = None):
    if tojoin != None and bet != None:
        if tojoin.id != ctx.message.author.id:
            #await ctx.message.delete()
            await ctx.send(f"{tojoin} ``you was invited to the fastgame by`` {ctx.message.author}\n``Bet: ``{bet}\n``To join type: `` !fg")
            await write_a_game(tojoin.id, ctx.message.author.id, bet)
        else:
            await ctx.send(f"{tojoin} ``you can't invite yourself to the game``")
    if tojoin == None and bet == None:
        is_game_exists = os.path.isfile(f"running_games/{ctx.message.author.id}.txt")
        if is_game_exists:
           # await ctx.message.delete()
            await ctx.send(f"```Starting the game```\n ")
            file_name = ctx.message.author.id
            File_object = open(f"running_games/{file_name}.txt","r")
            final_list = File_object.readlines()[0].split("SPLIT")
            await ctx.send(f"```GAME```\n<@{ctx.message.author.id}> vs <@{final_list[0]}>\nBET: **{final_list[1]}**")
            bet1=random.randint(0, 36)
            bet2=random.randint(0, 36)
            totalwin = int
            sex = await ctx.send(f"<@{ctx.message.author.id}> rolled: {bet1}\n<@{final_list[0]}> rolled: {bet2}")
            if bet1 > bet2:
                await sex.edit(content=f"<@{ctx.message.author.id}> rolled: {bet1}(WON)\n<@{final_list[0]}> rolled: {bet2}(LOST)")
                await ctx.send(f"@{ctx.message.author.id} won {int(final_list[1])*2}")
            if bet2 > bet1:
                await sex.edit(content=f"<@{ctx.message.author.id}> rolled: {bet1}(LOST)\n<@{final_list[0]}> rolled: {bet2}(WON)")
                await ctx.send(f"<@{final_list[0]}> won {int(final_list[1])*2}")
            File_object.close()
            os.remove(f"running_games/{ctx.message.author.id}.txt")
        else:
            await ctx.send(f"``Not found running game for you!``\n``Start your own game: ``!fg (@user) (bet)")


client.run(tokenz)

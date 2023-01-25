import discord
import random
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.members = True
intents.dm_messages = True
intents.dm_typing= True
bot = commands.Bot(command_prefix=':', help_command=None, intents=intents)

@bot.listen()
async def on_ready():
    print("-- no_one est en ligne--\n\n")
    for guild in bot.guilds:
        print(guild)
    changeStatus.start()
    
@bot.command()
async def help(ctx):
    embed = discord.Embed(title = "**Liste des commandes**", description = "les commandes du bot", url="https://www.youtube.com/channel/UC63cDEWkTlQ1PhqenmF0WGQ")
    embed.set_thumbnail(url = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Femoji.gg%2Fassets%2Femoji%2F5061_the_rules.png&f=1&nofb=1")
    embed.add_field(name = "Listes des commandes du bot No'one",value="les commande de no'one", inline=True)
    embed.add_field(name = "**:dm [mention du membre à dm] {le message à envoyé en dm}**",value="permet d'envoyer des message privé anonyme", inline=False)
    embed.add_field(name = "**:salon [le message à envoyé dans le salon ou vous faîtes la commande]**",value="permet de parler anonymement dans un salon", inline=False)
    embed.add_field(name = "**:rumeur [la rumeur à envoyé]**",value="permet de créé une rumeur", inline=False)
    embed.add_field(name = "**:mute [mute la perssone ping]**",value="permet de mute quelqu'un (admin uniquement) METTRE LE RÔLE EN HAUT", inline=False)

    embed.set_footer(text = "Commandes de no'one")
    await ctx.send(embed = embed)

player = [":help", ":dm", ":salon", ":rumeur", "Conneté sur 10 serveurs"]
@tasks.loop(seconds=10)
async def changeStatus():
    game = discord.Game(random.choice(player))
    await bot.change_presence(status = discord.Status.online, activity=game)
@bot.listen()
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel):
        guild = bot.get_guild(978407942187536445)
        channel = guild.get_channel(979477307410485288)
        mp_question = await channel.send( message.author.mention  +  message.content )
        return
@bot.command()
async def dm(message, member: discord.Member,*, content):
    print(f"Un Message privé à été envoyé à {member}, par {message.author}, contenu du message : {content}\n")
    await message.message.delete()
    channel = await member.create_dm()
    await channel.send(content)
    valid = await message.author.create_dm()
    await valid.send(f"Le message à bien été envoyé à {member}")
@bot.command()
async def salon(ctx, * texte):
    await ctx.message.delete() 
    msg_say = await ctx.send(' '.join(texte))
@bot.command()
async def rumeur(ctx,*,texte):
    await ctx.message.delete()
    rumeur = await ctx.send(f"** RUMEUR : \n"+texte+"**"+"\n*votez si elle est réel réaggisez avec : ✅ sinon réagissez avec ❌ si vous pensez que elle est fausse*")
    await rumeur.add_reaction("✅")
    await rumeur.add_reaction("❌")



async def CreateMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(name = "Muted", permissions = discord.Permissions(send_messages = False, speak = False), reason = "création du rôle Muted")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages = False, speak= False)
        return mutedRole
async def GetMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role
    return await CreateMutedRole(ctx)       
@bot.command()
@commands.has_permissions(ban_members = True)
async def mute(ctx, member : discord.Member, * , reason = "Aucune raison assigner"):
    mutedRole = await GetMutedRole(ctx)
    await member.add_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} à été mute !")
bot.run("")
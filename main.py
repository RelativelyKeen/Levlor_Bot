from unittest import expectedFailure
from dotenv import load_dotenv
import discord, json, os, random
from datetime import datetime, timedelta
from discord.ext import commands

dir = os.path.dirname(__file__)

load_dotenv(os.path.join(dir, ".env"))

if os.path.isdir(os.path.join(dir, 'settings')):
    pass
else:
    os.mkdir(os.path.join(dir, 'settings'))
    
if os.path.isdir(os.path.join(dir, 'ranks')):
    pass
else:
    os.mkdir(os.path.join(dir, 'ranks'))
    
if os.path.isdir(os.path.join(dir, 'ranks', 'points')):
    pass
else:
    os.mkdir(os.path.join(dir, 'ranks', 'points'))

def Reverse(list):
    list.reverse()
    return list

def joinguild(guild):
    if os.path.exists(os.path.join(f'{dir}' , 'settings', f'{guild}.json')) == True:
        return
    else:
        with open(os.path.join(f'{dir}' , 'settings', f'{guild}.json'), 'w+') as f:
            json.dump({
                "prefix" : "l!",
                "points" : 200
            }, f, indent=4)
            
    if os.path.exists(os.path.join(f'{dir}' , 'ranks', 'points', f'{guild}.json')) == True:
        return
    else:
        with open(os.path.join(f'{dir}' , 'ranks', 'points', f'{guild}.json'), 'w+') as f:
            json.dump({}, f, indent=4)

def checkfiles(guild):
    if os.path.isdir(os.path.join(f'{dir}' , 'settings', f'{guild}.json')) == True and os.path.isdir(os.path.join(f'{dir}' , 'ranks', f'{guild}.json')) == True and os.path.isdir(os.path.join(f'{dir}' , 'ranks', 'points', f'{guild}.json')) == True and os.path.isdir(os.path.join(f'{dir}' , 'ranks', 'points', f'{guild}.json')) == True:
        return
    else:
        joinguild(guild)
        return 

def get_prefix_start(client, message):
    guild = message.guild.id
    if os.path.exists(os.path.join(f'{dir}' , 'settings', f'{guild}.json')) == True:
        pass
    else:
        joinguild(guild)
        return
    with open(os.path.join(f'{dir}' , 'settings', f'{guild}.json'), 'r') as f:
        x = json.load(f)
        prefix = x["prefix"]
    return prefix

def get_setting(guild, setting):
    with open(os.path.join(f'{dir}' , 'settings', f'{guild}.json'), 'r') as f:
        x = json.load(f)
        setting1 = x[setting]
    return setting1

def set_setting(guild, setting, set):
    with open(os.path.join(f'{dir}' , 'settings', f'{guild}.json'), 'r') as f:
        jsonload = json.load(f)
        jsonload[setting] = set
    with open(os.path.join(f'{dir}' , 'settings', f'{guild}.json'), 'w') as f:
        json.dump(jsonload, f, indent=4)
        
def get_points(guild, user):
    with open(os.path.join(f'{dir}' , 'ranks', 'points', f'{guild}.json'), 'r') as f:
        x = json.load(f)
        try:
            points = x[str(user)]
        except KeyError:
            set_points(guild, user, 0)
        else:
            return points

def add_points(guild, user, points):
    try:
        with open(os.path.join(f'{dir}' , 'ranks', 'points', f'{guild}.json'), 'r') as f:
            jsonload = json.load(f)
            jsonload[str(user)] = jsonload[str(user)] + points
    except KeyError:
        set_points(guild, user, 1)
    else:
        with open(os.path.join(f'{dir}' , 'ranks', 'points', f'{guild}.json'), 'w') as f:
            json.dump(jsonload, f, indent=4)

def set_points(guild, user, points):
    with open(os.path.join(f'{dir}' , 'ranks', 'points', f'{guild}.json'), 'r') as f:
        jsonload = json.load(f)
        jsonload[str(user)] = points
    with open(os.path.join(f'{dir}' , 'ranks', 'points', f'{guild}.json'), 'w') as f:
        json.dump(jsonload, f, indent=4)
        
def get_rank(guild, user):
    with open(os.path.join(f'{dir}' , 'ranks', 'points', f'{guild}.json'), 'r') as f:
        x = json.load(f)
        y={}

        sortedList=sorted(x.values())

        for sortedKey in sortedList:
            for key, value in x.items():
                if value==sortedKey:
                    y[key]=value
        w = Reverse(list(y.keys()))
        return w.index(str(user))+1
    
def get_ranks(guild, user):
    with open(os.path.join(f'{dir}' , 'ranks', 'points', f'{guild}.json'), 'r') as f:
        x = json.load(f)
        y={}

        sortedList=sorted(x.values())

        for sortedKey in sortedList:
            for key, value in x.items():
                if value==sortedKey:
                    y[key]=value
    return Reverse(list(y.keys()))
    
def get_levels(guild):
    with open(os.path.join(f'{dir}' , 'ranks', 'points', f'{guild}.json'), 'r') as f:
        x = json.load(f)
        y={}

        sortedList=sorted(x.values())

        for sortedKey in sortedList:
            for key, value in x.items():
                if value==sortedKey:
                    y[key]=value
    pointsinlevel = get_setting(guild, "points")
    pointslist = Reverse(list(y.values()))
    levels = []
    for i in pointslist:
        levels.append(i//pointsinlevel)
    return levels
    
bot = commands.Bot(command_prefix=(get_prefix_start))
bot.remove_command("help") #makes it so my custom help command works

lastauthor = ""
usertimes = {}

@bot.listen('on_message')
async def on_message(message):
    if (message.author.bot):
        return
    
    global lastauthor
    global usertimes
    
    if not lastauthor:
        lastauthor = message.author.id
        return
    if message.author.id == lastauthor:
        return
    
    now = datetime.now()
    more = now + timedelta(0, random.randint(7, 12))
    usertimes.update({message.author.id : more.strftime("%H:%M:%S")})
    if datetime.now() > datetime.strptime(usertimes[message.author.id], "%H:%M:%S"):
        add_points(message.guild.id, message.author.id, 1)
    
    pointsforlevel = get_setting(message.guild.id, "points")
    points = get_points(message.guild.id, message.author.id)
    if points == 0:
        return
    elif points % pointsforlevel == 0:
        await message.reply(f"<@{message.author.id}> Just leveled up to level {points // pointsforlevel}!")
        if discord.utils.get(message.guild.roles, name=f"Level {points // pointsforlevel}"):
            role = discord.utils.get(message.guild.roles, name=f"Level {points // pointsforlevel}")
            oldrole = discord.utils.get(message.guild.roles, name=f"Level {points // pointsforlevel-1}")
            user = message.author
            await user.add_roles(role)
            await user.remove_roles(oldrole)
        else:
            await message.guild.create_role(name=f"Level {points // pointsforlevel}", colour=discord.Colour(0xFFD700))
            role = discord.utils.get(message.guild.roles, name=f"Level {points // pointsforlevel}")
            oldrole = discord.utils.get(message.guild.roles, name=f"Level {points // pointsforlevel-1}")
            user = message.author
            await user.add_roles(role)
            await user.remove_roles(oldrole)
    
    lastauthor = message.author.id

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Game(name="l!help"))
    
@bot.event
async def on_guild_join(guild):
    joinguild(guild.id)
    
@bot.command()
async def level(ctx, user: discord.User=None):
    if not user:
        pointsforlevel = get_setting(ctx.guild.id, "points")
        try:
            points = get_points(ctx.guild.id, ctx.author.id)
        except TypeError:
            points = get_points(ctx.guild.id, ctx.author.id)
        level = points // pointsforlevel
        pointsleft = points % pointsforlevel
        author = ctx.message.author
        pfp = author.avatar_url
        rank = get_rank(ctx.guild.id, ctx.author.id)
    elif user.bot:
        await ctx.send("User is a bot")
    else:
        pointsforlevel = get_setting(ctx.guild.id, "points")
        points = get_points(ctx.guild.id, user.id)
        level = points // pointsforlevel
        pointsleft = points % pointsforlevel
        author = user
        pfp = author.avatar_url
        rank = get_rank(ctx.guild.id, user.id)
    await ctx.send(embed=discord.Embed.from_dict({
      "title": f"**Rank:** #{rank}",
      "color": 0,
      "description": f"**Level:** {level}\n\n*Points:* {pointsleft}/{pointsforlevel}",
      "timestamp": "",
      "author": {
        "name": f"{author}",
        "icon_url": f"{pfp}"
      },
      "image": {},
      "thumbnail": {},
      "footer": {},
      "fields": []
    }))

@bot.command()
async def leaderboard(ctx):
    levels = get_levels(ctx.guild.id)
    ranks = get_ranks(ctx.guild.id, ctx.author.id)
    names = []
    for i in ranks:
        username = await bot.fetch_user(int(i))
        names.append(username)
    while True:
        if len(names) >= 10:
            break
        else:
            names.append("Nobody")
    while True:
        if len(levels) >= 10:
            break
        else:
            levels.append(0)
    await ctx.send(embed=discord.Embed.from_dict({
      "title": "**Leaderboard**",
      "color": 0,
      "description" : f"**1.** {names[0]} - *Level: *{levels[0]}\n**2.** {names[1]} - *Level: *{levels[1]}\n**3.** {names[2]} - *Level: *{levels[2]}\n**4.** {names[3]} - *Level: *{levels[3]}\n**5.** {names[4]} - *Level: *{levels[4]}\n**6.** {names[5]} - *Level: *{levels[5]}\n**7.** {names[6]} - *Level: *{levels[6]}\n**8.** {names[7]} - *Level: *{levels[7]}\n**9.** {names[8]} - *Level: *{levels[8]}\n**10.** {names[9]} - *Level: *{levels[9]}",
      "timestamp": "",
      "image": {},
      "thumbnail": {},
      "footer": {},
      "fields": []
    }))

#help command
@bot.command()
async def help(ctx):
    prefix = get_setting(ctx.guild.id, "prefix")
    checkfiles(ctx.guild.id)
    await ctx.send(content=None, embed=discord.Embed.from_dict(
    {
      "title": "Levlor Help",
      "color": 0,
      "description": "This is a list of commands use any to bring up further info",
      "timestamp": "",
      "author": {
        "name": "",
        "icon_url": ""
      },
      "image": {},
      "thumbnail": {},
      "footer": {},
      "fields": [
        {
          "name": f"{prefix}help",
          "value": "you just used this"
        },
        {
          "name": f"{prefix}settings",
          "value": "used to configure the bot"
        },
        {
          "name": f"{prefix}level",
          "value": "shows user level, rank, and points"
        },
        {
          "name": f"{prefix}leaderboard",
          "value": "shows server leaderboard"
        }
      ]
    }
  ))    

#settings command
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def settings(ctx, setting, args):
    prefix = get_setting(ctx.guild.id, "prefix")
    
    if setting == "prefix" and args and len(args) <= 5:
        set_setting(ctx.guild.id, "prefix", args)
        await ctx.send(f'Prefix changed to: {args}')
    elif setting == "prefix" and args and len(args) >= 5:
        await ctx.send("Choosen prefix too long")  
        
        
#settings help message if there is no args
@settings.error
async def flip_error(ctx, error):
    prefix = get_setting(ctx.message.guild.id, "prefix")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(content=None, embed=discord.Embed.from_dict({
             "title": "List Of Settings",
             "color": 0,
             "timestamp": "",
             "author": {},
             "image": {},
             "thumbnail": {},
             "footer": {},
             "fields": [
               {
                 "name": "prefix",
                 "value": f"used to change bot prefix\nusage: {prefix}settings prefix <new prefix>"
               }
             ]
           }))

if __name__ == '___main__': 
    pass

#runs bot using KEY enviroment vaiable gotten from .env
bot.run(os.environ.get("KEY"))
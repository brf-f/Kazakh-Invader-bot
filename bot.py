# public bot.py
import datetime
import os
import random
from random import randrange
from table2ascii import table2ascii as t2a, PresetStyle
import sqlite3
import time
import aiohttp
import emoji

trivia_question = None
questions = None


from pyrandmeme import *

from requests import get

import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
import asyncio

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
#activity
activity = discord.Activity(type=discord.ActivityType.listening, name="Horsestyle")

client = commands.Bot(command_prefix = "mongol ", activity=activity, status=discord.Status.idle, intents=intents)

general_channel = None
bots_channel = None
guild = None

#location of folder
KazakInvader_location = "C:/Users/[USER]/OneDrive/discordBots/Kazak Invader"

#discord ID's
user1 = 77072897512728167
user2 = 58145454893406618

num_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "🔟"]

#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

#PREFIX: "mongol"

@client.event
async def on_ready():
    client.session = aiohttp.ClientSession()
    global general_channel, bots_channel, guild
    print(f'{client.user.name} has connected to Discord!')
    general_channel = client.get_channel(108378950026789697)
    bots_channel = client.get_channel(108378960731912621)
    guild = general_channel.guild
    await bots_channel.send("Bot online")
    MongolOTW.start()
    #while True:
    #    await general_channel.send(input("Enter what to send: "))


#~~~~~~~~~~~~~~~~~~

# cmd for admin bot commands
@client.command(name = "cmd", description="for admin only")
async def cmd(ctx):
    author = ctx.message.author
    if author.id != user1: #not bot admin running this
        await ctx.reply("you need to be the bot admin to run this command")
        return
    else: #is bot author
        await ctx.reply("Check your CMD to proceed, all bot commands will be paused until this is complete")
        cmd_ = input("Enter command here:")
        match cmd_:
            
            case "help": #show commands
                print("stop")
                print("del")
                print("MOTWAnnounce")
                print("MOTWVote")
                print("createTable")
                print("sql")
                print("send_message")
                print("VCKick")
                print("VCMove")
                
                await cmd(ctx)
            
            case "stop": #stop running program
                if input("Are you sure you want to put the bot offline?") == "Y":
                    await bots_channel.send("Bot offline")
                    await client.close()
                    exit()
            case "del": #delete something
                inp = input("channel or message or other")
                if inp == "channel":
                    inp = input("enter channel id")
                    fetched = await client.fetch_channel(inp)
                    await fetched.delete()
                elif inp == "message":
                    inp = input("enter message id")
                    inp2 = input("enter message channel id")
                    channel = await client.fetch_channel(inp2)
                    fetched = await channel.fetch_message(inp)
                    await fetched.delete()
                else:
                    item = input("what do you want to delete?")
                    await eval(item).delete()
                print("deleted")
                
            case "MOTWAnnounce":
                await MOTWAnnounce()
            case "MOTWVote":
                await MOTWVote()
            
            case "createTable":
                await createTable(ctx)
            case "sql":
                database = input("Enter database: ")
                conn = sqlite3.connect(database)
                c = conn.cursor()
                eval(input("Enter command: "))
                conn.commit()
                conn.close()
                print("\nDone")
                
            case "send_message":
                await general_channel.send(input("Enter what to send: "))
                
            case "VCKick":
                user = input("What is the user's ID?")
                guild = ctx.guild
                memberTarget = guild.get_member(int(user))
                await memberTarget.move_to(None)
                
            case "VCMove":
                user = input("What is the user's ID?")
                guild = ctx.guild
                memberTarget = guild.get_member(int(user))
                moveTo = await client.fetch_channel(input("channel id"))
                await memberTarget.move_to(moveTo)
                
            case _: #no special command
                eval(cmd_)
    


#quotes
authordict = {
    user1 : 0,
    user2 : 1,
}
inv_dict = {v: k for k, v in authordict.items()} # inverse of authordict

    #0 = user1, 1 = user2, etc.
quotes = [
        ["quote", "quote"], #user1
        ["quote", "quote"] #user2
]

# quote leaderboard
@client.command(name = "quoteboard", description="shows a quote leaderboard")
async def quoteboard(ctx):
    quoteboard = []
    for author in range(len(quotes)):
        user = await client.fetch_user(inv_dict[author])
        quoteboard.append([user.name,len(quotes[author])])
    
    quoteboard = sorted(quoteboard,key=lambda l:l[1], reverse=True)
    for i in range(len(quoteboard)):
        quoteboard[i].insert(0, i+1)
        
    output = t2a(
    header=["Rank", "User", "Total Quotes"],
    body=quoteboard,
    first_col_heading=True
    )   
    await ctx.reply(f"*->*\n\n**Quotes Leaderboard:**\n```\n{output}\n```")

#give quote
@client.command(name = "quote", description="shows a random quote [User can be added as arg]")
async def quote(ctx, target: discord.Member = None):
    
    if not target:
        target = randrange(len(quotes))
    else:
        target = authordict[target.id]
        
    if ctx.author == client.user:
            return


    print("mongol quote")
    author = target
    response = random.choice(quotes[author])
    author = inv_dict[author]
            
    user = await client.fetch_user(author)
    #give quote
    await ctx.reply(f"***\"{response}\"*** **- {user.name}**")


#ping user
#@client.command(name = "pingUser", description="Pings user the specified number of times")
#async def pingUser(ctx, num = "1"):
#    if ctx.author == client.user:
#            return
#
#    #invalid command
#    if not num.isnumeric() or int(num) < 1 or int(num) > 100:
#         await ctx.reply("I cannot do that")
#         return
#    
#    #ping him
#    print("pinging User")
#    response = "<@" + str(user) + ">"
#    for i in range(int(num)):
#        await ctx.channel.send(response)
#
#    #print done
#    await ctx.reply("All done :)")


#Invade dm
@client.command(name = "InvadeDM", description="Invades specified users DM [Blank=Author]")
async def InvadeDM(ctx, target: discord.Member = None):

    if not target:
        target = ctx.message.author

    if ctx.author == client.user:
            return

    #invalid command
    try:
        channel = await target.create_dm()
        #invade dm
        print("Invading DM")
        response = f"{ctx.message.author.name} Invaded you!"
        await channel.send(response)

        #print done
        await ctx.reply("Successful raid :)")
    except:
        await ctx.reply("there was an error")
        return


#show random role
@client.command(name = "fact", description="shows a random role of specified user [Blank=Author]")
async def fact(ctx, target: discord.Member = None):

    if not target:
        target = ctx.message.author

    if ctx.author == client.user:
            return

    #invalid command
    try:
        response = "**" + str(random.choice(target.roles)) + "**"
        #avoid @everyone
        everyone = "**" + str(target.roles[0]) + "**"
        while response == everyone:
             response = "**" + str(random.choice(target.roles)) + "**"
        #print role
        print("user fact (role)")
        await ctx.reply(response)

    except:
        await ctx.reply("there was an error")
        return


#Invade VC
@client.command(name = "InvadeVC", description="Invade VC of specified target, or yourself if noone is specified [Blank=Author]")
async def InvadeVC(ctx, target: discord.Member = None):

    if not target:
        target = ctx.message.author

    if ctx.author == client.user:
            return

    #invalid command
    try:
        # grab the user who sent the command
        user=target
        voice_channel=user.voice.channel

        # play music
        vc= await voice_channel.connect()
        player = discord.FFmpegPCMAudio(executable=KazakInvader_location+"/ffmpeg-2023-03-23-git-30cea1d39b-essentials_build/bin/ffmpeg.exe", source="InvadeAudio.mp3")
        await ctx.reply("Invasion started")
        vc.play(player)
        while vc.is_playing():
            await asyncio.sleep(1)

        # disconnect after the player has finished
        await ctx.reply("Invasion finished")
        await vc.disconnect()

    except:
        await ctx.reply("there was an error")
        return

#poll
@client.command(name = "poll", description="make a poll")
async def poll(ctx, question=None, option1="Yes", option2="No"):
    if not question:
        await ctx.reply("No question was given")
        return
    pollmsg = f"**{question}\n\n✅ = {option1}\n❎ = {option2}\n\n||<@everyone>||**"
    msg = await ctx.reply(pollmsg)
    await msg.add_reaction('✅')
    await msg.add_reaction('❎')


#levels ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#create table
#@client.command(name = "createTable", description="create sql table")
#async def createTable(ctx):
#    conn = sqlite3.connect('levels.db')
#    cur = conn.cursor()
#    cur.execute("""
#    CREATE TABLE levelsTable(
#    userid INT PRIMARY KEY,
#    xp INT,
#    level INT
#    );
#    """)
#    conn.commit()
#    conn.close()
#    await ctx.reply("succesfull")
#
##insert new user
#@client.command(name = "insertUser", description="insert user into sql table")
#async def insertUser(ctx, target: discord.Member = None):
#    if not target:
#        target = ctx.message.author
#    member = target
#    user = member.id
#    conn = sqlite3.connect('levels.db')
#    cur = conn.cursor()
#    cur.execute('INSERT INTO levelsTable("userid", "xp", "level")VALUES(?, ?, ?)', (user, 0, 0,))
#    conn.commit()
#    conn.close()
#    await general_channel.send(f'**Hi <@{member.id}>, welcome to the Mongol regime!**')

#add user to db and greet when join
@client.event
async def on_member_join(member): ###add a row in the db for the new member when they join
   user = member.id
   conn = sqlite3.connect('levels.db')
   cur = conn.cursor()
   cur.execute('INSERT INTO levelsTable("userid", "xp", "level")VALUES(?, ?, ?)', (user, 0, 0,))
   conn.commit()
   conn.close()
   await general_channel.send(f'**Hi <@{member.id}>, welcome to the Mongol regime!**')

#check levels
@client.command(name = "level", description="check user level")
async def level(ctx, target: discord.Member = None):
    print("Showing level")
    if not target:
        target = ctx.message.author
    
    conn = sqlite3.connect('levels.db')
    cur = conn.cursor()
    row = cur.execute('SELECT xp, level FROM levelsTable WHERE userid = ?', (target.id,)).fetchone()
    show_xp = row[0] ##the first item in the index, in this case, xp
    show_level = row[1] ## the second item in the index, in this case, level

    await ctx.reply(f'**{target.name} is mongol level:  {show_level}, \t xp: {show_xp}/100**')
    
#check levels leaderboard
@client.command(name = "leaderboard", description="shows mongol levels leaderboard")
async def leaderboard(ctx):
    print("Showing leaderboard")
    
    conn = sqlite3.connect('levels.db')
    cur = conn.cursor()
    leaderboard = []
    
    for record in cur.execute('SELECT * FROM levelsTable ORDER BY level DESC, xp DESC').fetchall():
        user = await client.fetch_user(record[0])
        user = user.name
        leaderboard.append([len(leaderboard)+1, user, record[2], record[1]]) #user, xp, level
    
    output = t2a(
        header=["Rank", "User", "Level", "XP"],
        body=leaderboard,
        first_col_heading=True
        )   

    await ctx.reply(f"*->*\n\n**Mongol Leaderboard:**\n```\n{output}\n```")

#member messages
member_messages = {}

#level with messages
@client.event
async def on_message(message):
    
    global questions, trivia_question
    if trivia_question:
        
        answer = message.content.lower().replace(" ", "").replace("*", "").replace("(", "").replace(")", "").replace("^", "").replace(",", "")             #makes more answers accepted
        
        trivia_answer = [sub.lower().replace(" ", "").replace("*", "").replace("(", "").replace(")", "").replace("^", "").replace(",", "") for sub in trivia_question[1]]     #makes more answers accepted
        
        if answer in trivia_answer:
            print("correct trivia answer")
            await message.reply("**Correct!**")
            await triviaQuestion(message.channel)
            
        elif answer == "stop":
            print("stopped trivia")
            await message.channel.send("**Stopped trivia**")
            questions = None
            trivia_question = None
            
        elif answer == "answer":
            print("giving answer")
            await message.reply(f"```answer: {trivia_question[1][0]}```")
            await triviaQuestion(message.channel)
            
        elif answer == "question":
            print("giving question again")
            await message.reply(f"```Q: {trivia_question[0]}```")
    
    u = await Khanquest_message(message)
    
    try:
        
        user = int(message.author.id)
    
        if not (user in member_messages): #member not in dict sent message
            print("new member message")
            member_messages[user] = time.time()
            
        if (message.author == client.user) or (user == 715906723982082139) or (user == 270904126974590976) or  (time.time() - member_messages[user] < 30): #anti spam or bugs with bot
                #allows other commands to run
                if u != "NO":
                    await client.process_commands(message)
                return
            
        member_messages[user] = time.time() #reset timer for user
        conn = sqlite3.connect('levels.db')
        cur = conn.cursor()
        row = cur.execute('SELECT xp, level FROM levelsTable WHERE userid = ?', (user,)).fetchone()
        old_xp = row[0] ##the first item in the index, in this case, xp
        old_level = row[1] ## the second item in the index, in this case, level
        new_xp = old_xp + 1
        new_level = old_level
        if new_xp > 100: #this is where you set the threshold for leveling up
            new_level = old_level + 1
            new_xp = 0
            await bots_channel.send(f'**{message.author.name} is a Certified Mongol!\nThey are now level:  {new_level}**')
        cur.execute('UPDATE levelsTable SET xp = ?, level = ? WHERE userid = ?', (new_xp, new_level, user,))
        conn.commit()
        conn.close()
        
    except:
        print("Error on message leveling")
        pass

    #allows other commands to run
    if u != "NO":
        await client.process_commands(message)


#         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
sent_memes = []
#send Meme from reddit command
@ client.command(pass_context=True)
async def meme(ctx):
    global sent_memes
    async with aiohttp.ClientSession() as cs:
        async with cs.get(
                'https://www.reddit.com/r/meme/new.json?sort=new') as r:
            res = await r.json()
            foundmeme = res['data']['children'][random.randint(0, 25)]['data']
            url = foundmeme['url']
            
            # check if meme has been sent - skip if so
            while url in sent_memes:
                if len(res['data']['children'])<1:
                    print("reset sent memes")
                    sent_memes = []
                foundmeme = res['data']['children'][random.randint(0, len(res['data']['children']))]['data']
                url = foundmeme['url']

            sent_memes.append(url) # add url to list of sent_memes
                
            embed = discord.Embed(title=foundmeme["title"], description="")
            embed.set_image(url=url)
            
            try:
                foundmeme["preview"]["images"][0]["source"]["url"]
            except: #no image
                print("skipped non image meme")
                await meme(ctx)
                return
        
            says = ["***The most mongol meme I could find:***", "***Suleyman would approve:***", "***Most normal day in Kazakstan:***", "***Jack Bresky literally made this:***"]
            await ctx.send(random.choice(says),embed=embed)

#~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|
    
    #KHANQUEST ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
#Khanquest get commands
@client.event
async def Khanquest_message(message):
    #for checking table column names
    #conn2 = sqlite3.connect("gamedata.db")
    #c2 = conn2.cursor()
    #
    #c2.execute("PRAGMA table_info(itemsTbl)")
    #print(c2.fetchall())
    #
    #conn2.close()
    
    
 #       #check for Khanquest
     #connect to active games databse
    conn = sqlite3.connect("ActiveGames.db")
    c = conn.cursor()

    active_games = c.execute('SELECT ChannelID FROM ActiveGamesTbl').fetchall()
    if (message.channel.id,) in active_games:
        
        prefix = message.content.startswith('mongol')
        if prefix: #prevent commands in game
            await message.delete()
            await message.channel.send("Cannot run commands here")
            return "NO"
        
        if (message.author.id,) != c.execute('SELECT Player FROM ActiveGamesTbl WHERE ChannelID = ?', (message.channel.id,)).fetchone(): #not correct player
            return
        
        
        #check for awaiting confirmation
        conn2 = sqlite3.connect("gamedata.db")
        c2 = conn2.cursor()
        todo = c2.execute("SELECT do FROM confirmRequestTbl WHERE ChannelID =?", (message.channel.id,)).fetchone()[0]
        print(todo)
        if todo != ".":   #is awaiting confirm
            #reset it to nothing
            c2.execute("UPDATE confirmRequestTbl SET do = ? WHERE ChannelID =?", (".", message.channel.id,))
            conn2.commit()
            conn2.close()
            
            inp = message.content.lower()
            
            if inp == "y" or inp == "yes":
                await eval(todo)(message.channel, message.author.id)
                print("confirmed")
            else:
                print("denied")
                await message.channel.send("You did not do it")
                
            return
        
        conn2.commit()
        conn2.close()
    
# ~~~~~~~~~~~~~~~~~~~     ACTIONS     ~~~~~~~~~~~~~~~~~~~~~~


        #check for movement

        #is in a valid Khanquest game channel
        actn = message.content.lower()

        directions = ["n","s","e","w", "north", "south", "east", "west"]
        if actn in directions:
            await Khanquest_move(actn, message.channel, message.author.id)
            
        elif actn == "help" or actn == "h": #help
            await Khanquest_help(message.channel, message.author.id)
            
        #check for other commands
        elif actn == "look" or actn == "l": #look
            await Khanquest_look(message.channel, message.author.id)
        elif actn == "inventory" or actn == "i": #inventory
            await Khanquest_Inventory(message.channel, message.author.id)
        elif actn == "map" or actn == "m": #map
            await Khanquest_Map(message.channel, message.author.id)
        elif actn == "end": #end
            await message.channel.send("```(?) " + "Are you sure you would like to end your current game?" + "```")
            await Khanquest_Confirm(message.author.id, message.channel, "Khanquest_End")

       #No valid command
        else:
            await message.reply(f"Invalid Command")
        
    conn.close()
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    
async def KhanquestNew(ctx): #start new Khanquest game instance

    #connect to active games databse
    conn = sqlite3.connect("ActiveGames.db")
    c = conn.cursor()

    print("Khanquest")
    player = ctx.message.author.id

    active_games = c.execute('SELECT Player FROM ActiveGamesTbl').fetchall()
    print(active_games)
    #if player does not have an active game
    if not ((player,) in active_games):
        #only allow user to view channel
        overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.message.author: discord.PermissionOverwrite(read_messages=True)
        }
        #create channel in category
        name = 'Khanquest'
        category = discord.utils.get(ctx.guild.categories, name=name)

        channel = await ctx.guild.create_text_channel('Khanquest', category=category, overwrites=overwrites)
        print("Channel created")
        #set perms and redirect to channel
        channel.set_permissions(ctx.guild.default_role, send_messages=False)

        c.execute('INSERT INTO ActiveGamesTbl ("ChannelID", "Player") VALUES (?,?)', (channel.id, player))


        # Init gamedata
        conn2 = sqlite3.connect("gamedata.db")
        c2 = conn2.cursor()

        c2.execute("INSERT INTO roomTbl VALUES (?,?,?)", (player, 2, 0,)) #user, y, x
        #userID, Map, Sword, Horse, EagleOfLife, HorseOfPower, Chalice, DaggerOfWisdom, PreciousJade, GuardShiftsPlanner
        c2.execute("INSERT INTO itemsTbl VALUES (?,?,?,?,?,?,?,?,?, ?)", (player, 0, 0, 0, 0, 0, 0, 0, 0, 0,)) #user, 9*items bool values -> 1= player has | 0= player doesnt have
        try:
            c2.execute("INSERT INTO confirmRequestTbl VALUES (?,?,?)", (channel.id, player,".",))
        except:
            c2.execute("UPDATE confirmRequestTbl SET do = ? WHERE userID =?", (".", player,))

        conn2.commit()
        conn2.close()

            #Redirect to game    
        await ctx.reply(f"**Khanquest game started in : <#{channel.id}>**")
        await channel.send(file=discord.File('Khanquest_banner.png'))
        await channel.send("*Khanquest game started*")
        description = """*_
You are Genghis Khan, the Emperor of the Mongol Empire, on a quest to uncover the secrets of the forbidden Yurt. 
As the greatest conqueror of your time, you must navigate through treacherous terrain and outwit your enemies to find the ultimate prize: the Eagle of Life and the Horse of Power. 
Navigate between rooms to find new challenges and minigames such as Eagle Hunting, which will give you the tools required on your journey.
        _*"""
        await channel.send(description)
        await channel.send("**Type: 'h' for help**")
            
        
    else: #has active game
        #Redirect to game    
        channel = c.execute("SELECT ChannelID FROM ActiveGamesTbl WHERE Player = ?", (player,)).fetchone()[0]
        await ctx.reply(f"**You have an active game in : <#{channel}>**")

    conn.commit()
    conn.close()




#rooms()
class new_room:
    def __init__(self, name, lookStr, items):
        self.name = name
        self.lookStr = lookStr
        self.items = items

room00 = new_room("City", "Your empire city lies before you", "(!) You know a cartographer is around here")
room02 = new_room("Stables", "These are the Horses Stables, horses of all kind are lined up. Sullymen would love this place.", "(!) You can take something in this room")
room10 = new_room("Palace Court", "The Palace Court lies in front of you, with people scuttering about, bowing to you as they see you. Large gates extend in front, below the stairs.", "Nothing in this room")
room11 = new_room("The Wall", "This is a large stone wall protecting your nation from intruders.\nYou hide and check your planner for the guard shifts and make your move when you know its safe.", "Nothing in this room")
room12 = new_room("Great Field", "A large field with brownish grass, not many people are here.", "Nothing in this room")
room13 = new_room("Gobi Desert", "Vast expanses of desert, extending beyond view", "The Forbidden Yurt is somewhere here")
room20 = new_room("Bedroom", "This is a smaller room, with a large bed taking up most of the center of the room.", "Nothing in this room")
room30 = new_room("Throne Room", "This is a large room, not too wide but with a carpet extending beyond view. At the end of the room, a large wooden Throne with ornate decorations can be seen.", "(!) Your commander is in this room")
#room00 = new_room("name", "look", "Nothing in this room")
#print(room48.name, room48.lookStr, room48.items)

#define rooms
rooms = [[room00, "", room02],[room10, room11, room12, room13], [room20] , [room30]] #rooms [y][x] | s=[0][x], n=[3][x], e=[x][1], w=[0]

def Khanquest_room(user):
    conn = sqlite3.connect("gamedata.db")
    c = conn.cursor()
    a = c.execute("SELECT * FROM roomTbl WHERE userID = ?", (user,)).fetchone()
    room = [0,0]
    print(a)
    room[0] = a[1] #(user, y,x)
    room[1] = a[2]

    conn.commit()
    conn.close()

    return room

#get current room
def Khanquest_currRoom(user):

    room = Khanquest_room(user)

    return rooms[room[0]][room[1]]

    
async def Khanquest_move(dir, channel, userID):
    print("Khanquest move")
    
    if Khanquest_currRoom(userID).name == "Gobi Desert": #in gobi desert
        await Khanquest_GobiDesert(channel, userID)
        return
    
    if len(dir) > 1:
            dir = dir[0]

    tempRoom = Khanquest_room(userID)[:]
    match dir:
        case "n":
            tempRoom[0] += 1
        case "s":
            tempRoom[0] -= 1
        case "e":
            tempRoom[1] += 1
        case "w":
            tempRoom[1] -= 1

    try:
        if (tempRoom[0] >= 0 and tempRoom[1] >= 0) and (not rooms[tempRoom[0]][tempRoom[1]] == ""): #prevent negative index == last element, filler room, and no room
            
            conn = sqlite3.connect("gamedata.db")
            c = conn.cursor()
            c.execute("UPDATE roomTbl SET  x = ?, y = ? WHERE userID = ?", (tempRoom[0], tempRoom[1], userID,)) #user, x, y
            conn.commit()
            c.close()
            
            #move to room
            await channel.send("```> " + "moved to: "+ Khanquest_currRoom(userID).name + "```")
            await channel.send("**" + Khanquest_currRoom(userID).items + "**")
            await Khanquest_moveAction(userID, channel)
        else:
            await channel.send("Can't go there")
    except:
        await channel.send("Can't go there")
    
async def Khanquest_Confirm(userID, channel, function):
    print("khanquest confirming")
        # Init gamedata
    conn = sqlite3.connect("gamedata.db")
    c = conn.cursor()

    c.execute("UPDATE confirmRequestTbl SET do = ? WHERE userID =?", (function, userID,))

    conn.commit()
    conn.close()
    

async def Khanquest_lookAction(userID, channel):
    
    room = Khanquest_currRoom(userID).name
    
    if room == "Throne Room": #has commander
        print("awaiting input for commander")
        await channel.send("```(?) " + "You see your commander in the corner, would you like to speak to him?" + "```")
        await Khanquest_Confirm(userID, channel, "Khanquest_talkCommander")
        
    elif room == "City": #has cartographer and angry kazak man
        conn = sqlite3.connect("gamedata.db")
        c = conn.cursor()
        map = c.execute("SELECT Map FROM itemsTbl WHERE userID = ?", (userID,)).fetchone()[0]
        conn.close()
        
        if map == 0: #cartographer
            print("awaiting input for cartographer")
            await channel.send("```(?) " + "You know a well known cartographer lives around these parts, would you like to go visit him?" + "```")
            await Khanquest_Confirm(userID, channel, "Khanquest_talkCartographer")
            
    elif room == "Stables": #has horses
        conn = sqlite3.connect("gamedata.db")
        c = conn.cursor()
        horse = c.execute("SELECT Horse FROM itemsTbl WHERE userID = ?", (userID,)).fetchone()[0]
        conn.close()
        
        if horse == 0: #doesnt have horse
            print("get horse option")
            await channel.send("```(?) " + "You think to yourself a ride might be useful, do you take a horse?" + "```")
            await Khanquest_Confirm(userID, channel, "Khanquest_takeHorse")
        else:
            await channel.send("*You already got yourself the sturdiest horse you could find here.*")
            
    else:
        await channel.send("**" + Khanquest_currRoom(userID).items + "**")


async def Khanquest_moveAction(userID, channel):
    
    room = Khanquest_currRoom(userID).name
        
    if room == "The Wall": #you need to have the shifts planner
        
        conn = sqlite3.connect("gamedata.db")
        c = conn.cursor()
        
        planner = c.execute("SELECT GuardShiftsPlanner FROM itemsTbl WHERE userID = ?", (userID,)).fetchone()[0]
        
        if planner == 0: #doesn't have planner
            print("Went to wall without planner")
            
            #set room back
            c.execute("UPDATE roomTbl SET  x = ?, y = ? WHERE userID = ?", (2, 0, userID,))
            
            await channel.send("```(~) The guards see you lurking around the wall and escort you back to your room, this is not somwehere for the Khagan to be```")
            await channel.send("```> You are back in your room```")
            
        else: #went to wall with planner
            await channel.send("```(~) You carefully looked at the planner and chose the perfect moment to make a run for it over the great wall.\nThat was a close one!```")
        conn.commit()
        conn.close()
        
    elif room == "City": #has cartographer and angry kazak man
        conn = sqlite3.connect("gamedata.db")
        c = conn.cursor()
        map = c.execute("SELECT Map FROM itemsTbl WHERE userID = ?", (userID,)).fetchone()[0]
        conn.close()
        
        if map == 1: #angry Kazak man
            print("angry Kazak man")
            await channel.send("*You wander around the city, testing your luck again in a place where many hate you.\nYou don't get far before you feel a cold piece of steel sliding into your back as an angry Kazak man runs off.*")
            #adventure over
            await Khanquest_AdventureEnd(userID, channel)
        
    elif room == "Gobi Desert": # needs horse
        print("needs horse")
        conn = sqlite3.connect("gamedata.db")
        c = conn.cursor()
        
        horse = c.execute("SELECT Horse FROM itemsTbl WHERE userID = ?", (userID,)).fetchone()[0]
        
        conn.close()
        
        if horse == 0: #doesn't have horse
            print("Went to desert without horse")
            
            await channel.send("*You attempt to walk across the desert on foot.\nYou don't know what you were thinking, this was never gonna work.*")
            #adventure over
            await Khanquest_AdventureEnd(userID, channel)
        else: # has horse
            await channel.send("```(~) You get onto your robust mount and set off into the desert.\nYou don't know what you would have done had you not found this horse!```")


async def Khanquest_AdventureEnd(userID, channel):
    
    await channel.send("**_\n\nYou Died** \n ```> Your adventure is over``` \n\n --------------------- \n\n.")
    await channel.send("```A new Adventure has started```")
    
    # ReInit gamedata
    conn2 = sqlite3.connect("gamedata.db")
    c2 = conn2.cursor()

    #delete old values
    c2.execute('DELETE FROM itemsTbl WHERE userID = ?', (userID,))
    c2.execute('DELETE FROM roomTbl WHERE userID = ?', (userID,))

    #reput values
    c2.execute("INSERT INTO roomTbl VALUES (?,?,?)", (userID, 2, 0,)) #user, y, x
    #userID, Map, Sword, Horse, EagleOfLife, HorseOfPower, Chalice, DaggerOfWisdom, PreciousJade, GuardShiftsPlanner
    c2.execute("INSERT INTO itemsTbl VALUES (?,?,?,?,?,?,?,?,?, ?)", (userID, 0, 0, 0, 0, 0, 0, 0, 0, 0,)) #user, 9*items bool values -> 1= player has | 0= player doesnt have
    try:
        c2.execute("INSERT INTO confirmRequestTbl VALUES (?,?,?)", (channel.id, userID,".",))
    except:
        c2.execute("UPDATE confirmRequestTbl SET do = ? WHERE userID =?", (".", userID,))

    conn2.commit()
    conn2.close()
 
    await channel.send(file=discord.File('Khanquest_banner.png'))
    await channel.send("*Khanquest game started*")
    await channel.send("**Type: \t'h'\t for help**")
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~functions of what you do
async def Khanquest_GobiDesert(channel, userID):
    print("Gobi Desert Wandering")

    DesertRooms = ["You find nothing but endless sand and dunes", "Suddenly you notice a snake jump at you but an eagle snatches it up before it reaches you", "You are suddenly surrounded by a group of bandits", "You see the white cloth of a Yurt in the distance. You approach but find it abandoned with nothing of value.", "Eagles soar above you", "You suddenly hear the snarl of a large beast.", "A large group of Kazaks wanders towards you.", "You see a large well-built horse in front of you, it stares majestically in your direction, as if inviting you.", "Mongols appear out of nowhere, rushing towards you on horseback.", "There is a cluster of large rocks in front of you" ,"You finally see it, lying in front of you. This has to be the Forbidden Yurt."]    
    
    room = random.randint(0, 16) # 0 to 11  | Add bias for more nothing
    
    Desert_Room =  "You found a bug lurking in the sand"
    
    if room > 10:
        Desert_Room = DesertRooms[0] # Nothing bias
    else:
        Desert_Room = DesertRooms[room]
                        
    await channel.send(f"```> You wander in the desert for a while```\n **{Desert_Room}**")
    
    match room:
            
        case 2: #Bandits - fight of run
            print("Bandits")               #dagger of wisdom
            await channel.send("```(?) " + "Would you like to fight back against the bandits? (Otherwise you run away to try avoiding conflict)" + "```")
            await Khanquest_Confirm(userID, channel, "Khanquest_fightBandits")
        case 5: #Snow Leopard
            print("Snow Leopard")
            await channel.send("```(?) " + "Would you like to try to find this beast?" + "```")
            await Khanquest_Confirm(userID, channel, "Khanquest_fightLeopard")
        case 6: #Kazaks
            print("Kazaks")               #has chalice
            await channel.send("```(?) " + "Would you like to try approaching the Kazaks?" + "```")
            await Khanquest_Confirm(userID, channel, "Khanquest_talkKazaks")
        case 7: #Horse Of Power
            print("Horse Of Power")
            
            #get HorseOfPower
            conn = sqlite3.connect("gamedata.db")
            c = conn.cursor()
            c.execute("UPDATE itemsTbl SET HorseOfPower = 1 WHERE userID = ?", (userID,))
            conn.commit()
            conn.close()
            
            await channel.send("*The Horse of Power seems to follow you*")
            await channel.send("```(?) " + "Would you like to try taking the horse with you?" + "```")
            await Khanquest_Confirm(userID, channel, "Khanquest_takeHorseOfPower")
        case 8: #Mongols
            print("Mongols")
            await channel.send("```(?) " + "Would you like to try approaching the Mongols?" + "```")
            await Khanquest_Confirm(userID, channel, "Khanquest_fightMongols")
        case 9: #Large Rocks               #has precious jade
            print("Large Rocks")
            await channel.send("```(?) " + "Would you like to try going through the rocks?" + "```")
            await Khanquest_Confirm(userID, channel, "Khanquest_searchRocks")
        
        #end
        case 10: #Forbidden Yurt               #    need: Horse Of Power, dagger of wisdom, precious jade, chalice
            print("Forbidden Yurt question")
            
            await channel.send("```(?) " + "Would you like to try entering the forbidden Yurt?" + "```")
            await Khanquest_Confirm(userID, channel, "Khanquest_forbiddenYurt")

#userID, Map, Sword, Horse, EagleOfLife, HorseOfPower, Chalice, DaggerOfWisdom, PreciousJade, GuardShiftsPlanner

async def Khanquest_forbiddenYurt(channel, userID):
    print("Forbidden Yurt")
    #check if has all items
    conn = sqlite3.connect("gamedata.db")
    c = conn.cursor()
    
    HorseOfPower = c.execute("SELECT HorseOfPower FROM itemsTbl WHERE userID = ?", (userID,)).fetchone()[0]
    daggerOfWisdom = c.execute("SELECT DaggerOfWisdom FROM itemsTbl WHERE userID = ?", (userID,)).fetchone()[0]
    PreciousJade = c.execute("SELECT PreciousJade FROM itemsTbl WHERE userID = ?", (userID,)).fetchone()[0]
    Chalice = c.execute("SELECT Chalice FROM itemsTbl WHERE userID = ?", (userID,)).fetchone()[0]
    
    conn.commit()
    conn.close()
    
    if (HorseOfPower == 1) and (daggerOfWisdom == 1) and (PreciousJade == 1) and (Chalice == 1):
        print("Has all items for Yurt")
        await channel.send("** You make your way into the Yurt**")
        await channel.send("```(~) A Forbidden Guard watches you but doesn't say a thing. ```")
        
        await channel.send("*You realise you've made it, you have finally reached the Forbidden Yurt and are ready to be immortalised.*\n**You are proud of what you have accomplished**")
        await channel.send("```(>) Congratulations! This is the end of your journey. You have completed the game.```")
        
        await channel.send(file=discord.File('forbiddenYurt.png'))
        
        await channel.send("```(!) The Eagle Of Life and the Horse Of Power advance towards you, recognizing you as their new master```")
        
        await channel.send("**You suddenly feel a cold knife slide into your neck and realise you have been tricked.**")

        await Khanquest_AdventureEnd(userID, channel)
        
    else:
        print("Doesn't have all items for Yurt")
        await channel.send("** You make your way into the Yurt but a Forbidden Guard steps in and kicks you out as you don't have all that is required. **")
        await channel.send("```(~) You need the Horse Of Power, Dagger Of Wisdom, Precious Jade, and Chalice to enter. ```")


async def Khanquest_searchRocks(channel, userID):
    print("searching rocks")
    
    #got jade
    conn = sqlite3.connect("gamedata.db")
    c = conn.cursor()
    
    jade = c.execute("SELECT PreciousJade FROM itemsTbl WHERE userID = ?", (userID,)).fetchone()[0]
    
    if jade == 1:
        print("already has")
        conn.close()
        await channel.send("**You try to make your way through the rocks but a large boulder collapses on you out of nowhere**")
        await Khanquest_AdventureEnd(userID, channel)
    else:
    
        c.execute("UPDATE itemsTbl SET PreciousJade = 1 WHERE userID = ?", (userID,))
        conn.commit()
        conn.close()
        
        await channel.send("** You make your way through the rocks when a reflection catches the corner of your eye. **")
        await channel.send("```(!) You find a Precious Jade burried between the rocks and take it with you. ```")

async def Khanquest_fightLeopard(channel, userID):
    print("fight leopard")
    await channel.send("*You bearly get a glimpse of the Snow Leopard before your mount gets ripped from under you and you feel the strength of its jaws.\n You don't know what you were thinking*")
    await Khanquest_AdventureEnd(userID, channel)
    
async def Khanquest_fightMongols(channel, userID):
    print("fight mongols")
    await channel.send("**You get overwhelmed by their fierce battle song as you approach them. \n They surround you before you even notice and now there is nothing you can do.\n They didn't realise who you were**")
    await Khanquest_AdventureEnd(userID, channel)

async def Khanquest_fightBandits(channel, userID):
    print("fight bandits")
    
    #got dagger
    conn = sqlite3.connect("gamedata.db")
    c = conn.cursor()
    
    dagger = c.execute("SELECT DaggerOfWisdom FROM itemsTbl WHERE userID = ?", (userID,)).fetchone()[0]
    
    if dagger == 1:
        print("already has")
        conn.close()
        await channel.send("**The bandits get you and you are helpless as they take all you have**")
        await Khanquest_AdventureEnd(userID, channel)
    else:
    
        c.execute("UPDATE itemsTbl SET DaggerOfWisdom = 1 WHERE userID = ?", (userID,))
        conn.commit()
        conn.close()
        
        await channel.send("** You fight back against the bandits and manage to knock the down. **")
        await channel.send("```(!) You find the dagger of wisdom in one of the bandit's clothing and take it with you. ```")
    
async def Khanquest_talkKazaks(channel, userID):
    print("talked to kazaks")
    
    #got chalice
    conn = sqlite3.connect("gamedata.db")
    c = conn.cursor()
    
    chalice = c.execute("SELECT Chalice FROM itemsTbl WHERE userID = ?", (userID,)).fetchone()[0]
    
    if chalice == 1:
        print("already has")
        conn.close()
        await channel.send("**The Kazaks were not too friendly this time and take all you have and leave you helpless in the desert to die**")
        await Khanquest_AdventureEnd(userID, channel)
    else:
    
        c.execute("UPDATE itemsTbl SET Chalice = 1 WHERE userID = ?", (userID,))
        conn.commit()
        conn.close()
        
        await channel.send("* You talk to the Kazaks and they seem to be a pretty friendly group.*\n**You talk for a while but eventually they say the have to head off again. **")
        await channel.send("```(!) They give you a strange looking Chalice they found on their travels. ```")
    
async def Khanquest_takeHorseOfPower(channel, userID):
    print("talked to kazaks")
    
    #lose HorseOfPower
    conn = sqlite3.connect("gamedata.db")
    c = conn.cursor()
    c.execute("UPDATE itemsTbl SET HorseOfPower = 0 WHERE userID = ?", (userID,))
    conn.commit()
    conn.close()
    
    await channel.send("** You try approaching the horse of power and reach over to try to grab him. **")
    await channel.send("```(^) He runs away and you have no idea where he went. ```")
    await channel.send("** The Horse Of Power doesn't like greedy people.\nYou no longer have the Horse of Power by your side. **")
    

async def Khanquest_takeHorse(channel, userID):
    print("got horse")
    #got map
    conn = sqlite3.connect("gamedata.db")
    c = conn.cursor()
    c.execute("UPDATE itemsTbl SET Horse = 1 WHERE userID = ?", (userID,))
    conn.commit()
    conn.close()
    
    await channel.send("```(!) " + "You choose the sturdiest looking mount to take with you on your travels." + "```")

async def Khanquest_talkCartographer(channel, userID):
    print("talked to cartographer")
    #got map
    conn = sqlite3.connect("gamedata.db")
    c = conn.cursor()
    c.execute("UPDATE itemsTbl SET Map = 1 WHERE userID = ?", (userID,))
    conn.commit()
    conn.close()
    
    await channel.send("```(!) " + "You talked to the cartographer and he gave you a map of the area." + "```")

async def Khanquest_talkCommander(channel, userID):
    print("talked to commander")
    #got GuardShiftsPlanner
    conn = sqlite3.connect("gamedata.db")
    c = conn.cursor()
    
    planner = c.execute("SELECT GuardShiftsPlanner FROM itemsTbl WHERE userID = ?", (userID,)).fetchone()[0]
    
    if planner == 1: #already has it
        await channel.send("*You talk to the commander for a bit, and you talk about all of your grand exploits whilst conquering Mongolia*")
    else:
        c.execute("UPDATE itemsTbl SET GuardShiftsPlanner = 1 WHERE userID = ?", (userID,))
        await channel.send("```(!) " + "You talked to the commander and he gave you a long document containing the shift times for the wall guards." + "```")
        
    conn.commit()
    conn.close()
    
    
async def Khanquest_End(channel, userID):
    print("Khanquest end")
    
    #remove active game record
    conn = sqlite3.connect("ActiveGames.db")
    c = conn.cursor()
    c.execute('DELETE FROM ActiveGamesTbl WHERE Player = ?', (userID,))
    conn.commit()
    conn.close()
    
    conn2 = sqlite3.connect("gamedata.db")
    c2 = conn2.cursor()
    c2.execute('DELETE FROM itemsTbl WHERE userID = ?', (userID,))
    c2.execute('DELETE FROM roomTbl WHERE userID = ?', (userID,))
    conn2.commit()
    conn2.close()

    #delete game channel
    await channel.delete()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

async def Khanquest_help(channel, userID):
    print("Khanquest help")
    output = t2a(
    header=["Command", "Shortcut", "Does"],
    body=[["yes", "y", "(?) confirms"], ["North", "n", "Moves North"], ["South", "s", "Moves South"], ["East", "e", "Moves East"], ["West", "w", "Moves West"] ,["Look", "l", "Shows location"], ["Inventory", "i", "Shows inventory"], ["Map", "m", "Shows map"], ["end", "", "(?) ends game"], ["help", "h", "Shows this menu"]],
    first_col_heading=True
    )
    
    output2 = t2a(
    header=["Symbol", "Meaning"],
    body=[["(!)", "Item obtainable"], ["(?)", "Awaiting confirmation"], ["(~)", "Action requires item"], ["(>)", "moved to"]],
    first_col_heading=True
    )
    
    
    await channel.send("**Help:**\n.")
    await channel.send(f"**commands**:\n```{output}```")
    await channel.send(f"**symbols**:\n```{output2}```")
    
async def Khanquest_Map(channel, userID):
    print("Khanquest Map")
    conn = sqlite3.connect("gamedata.db")
    c = conn.cursor()
    map = c.execute("SELECT Map FROM itemsTbl WHERE userID = ?", (userID,)).fetchone()[0]
    conn.close()
    
    if map == 1: #has map
        await channel.send(file=discord.File('map.png'))
    else:
        await channel.send("**You do not have a map**")


async def Khanquest_Inventory(channel, userID):
    print("Khanquest Inventory")
    
    inventory = "``` | "
    
    #ID to item dict
    item_dict = {
        1 : "Map",
        2 : "Sword",
        3 : "Horse",
        4 : "Eagle Of Life",
        5 : "Horse Of Power",
        6 : "Chalice",
        7 : "Dagger Of Wisdom",
        8 : "Precious Jade",
        9 : "Guard Shifts Planner"
    }
    
    conn = sqlite3.connect("gamedata.db")
    c = conn.cursor()
        
    for id, item in enumerate(c.execute("SELECT * FROM itemsTbl WHERE userID = ?", (userID,)).fetchone()):
        
        if item == 1: #player has
            inventory = inventory + item_dict[id] + " | "
    
    inventory = inventory + "```"
    
    conn.close()
    
    await channel.send("**Inventory:**")
    await channel.send(inventory)
    
async def Khanquest_look(channel, userID):
    print("Khanquest look")
    name = "```" + Khanquest_currRoom(userID).name + ": " + "```"
    await channel.send(name)
    await channel.send("*" + Khanquest_currRoom(userID).lookStr + "*")
    
    await Khanquest_lookAction(userID, channel)
    

#~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|~|


#Announce
@client.command(name = "Announce", description="make an announcement")
async def Announce(ctx, arg):
    print("Announce")
    await ctx.message.delete()
    
    channel = ctx.message.channel
    
    message1 = f"📢📢**Announcement:**📢📢"
    message2 = f"||<@everyone>|| \n\n ```{arg}```"
    await channel.send(message1)
    await channel.send(file=discord.File('mongol_flag.png'))
    await channel.send(message2)
    
#private say
@client.command(name = "private_say", description="say something anonymously")
async def private_say(ctx, arg):
    print("private_say")
    await ctx.message.delete()
    
    message = f"**Anonymous message:**\n```{arg}```"
    await ctx.message.channel.send(message)

#play Khanquest
@client.command(name = "Khanquest", description="play Khanquest II")
async def Khanquest(ctx):
    print("Khanquest")

    await KhanquestNew(ctx)#start new Khanquest
    
              #  prevent custom reactions | Only allow one reaction (?) | Give mongol of the week role | Say who did most mongol thing this week | The <@Mongol of the week> is:

async def MOTWAnnounce():
    print("Mongol of the Week Announced")
    #get messageID
    conn = sqlite3.connect('MOTW.db')
    cur = conn.cursor()
    msgID = cur.execute('SELECT messageID FROM mongolTable WHERE ID = 0').fetchone()[0]

    msg = await general_channel.fetch_message(msgID)
    most_voted = str(max(msg.reactions, key = lambda r: r.count).emoji)
    
    count = emoji.demojize(most_voted)
    count = int(count.strip(":").strip("keycap_")) #remove emoji : | remove: keycap_
    
    Mongol_user = cur.execute('SELECT userID FROM UsersTable WHERE ID = ?', (count,)).fetchone()[0]
    
    #role
    user = guild.get_member(Mongol_user)
    print(user)
    role = discord.utils.get(guild.roles, name="Mongol Of The Week")
    
    #remove all previous roles
    for m in guild.members:
        try:
            await m.remove_roles(role)
        except:
            pass
    
    #assign new role
    await user.add_roles(role)

    MOTW_msg = f"**||<@everyone>|| \nHappy Mongol Monday! \nhttps://www.youtube.com/watch?v=1_oHK2fzGe8\n\n*The {role.mention} is:* \n <@{int(Mongol_user)}>**"
    await msg.reply(MOTW_msg)
    
    conn.commit()
    conn.close()

async def MOTWVote():
    print("Mongol of the Week Voting opened")

    #clear prev users table
    conn = sqlite3.connect('MOTW.db')
    cur = conn.cursor()
    cur.execute('DELETE FROM UsersTable')
    conn.commit()
    conn.close()

    count =  0
    users = ""

    for guild in client.guilds:         #get members
        for member in guild.members:
            if not member.bot: #not a bot
                count += 1 #keep count of how many users for reactions
                users = users + "\t" + str(count) + ". " + str(member.name)
                
                #store users for results
                conn = sqlite3.connect('MOTW.db')
                cur = conn.cursor()
                cur.execute('INSERT INTO UsersTable ("ID", "userID") VALUES (?,?)', (count, member.id,))
                conn.commit()
                conn.close()

    pollmsg = f"**||<@everyone>|| \nPut in your votes:\nWho is this week's *Mongol Of The Week?***" + "\n\n```" + str(users) + "```"
    msg = await general_channel.send(pollmsg)

    #store message id for results
    conn = sqlite3.connect('MOTW.db')
    cur = conn.cursor()
    cur.execute('UPDATE mongolTable SET messageID = ? WHERE ID = 0', (msg.id,))
    conn.commit()
    conn.close()

    for i in range(count):
        await msg.add_reaction(num_emojis[i])

#Mongol OTW    
@tasks.loop(minutes=60.0)       #mongol of the week - 7pm to 9pm  ->  mongol monday announces mongol of the week  ->  vote on sunday, announced on monday
async def MongolOTW():           #mongolOfTheWeek
    if datetime.datetime.today().weekday() == 6: # 6 = Sunday
        if datetime.datetime.now().hour == 8:  #if datetime.now().hour == 8:
            await MOTWVote()
            
    if datetime.datetime.today().weekday() == 0: # 0 = Monday - Get results
        if datetime.datetime.now().hour == 8:
            await MOTWAnnounce()
          

#create table          
async def createTable(ctx):
    conn = sqlite3.connect('ActiveGames.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE ActiveGamesTbl(
                            ChannelID INT PRIMARY KEY,
                            Player INT
            ); """)
    conn.commit()
    conn.close()
    await ctx.reply("succesfull")
    
    
#trivia
@client.command(name = "IGCSE_Trivia", description="trivia for IGCSE subjects: physics, chemistry, biology")
async def IGCSE_Trivia(ctx, subject = None):
    print("IGCSE TRIVIA")
    channel = ctx.message.channel
    
    if not subject:
        await ctx.message.reply("**no valid category was supplied, use:**\n```IGCSE_Trivia categories```\nto see all avaliable categories")
        return
    
    #physics questions
    physics = {
        #   "question" : ["answer"],
        "Formula for power" : ["P = W/t", "W/t", "Power = work done / time"],
        "Formula for Density (rho = p)" : ["p = m/v", "m/v", "density = mass/volume", "mass/volume"],
        "unit for density" : ["kg/m3", "g/cm3"],
        "Formula for velocity" : ["v = s/t", "s/t", "velocity = distance/time", "velocity = displacement/time", "distance/time", "displacement/time"],
        "What is the relationship between Pressure * Volume for a fixed mass of gas at constant temperature" : ["constant", "they are constant", "P*V = constant", "P1*V1 = P2*V2", "Pressure * voltage is constant", "Pressure times voltage is constant"],
        "K = *C + x; x=?" : ["273", "273 degrees"],
        "Formula for Voltage (Ohm's Law)" : ["V = I*R", "I*R", "Current * resistance", "Voltage = current * resistance"],
        "Formula for Impulse in terms of Force" : ["I = F*t", "F*t", "Impulse = Force * time", "Force * time"],
        "Formula for Impulse in terms of momentum" : ["I = m*v-m*u", "m*v-m*u", "change in momentum", "Impulse = change in momentum"],
        "Formula for Voltage in a transformer in terms of numbers of turns in the coils" : ["Vp/Vs = Np/Ns", "Voltage in primary coil/Voltage in secondary = Number of turns of primary coil / Number of turns of secondary coil"],
        "Formula for Weight" : ["W = m*g", "m*g", "Weight = mass * gravitational potential"],
        "a = ?" : ["v-u/t", "(change in v)/t"],
        "(Pressure) P = ?" : ["F/A", "Force / Area"],
        "Hookes Law" : ["F = k*x", "F = x*k", "Force = extension * spring constant", "Force = spring constant * extension"],
        "Newton's Second Law of Motion" : ["F = m*a", "Force = mass * acceleration"],
        "I = ?" : ["Q/t", "charge / time"],
        "V = ? in Electricity and Magnetism" : ["W/Q", "Work done / charge"],
        "Electromotive Force = ?" : ["W/Q", "Work done / charge", "Voltage", "V"],
        "Energy Change in thermal physics (0 = change in temperature)" : ["E = m*c*0", "Energy = mass*specific heat capacity*change in temperature"],
        "In a Parallel Circuit total Current = ?" : ["I1 + I2", "Current 1 + Current 2"],
        "In a Parallel Circuit total Voltage = ?" : ["V1 = V2", "Voltage 1 = Voltage 2"],
        "In a Parallel Circuit what is the formula for total resistance" : ["1/R total = 1/R1 + 1/R2", "1/R tot = 1/R1 + 1/R2", "1/total R = 1/R1 + 1/R2", "1/total resistance = 1/resistance 1 + 1/resistance 2"],
        "In a Series Circuit total Current = ?" : ["I1 = I2", "current 1 = current 2"],
        "In a Series Circuit total Voltage across the supply = ?" : ["V1 + V2", "voltage 1 + voltage 2"],
        "In a Series Circuit total Resistance = ?" : ["R1 + R2", "resistance 1 + resistance 2"],
        "Formula for Current and Voltage across a Transformer" : ["Ip * Vp = Is * Vs", "Current in primary * Voltage in primary = current in secondary * voltage in secondary"],
        "Formula for Power loss in cables" : ["P = I2 * R", "I2 * R", "current^2 * resistance", "Power = current^2 * resistance"],
        "Approximate diameter of the Milky Way" : ["100 000 light years", "100 000 light-years", "100 000"],
        "Approximate for Hubble's constant" : ["2.2*10^-18"],
        "Hubble's constant formula" : ["H0 = v/d"],
        "Approximate for speed of light in a vaccuum" : ["3*10^8", "3.0*10^8"],
        "Approximate for speed of light in air" : ["3*10^8", "3.0*10^8"],
        "Moment formula" : ["Moment = F * perpendicular distance to the pivot", "F * perpendicular distance to the pivot", "F*d", "Force times perpendicular distance from the pivot", "perpendicular distance from the pivot times Force"],
        "Momentum formula" : ["p = m*v"],
        "Formula for a reflection" : ["i = r"],
        "Snell's law (Formula for a refraction)" : ["ni * sin i = nr * sin r", "n = sin i / sin r"],
        "Formula for Work Done" : ["W = F*d"],
        "Equation for two resistors used as a potential divider" : ["R1 / R2 = V1 / V2", "resistance 1 / resistance 2 = voltage 1 / voltage 2"],
        "Change in pressure beneath surface of a liquid" : ["P = h*p*g"],
        "When fully charged, the battery can deliver a power of 600W for 60min. Calculate the energy, in joules, stored in the battery when fully charged." : ["2 200 000 J", "2 200 000"],
        "What form of energy is stored in a battery" : ["chemical", "chemical energy"],
        "A 2.0kg object is released from rest and accelerates at 4.0m/s2. Calculate the resultant force acting on the 2.0kg object." : ["8.0 N", "8", "8N", "8.0"],
        "The mass of a canoeist is 65kg. Calculate her kinetic energy when travelling on still water at 2.5m/ s" : ["200J", "200"],
        "State one feature of a liquid-in-glass thermometer that are necessary for linearity." : ["bore of constant (cross sectional) area", "(liquid has) constant thermal expansion"],
        "What type of waves are sound waves?" : ["longitudinal", "longitudinal waves"],
        "What is a similary between visible light and radio waves?" : ["transverse", "transverse waves"],
        "on a circuit, what is a triangle shape" : ["diode", "a diode"],
        "Two resistors of resistance 2.0Ω and 3.0Ω are connected in parallel. Calculate the combined resistance of the resistors in this arrangement." : ["1.2", "1.2 ohms"],
        "Two resistors of resistance 2.0Ω and 3.0Ω are connected in parallel to a socket of output 12 V. Calculate the combined current in this arrangement." : ["2.4", "2.4 A"],
        "Unit for current" : ["A", "ampere"],
        "Unit for Charge" : ["C", "coulomb"],
        "Unit for Work Done" : ["J"],
        "Unit for Energy transferred" : ["J"],
        "Unit for resistance" : ["Ω", "ohms", "ohm", "omega", "Oméga"],
        "Symbol for specific heat capacity" : ["c"],
        "Symbol for current" : ["I"],
        "Symbol for Charge" : ["Q"],
        "Symbol for Work Done" : ["W"],
        "Symbol for resistance" : ["R"]
    }
    
    #chem questions
    chemistry = {
        #   "question" : "answer",
        "Volume occupied by one mole of gas" : ["24dm3"]
    }
    
    #bio questions
    biology = {
        #   "question" : "answer",
        "Artery leading to the heart" : ["coronary artery", "coronary"],
        "Which chamber of the heart pumps blood at the highest pressure?" : ["left ventricle"]
    }
    
    global questions
    
    match (subject):
        case "categories":
            await channel.send(f"```physics: {len(physics)}, chemistry: {len(chemistry)}, biology: {len(biology)}```")
            return
        case "physics":
            questions = physics
        case "phys":
            questions = physics
        case "chemistry":
            questions = chemistry
        case "chem":
            questions = chemistry
        case "biology":
            questions = biology
        case "bio":
            questions = biology
        case _:
            await channel.send("**does not have that subject**")
            return
        
    
    await channel.send("**Trivia starting...**")
        
    await triviaQuestion(channel)
    
async def triviaQuestion(channel):
    global trivia_question
    
    trivia_question = random.choice(list(questions.items()))
    await channel.send("```Q: " + trivia_question[0] + "```")


#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

client.run(TOKEN)
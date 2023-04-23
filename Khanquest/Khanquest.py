import time
import sqlite3
import InitialiseSQL
import discord
from dotenv import load_dotenv
import os
from discord.ext import commands
import sys

async def KhanquestRun(channel):
    print("Running Khanquest")
    conn = sqlite3.connect("gamedata.db")
    c = conn.cursor()

    # rooms
    DesertRooms = ["Nothing", "Snake", "Bandits", "Yurt", "Eagles", "Snow Leopard", "Kazaks", "Horse", "Chalice", "Mongols", "Large Rocks" ,"Forbidden Yurt"]
    # Init gamedata
    room = [(2,0)] #y, x
    items = [(0,"Map"), (1,"Sword"), (2,"Horse"), (3,"Eagle of Life"), (4,"Horse of Power")]
    player_items = [(0,"Map")]



        #load gamedata

    #Current Room
    InitialiseSQL.init(db ="gamedata.db", crtTbl="""CREATE TABLE roomTbl(
                            y INT,
                            x INT
            ); """, initTblVals=room, InsrtCmd = "INSERT INTO roomTbl VALUES (?,?)")

    #Available items
    InitialiseSQL.init(db ="gamedata.db", crtTbl="""CREATE TABLE itemsTbl(
                            ID INT PRIMARY KEY,
                            item TEXT
            ); """, initTblVals=items, InsrtCmd = "INSERT INTO itemsTbl VALUES (?,?)")

    #Inventory items
    InitialiseSQL.init(db ="gamedata.db", crtTbl="""CREATE TABLE inventoryTbl(
                            ID INT PRIMARY KEY,
                            item TEXT
            ); """, initTblVals=player_items, InsrtCmd = "INSERT INTO inventoryTbl VALUES (?,?)")

    # load gamedata
    a = c.execute("SELECT * FROM roomTbl").fetchone()
    room = a #(y,x)
    items = c.execute("SELECT * FROM itemsTbl").fetchone()
    player_items = c.execute("SELECT * FROM inventoryTbl").fetchone()


    #get current room
    def currRoom():
        return rooms[room[0]][room[1]]

    #rooms()
    class new_room:
        def __init__(self, name, lookStr, items):
            self.name = name
            self.lookStr = lookStr
            self.items = items

    room00 = new_room("City", "Your empire city lies before you", "Nothing in this room")
    room02 = new_room("Stables", "These are the Horses Stables, horses of all kind are lined up. Sullymen would love this place.", "Nothing in this room")
    room10 = new_room("Palace Court", "The Palace Court lies in front of you, with people scuttering about, bowing to you as they see you. Large gates extend in front, below the stairs.", "Nothing in this room")
    room11 = new_room("The Wall", "There is a tall stone wall in front of you, you could try to climb it, but you would need to speak to your commander to release the guards from position first.", "Nothing in this room")
    room12 = new_room("Great Field", "A large field with brownish grass, not many people are here.", "Nothing in this room")
    room13 = new_room("Gobi Desert", "Vast expanses of desert, extending beyond view", "Nothing in this room")
    room20 = new_room("Room", "This is a smaller room, with a large bed taking up most of the center of the room.", "Nothing in this room")
    room30 = new_room("Throne Room", "There is a large room, not too wide but with a carpet extending beyond view. At the end, a large wooden Throne with ornate decorations can be seen.", "Nothing in this room")
    #room00 = new_room("name", "look", "Nothing in this room")
    #print(room48.name, room48.lookStr, room48.items)


    #define rooms
    rooms = [[room00, "", room02],[room10, room11, room12, room13], [room20] , [room30]] #rooms [y][x] | s=[0][x], n=[3][x], e=[x][1], w=[0]

    #commands

    #Look
    async def look():
        await channel.send(currRoom()("look"))

    #Inventory
    async def Inventory():
        await channel.send("Inventory Items: ", player_items)

    #Map
    async def Map():
        await channel.send("Map")

    #Move 
    async def move(dir):
        if len(dir) > 1:
                dir = dir[0]

        global room
        tempRoom = room[:]
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
                room = tempRoom
                await channel.send("moved to: "+ currRoom()("name"))
            else:
                await channel.send("Can't go there")
        except:
            await channel.send("Can't go there")

    #register the given action
    async def registerAction():
        #ask for action and format it
        actn = input("\n:").lower()

        #check for movement
        directions = ["n","s","e","w", "north", "south", "east", "west"]
        if actn in directions:
            await move(actn)

        #check for other commands
        elif actn == "look" or actn == "l": #look
            look()
        elif actn == "inventory" or actn == "i": #inventory
            Inventory()
        elif actn == "map" or actn == "m": #map
            Map()

        #No valid command
        else:
            await channel.send("Invalid command")


    #Start game
    async def start():
        # Title ASCII Art
        await channel.send("""```
        _   ___                                       _       _____ _           ______         _     _     _     _             __   __         _   
        | | / / |                                     | |  _  |_   _| |          |  ___|       | |   (_)   | |   | |            \ \ / /        | |  
        | |/ /| |__   __ _ _ __   __ _ _   _  ___  ___| |_(_)   | | | |__   ___  | |_ ___  _ __| |__  _  __| | __| | ___ _ __    \ V /   _ _ __| |_ 
        |    \| '_ \ / _` | '_ \ / _` | | | |/ _ \/ __| __|     | | | '_ \ / _ \ |  _/ _ \| '__| '_ \| |/ _` |/ _` |/ _ \ '_ \    \ / | | | '__| __|
        | |\  \ | | | (_| | | | | (_| | |_| |  __/\__ \ |_ _    | | | | | |  __/ | || (_) | |  | |_) | | (_| | (_| |  __/ | | |   | | |_| | |  | |_ 
        \_| \_/_| |_|\__,_|_| |_|\__, |\__,_|\___||___/\__(_)   \_/ |_| |_|\___| \_| \___/|_|  |_.__/|_|\__,_|\__,_|\___|_| |_|   \_/\__,_|_|   \__|
                                    | |                                                                                                             
                                    |_|                                                                                                             
        ```
        **K H A N Q U E S T **
        *The Forbidden Yurt*
        """)

        # Introduction
        await channel.send("Welcome to Khanquest: The Forbidden Yurt")
        await channel.send("You are Genghis Khan, the Emperor of the Mongol Empire")
        await channel.send("Your goal is to find the forbidden Yurt and retrieve the Eagle of Life and the Horse of Power")
        await channel.send("You wake up in your room on your royal bed, your journey begins...")
        
        if (currRoom().name == "Gobi Desert"):      #change this to Forbidden Yurt later
            #game ended
            await registerAction()

    #run start
    await start()

    print("Game ended")

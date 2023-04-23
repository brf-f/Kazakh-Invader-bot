import time
import sqlite3
import InitialiseSQL

conn = sqlite3.connect("gamedata.db")
c = conn.cursor()

def print_slow(str):
    typeSpeed = 0.04
    if len(str) > 1000:
        typeSpeed = (1*(10**-40))

    for letter in str:
        print(letter, end='')
        time.sleep(typeSpeed)
    print('')


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
#room City
def room00(roomActn):
    name = "City"
    lookStr = "Your empire city lies before you"

    match roomActn:
        case "name":
            return name
        case "look":
            return lookStr
#room Stables
def room02(roomActn):
    name = "Stables"
    lookStr = "These are the Horses Stables, horses of all kind are lined up. Sullymen would love this place."

    match roomActn:
        case "name":
            return name
        case "look":
            return lookStr

#room Palace Court
def room10(roomActn):
    name = "Palace Court"
    lookStr = "The Palace Court lies in front of you, with people scuttering about, bowing to you as they see you. Large gates extend in front, below the stairs."

    match roomActn:
        case "name":
            return name
        case "look":
            return lookStr
#room The Wall
def room11(roomActn):
    name = "The Wall"
    lookStr = "There is a tall stone wall in front of you, you could try to climb it, but you would need to speak to your commander to release the guards from position first."

    match roomActn:
        case "name":
            return name
        case "look":
            return lookStr
#room Great Field
def room12(roomActn):
    name = "Great Field"
    lookStr = "A large field with brownish grass, not many people are here."

    match roomActn:
        case "name":
            return name
        case "look":
            return lookStr
#room Gobi Desert
def room13(roomActn):
    name = "Gobi Desert"
    lookStr = "Vast expanses of desert, extending beyond view"

    match roomActn:
        case "name":
            return name
        case "look":
            return lookStr

#room Room
def room20(roomActn):
    name = "Room"
    lookStr = "This is a smaller room, with a large bed taking up most of the center of the room."

    match roomActn:
        case "name":
            return name
        case "look":
            return lookStr

#room Throne Room
def room30(roomActn):
    name = "Throne Room"
    lookStr = "There is a large room, not too wide but with a carpet extending beyond view. At the end, a large wooden Throne with ornate decorations can be seen."

    match roomActn:
        case "name":
            return name
        case "look":
            return lookStr


#define rooms
rooms = [[room00, "", room02],[room10, room11, room12, room13], [room20] , [room30]] #rooms [y][x] | s=[0][x], n=[3][x], e=[x][1], w=[0]

#commands

#Look
def look():
    print_slow(currRoom()("look"))

#Inventory
def Inventory():
    print_slow("Inventory Items: ", player_items)

#Map
def Map():
    print_slow("Map")

#Move 
def move(dir):
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
            print_slow("moved to: "+ currRoom()("name"))
        else:
            print_slow("Can't go there")
    except:
        print_slow("Can't go there")

#register the given action
def registerAction():
    #ask for action and format it
    actn = input("\n:").lower()

    #check for movement
    directions = ["n","s","e","w", "north", "south", "east", "west"]
    if actn in directions:
        move(actn)

    #check for other commands
    elif actn == "look" or actn == "l": #look
        look()
    elif actn == "inventory" or actn == "i": #inventory
        Inventory()
    elif actn == "map" or actn == "m": #map
        Map()

    #No valid command
    else:
        print_slow("Invalid command")


#Start game
def start():
    # Title ASCII Art
    print_slow("""
     _   ___                                       _       _____ _           ______         _     _     _     _             __   __         _   
    | | / / |                                     | |  _  |_   _| |          |  ___|       | |   (_)   | |   | |            \ \ / /        | |  
    | |/ /| |__   __ _ _ __   __ _ _   _  ___  ___| |_(_)   | | | |__   ___  | |_ ___  _ __| |__  _  __| | __| | ___ _ __    \ V /   _ _ __| |_ 
    |    \| '_ \ / _` | '_ \ / _` | | | |/ _ \/ __| __|     | | | '_ \ / _ \ |  _/ _ \| '__| '_ \| |/ _` |/ _` |/ _ \ '_ \    \ / | | | '__| __|
    | |\  \ | | | (_| | | | | (_| | |_| |  __/\__ \ |_ _    | | | | | |  __/ | || (_) | |  | |_) | | (_| | (_| |  __/ | | |   | | |_| | |  | |_ 
    \_| \_/_| |_|\__,_|_| |_|\__, |\__,_|\___||___/\__(_)   \_/ |_| |_|\___| \_| \___/|_|  |_.__/|_|\__,_|\__,_|\___|_| |_|   \_/\__,_|_|   \__|
                                | |                                                                                                             
                                |_|                                                                                                             
    K H A N Q U E S T 
    The Forbidden Yurt
    """)

    # Introduction
    print_slow("Welcome to Khanquest: The Forbidden Yurt")
    print_slow("You are Genghis Khan, the Emperor of the Mongol Empire")
    print_slow("Your goal is to find the forbidden Yurt and retrieve the Eagle of Life and the Horse of Power")
    print_slow("You wake up in your room on your royal bed, your journey begins...")
    
    while not (currRoom()("name") == "Gobi Desert"):      #change this to Forbidden Yurt later
        #get action
        registerAction()

#run start
start()

print("Game ended")
import asyncio
from secrets import randbelow

from discord import client
from discord.ext import commands

bot = commands.Bot(command_prefix='?')

wPeople = []

initialised = False
gameInSession = False

NUM_OF_ROLES = 4
ROLE_WW = 1
ROLE_VILL = 2
ROLE_SEER = 3
ROLE_TANNER = 4

ww = 0
vil = 0
see = 0
tan = 0


class Player:
    id = ""
    role = ""

    def __init__(self, id):
        self.id = id

    def getID(self):
        return self.id

    def setRole(self, role):
        self.role = role

    def getRole(self):
        return self.role


@bot.event
async def on_ready():
    print('~~~~~~')
    print(bot.user.name)
    print(bot.user.id)
    print('~~~~~~')


@bot.event
async def on_message(data):
    message = getMessage(data)

    if message[0:1] == "?":
        print("Data received: " + message)

        temp = ""
        if len(message.split(" ")) > 0:
            message = message.split(" ")[0]

        try:
            temp = command(message)
        except:
            temp = command("")

        response = globals()[temp](data)

        await data.channel.send(response)


def sendMessageToUser(ID, msg):
    user = bot.get_user(ID)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(sendMessage(user, msg))


async def sendMessage(user, msg):
    await user.send(msg)


def helpMessage(data):
    return "I am a simple bot which does stuff like say '!Hello " + data.author.name + "'"


def errorMessage(data):
    return "i'm sorry " + data.author.name + " i'm afraid i can't do that"


def werewolf(data):
    global gameInSession
    global initialised
    global wPeople

    message = getMessage(data)
    try:
        message = message.split(" ")[1]
    except:
        message = "help"

    response = "Error"

    if not gameInSession:
        if message == "start":
            if not initialised:
                wPeople = []
                wRoles = []
                response = "Game initialised, run again to start"
                initialised = True
            else:
                gameInSession = True
                startWWGame()

        if initialised:
            if message == "join":
                ID = data.author.id
                if ID not in wPeople:
                    player = Player(ID)
                    wPeople.append(player)
                    response = data.author.name + " has joined!"
                    x = sendMessageToUser(ID, "OI")
                else:
                    response = data.author.name + " has already joined the game!"

            if message == "leave":
                ID = data.author.id
                if ID in wPeople:
                    wPeople.remove(ID)
                    response = data.author.name + " has left the game!"
                else:
                    response = data.author.name + " isn't playing!"

            if message == "who":
                response = ""
                for peep in wPeople:
                    response += str(peep.getID()) + " "

    else:
        print("hi")
        # commands during the game

    if message == "end":
        initialised = False
        gameInSession = False
        wPeople = []
        response = "Game ended"

    if message == "help":
        response = "Thank you for using this, heres a list of commands..."

    if message == 'test1':
        player = Player("1")
        wPeople.append(player)
        player = Player("2")
        wPeople.append(player)
        player = Player("3")
        wPeople.append(player)
        player = Player("4")
        wPeople.append(player)
        player = Player("5")
        wPeople.append(player)

    if message == 'test2':
        response = ""
        for peep in wPeople:
            response += str(peep.getID()) + " " + str(peep.getRole()) + "\n"

    return response


def startWWGame():
    res = setupRoles()
    print(res)


def setupRoles():
    global wPeople
    global ww, see, tan, vil
    num = len(wPeople)
    ww = 0
    vil = 0
    see = 0
    tan = 0

    if num <= 5:
        ww = 1
        see = 1
        vil = num - (ww + see)
    else:
        tempWW = int(num / 5)
        if tempWW > 2:
            ww = tempWW
        else:
            ww = 2

        see = 1
        tan = 1
        vil = num - (ww + see + tan)

    for peep in wPeople:
        assignRole(peep)

    return "Roles setup"


def assignRole(peep):
    global ww, see, tan, vil
    rand = randbelow(NUM_OF_ROLES) + 1

    if rand == 1 and ww > 0:
        ww -= 1
        peep.setRole(rand)

    elif rand == 2 and see > 0:
        see -= 1
        peep.setRole(rand)

    elif rand == 3 and tan > 0:
        tan -= 1
        peep.setRole(rand)

    elif rand == 4 and vil > 0:
        vil -= 1
        peep.setRole(rand)

    if peep.getRole() == "":
        peep = assignRole(peep)

    return peep


def command(x):
    return {
        "?help": "helpMessage",
        "?ww": "werewolf",
        "?werewolf": "werewolf",
        "": "errorMessage",
    }[x]


def getMessage(data):
    return data.content.lower().strip()


f = open('token.txt', 'r')
token = f.read()
bot.run(token)

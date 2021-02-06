import sprite
import pygame
import grid
import time
import random as r
import asyncio
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_w,
    K_s,
    K_a,
    K_d,
    KEYDOWN,
    QUIT,
    K_f
)

import farm_client

import google.protobuf.json_format as json_format

import os

sprite.init(inputFont="Minecraft")

screen = sprite.setScreen(1440, 760)
player = sprite.Player(screen, (255,255,255), 50, 0, 0, False, 5)
player.realX = player.x
player.realY = player.y
scrollX = 0
scrollY = 0
Map = grid.Grid(100,100)
lock = 0
Itemlock = 0
Playerlock = 0
PlayerSendlock = 0
name = os.environ.get("USER")
hotbarSlot = sprite.newImage('pointer.png')
yellowPointer = sprite.newImage('yellowPointer.png')
selectedSlot = 1
Items = []
Players = []
pygame.display.set_caption("Farming Game")
blockIDs = {
    1: 'Plantgrass',
    2: 'bush',
    3: 'soil',
    4: 'path',
    5: 'grass',
    6: 'tallGrass',
    7: 'lettuce'
}
plantsTag = [1,2,7]
plantTimes = [5000,5000,1]
plantStages = [5,2,2]
class Block():
    def __init__(self,ID, lvl=1):
        self.ID = ID
        self.lvl = lvl
        if self.ID in plantsTag:
            self.ticks = plantTimes[plantsTag.index(self.ID)]
        else:
            self.ticks = 0
        self.ticksfromstart = 0
    def tick(self):
        global plantStages
        if self.ticks != 0:
            self.ticksfromstart += 1
            if self.ticksfromstart % self.ticks == 0:
                if self.lvl < plantStages[plantsTag.index(self.ID)]:
                    if r.randint(0,100) == 0:
                        self.lvl += 1
                    else:
                        self.ticksfromstart -= 1
class DroppedItem():
    def __init__(self,x,y,ID, degrees=r.randint(0,360)):
        self.x = x
        self.y = y
        self.degrees = degrees
        self.ID = ID
        #print("x:", self.x, "y:", self.y)
    def pickUp(self):
        done = False
        for i in range(8):
            if isinstance(inventory[i+1], Item):
                if inventory[i+1].ID == self.ID:
                    inventory[i+1].count += 1
                    done = True
                    break
        if done == False:
            for i in range(8):
                if inventory[i+1] == 0:
                    inventory[i+1] = Item(self.ID, 1)
                    break

class Player():
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

            
scrollX = 0
scrollY = 0

itemIDs = {
    1: "grassSeeds",
    2: "hoe",
    3: 'berrySeeds',
    4: 'lettuce'

}
def GetMapAsync():
    global lock
    if lock != 1:
        lock += 1
        farm_client.GetMapAsync().add_done_callback(getMapCallBack)

def GetPlayersAsync():
    global Playerlock
    if Playerlock != 1:
        Playerlock += 1
        farm_client.GetPlayersAsync().add_done_callback(getPlayersCallBack)

def SendPlayerAsync():
    global PlayerSendlock
    if PlayerSendlock != 1:
        PlayerSendlock += 1
        farm_client.SendPlayerAsync(Player(name, int(player.x-scrollX), int(player.y-scrollY))).add_done_callback(SendPlayerCallBack)

def getMapCallBack(f):
    global lock
    lock -= 1
    setUpMap(f.result())

def getPlayersCallBack(f):
    global Playerlock
    Playerlock -= 1
    setUpPlayers(f.result())

def SendPlayerCallBack(f):
    global PlayerSendlock
    PlayerSendlock -= 1

def setUpPlayers(inputList):
    global Players
    #print('input list', inputList)
    Players = inputList.player
    #for player in inputList:
    #    Players.append(Player(player.name, player.x, player.y))
        #print('x:', inputList.item[i].x, 'y:', inputList.item[i].y)
    #print("Items:", Items)
    return Players

def getItemCallBack(f):
    global Items
    global Itemlock
    Itemlock -= 1
    Items = setUpItems(f.result())

def GetMapSync():
    result = farm_client.GetMapSync()
    setUpMap(result)

def GetItemsAsync():
    global Itemlock
    if Itemlock != 1:
        Itemlock += 1
        farm_client.GetItemsAsync().add_done_callback(getItemCallBack)

def DeleteItemAsync(Item):
    farm_client.DeleteItemAsync(Item).add_done_callback(DeleteItemCallBack)

def DeleteItemCallBack(future):
    result = future.result()
    DroppedItem(result.x, result.y, result.ID).pickUp()

def changeMap(r, c, changeto):#Async
    #print('r:', r, 'c:', c)
    Map.change(r, c, changeto)
    farm_client.ChangeStuffAsync(farm_client.farmServerMethods_pb2.MapUpdate(r=r,c=c, changedto=farm_client.farmServerMethods_pb2.Block(ID=changeto.ID, Lvl=changeto.lvl))).add_done_callback(lambda f: print("got changed block"))

class Item():
    def __init__(self, ID, count):
        global itemIDs
        self.ID = ID
        self.count = count
        if itemIDs[self.ID] != 'hoe':
            self.tool = False
        else:
            self.tool = True
    def used(self):
        if self.tool == False:
            self.count -=1



blockTextures = {
    'Plantgrass1': sprite.newImage('plantGrass1.png'),
    'Plantgrass2': sprite.newImage('plantGrass2.png'),
    'Plantgrass3': sprite.newImage('plantGrass3.png'),
    'Plantgrass4': sprite.newImage('plantGrass4.png'),
    'Plantgrass5': sprite.newImage('plantGrass5.png'),
    "grass": sprite.newImage('grass.png'),
    'bush1': sprite.newImage('bush1.png'),
    'bush2': sprite.newImage('bush2.png'),
    "path": sprite.newImage('path.png'),
    'soil': sprite.newImage('soil.png'),
    'tallGrass': sprite.newImage('tallGrass.png'),
    'lettuce1': sprite.newImage('lettuce1.png'),
    'lettuce2': sprite.newImage('lettuce2.png')
}

entityImages = {
    1: sprite.newImage("Entity.png")
}


inventory = {
    1: Item(2,1),
    2: Item(4,5),
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 0
}



itemImages = {
    'grassSeeds': sprite.newImage('grassSeeds.png'),
    'hoe': sprite.newImage('hoe.png'),
    'berrySeeds': sprite.newImage('berrySeeds.png'),
    'lettuce': sprite.newImage('lettuceItem.png')
}

def setUpMap(inputMap):
    global Map
    local_map = grid.Grid(100,100)
    local_map.list = []
    for i in range(len(inputMap.block)):
        local_map.list.append(Block(inputMap.block[i].block.ID, inputMap.block[i].block.Lvl))
    #print('done setting up map for {} blocks'.format(len(inputMap.block)))
    Map = local_map
    return Map

def setUpItems(inputList):
    Items = []
    for i in range(len(inputList.item)):
        Items.append(DroppedItem(inputList.item[i].x, inputList.item[i].y, inputList.item[i].ID))
        #print('x:', inputList.item[i].x, 'y:', inputList.item[i].y)
    #print("Items:", Items)
    return Items

def drawHotbar():
    for x in range(9):
        pointer = sprite.Player(screen, (255,255,255), 50, 50, 25, False, 0)
        if selectedSlot == x+1:
            pointer.image = yellowPointer
        else:
            pointer.image = hotbarSlot
        pointer.x = (x*50)+25
        pointer.update()
        if inventory[x+1] != 0:
            pointer.image = itemImages[itemIDs[inventory[x+1].ID]]
            pointer.update()
            if inventory[x+1].tool == False:
                sprite.text(str(inventory[x+1].count), (x*50)+25,25)
    if inventory[selectedSlot] != 0:
        pointer.image = itemImages[itemIDs[inventory[selectedSlot].ID]]
        pointer.x = player.x
        pointer.y = player.y
        Mx, My = pygame.mouse.get_pos()
        direction = sprite.getDirection((pointer.x, pointer.y), (Mx, My))
        pointer.direction = direction
        pointer.step(50)
        pointer.update()
    changeHotbar()


def changeHotbar():
    global selectedSlot
    keys = sprite.getKeys()
    numberKeys = [
        pygame.K_1,
        pygame.K_2,
        pygame.K_3,
        pygame.K_4,
        pygame.K_5,
        pygame.K_6,
        pygame.K_7,
        pygame.K_8,
        pygame.K_9

    ]
    i = 0
    for key in numberKeys:
        i += 1
        if keys[key]:
            selectedSlot = i

def drawBackground():
    global blockIDs
    image = sprite.Sprite(screen, (0,0,0), 50,0,0)
    sprite.setBackground((255,255,255))
    for R in range(Map.numRows):
        for C in range(Map.numCols):
            image.x = C*50+25-scrollX
            image.y = R*50+25-scrollY
            if image.x > -50 and image.x < 1490 and image.y > -50 and image.y < 810:
                #image = sprite.Sprite(screen, (0,0,0), 50,0,0)
                #print(Map.get(R,C))
                #print(len(Map.list))
                #print((((round(C))*Map.numCols))+(round(R)))
                if Map.get(R,C).ticks != 0:
                    image.image = blockTextures[str(blockIDs[Map.get(R,C).ID])+str(Map.get(R,C).lvl)]
                else:
                    image.image = blockTextures[blockIDs[Map.get(R,C).ID]]
                image.updateImage()
                #sprite.text("R: " + str(R) + " C: " + str(C), image.x-25, image.y)
                #sprite.text(str(Map.get(R,C).ticksfromstart), image.x, image.y)
                Mx, My = pygame.mouse.get_pos()
                if round(Mx) > image.x - 25 and round(Mx) < image.x + 25:
                    if round(My) > image.y - 25 and round(My) < image.y + 25:
                        stop = False
                        image.image = hotbarSlot
                        image.updateImage()
                        if pygame.mouse.get_pressed()[0] == 1:
                            if Map.get(R,C).ticks != 0:
                                image.image = blockTextures[str(blockIDs[Map.get(R,C).ID])+str(Map.get(R,C).lvl)]
                            else:
                                image.image = blockTextures[blockIDs[Map.get(R,C).ID]]
                            if not inventory[selectedSlot] == 0:
                                if itemIDs[inventory[selectedSlot].ID] == 'hoe':
                                    if Map.get(R,C).ID == 5:
                                        changeMap(R, C, Block(3, 1))
                                if itemIDs[inventory[selectedSlot].ID] == 'grassSeeds':
                                    if Map.get(R,C).ID == 3:
                                        changeMap(R, C, Block(1, 1))
                                        inventory[selectedSlot].used()
                                        if inventory[selectedSlot].count < 1:
                                            inventory[selectedSlot] = 0
                                            stop = True
                                if stop == False:
                                    if itemIDs[inventory[selectedSlot].ID] == 'berrySeeds':
                                        if Map.get(R,C).ID == 5:
                                            changeMap(R, C, Block(2, 1))
                                            inventory[selectedSlot].used()
                                            if inventory[selectedSlot].count < 1:
                                                inventory[selectedSlot] = 0
                                    if itemIDs[inventory[selectedSlot].ID] == 'lettuce':
                                        if Map.get(R,C).ID == 5:
                                            changeMap(R, C, Block(7, 1))
                                            inventory[selectedSlot].used()
                                            if inventory[selectedSlot].count < 1:
                                                inventory[selectedSlot] = 0
                        #print("right click!")
                        if pygame.mouse.get_pressed()[2] == 1:
                            #print("right click!")
                            if Map.get(R,C).ID == 2:
                                if Map.get(R,C).lvl == 2:
                                    changeMap(R, C, Block(2, 1))
                                    #Items.append(DroppedItem(C*50, R*50, 3))
                        if pygame.mouse.get_pressed()[0] == 1:
                            if Map.get(R,C).ID == 6:
                                changeMap(R, C, Block(5, 1))
                                #Items.append(DroppedItem(C*50, R*50, 1))
                            if Map.get(R,C).ID == 7:
                                changeMap(R, C, Block(5, 1))
                                #Items.append(DroppedItem(C*50, R*50, 4))
                                #Items.append(DroppedItem(C*50, R*50, 4))
            #Map.get(R,C).tick()

def EntityLoop():
    global Players, name
    deleteItems = []
    for item in Items:
        image = sprite.Player(screen, (0,0,0), 50, item.x-scrollX+25, item.y-scrollY+25, True, 0, item.degrees)
        image.image = itemImages[itemIDs[item.ID]]
        image.update()
        item.degrees += 1
        if round(player.x) > image.x - 50 and round(player.x) < image.x + 50:
            if round(player.y) > image.y - 50 and round(player.y) < image.y + 50:
                item.pickUp()
                deleteItems.append(item)
    for item in deleteItems:
        DeleteItemAsync(item)
        Items.remove(item)
    for Player in Players:
        if Player.name != name:
            image = sprite.Sprite(screen, (0,0,0), 50, Player.x-scrollX, Player.y-scrollY)
            image.updateImage()
            sprite.text(str(Player.name), Player.x-scrollX-((len(Player.name)*20)/2), Player.y-scrollY-40)

    

def move(keys):
    if keys[K_RIGHT] or keys[K_d]:
        player.realX += 7
    if keys[K_LEFT] or keys[K_a]:
        player.realX -= 7
    if keys[K_UP] or keys[K_w]:
        player.realY -= 7
    if keys[K_DOWN] or keys[K_s]:
        player.realY += 7

async def Main(): 
    global scrollX, scrollY, player
    GetMapSync()
    GetItemsAsync()
    ticks = 0
    while True:
        drawBackground()
        sprite.run()
        move(sprite.getKeys())
        EntityLoop()
        scrollX += (player.realX - scrollX)/10
        scrollY += (player.realY - scrollY)/10
        player.x = player.realX -scrollX + 720
        player.y = player.realY -scrollY + 380
        if scrollX > 1440:
            scrollX = 1440
        if scrollX < 0:
            scrollX = 0
        if scrollY > 760:
            scrollY = 760
        if scrollY < 0:
            scrollY = 0
        player.update()
        drawHotbar()
        pygame.display.flip()
        time.sleep(1/60)
        ticks += 1
        if ticks % 6 == 0:
            GetMapAsync()
            GetItemsAsync()
            GetPlayersAsync()
            SendPlayerAsync()

asyncio.run(Main())
print("goodbye")
farm_client.PlayerLeave(Player(name, scrollX, scrollY)).result()

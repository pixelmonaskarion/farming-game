import sprite
import pygame
import grid
import random as r
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
)

sprite.init(inputFont="Minecraft")

screen = sprite.setScreen(1440, 760)
player = sprite.Player(screen, (255,255,255), 50, 0, 0, False, 5)
player.realX = player.x
player.realY = player.y
scrollX = 0
scrollY = 0
hotbarSlot = sprite.newImage('pointer.png')
yellowPointer = sprite.newImage('yellowPointer.png')
selectedSlot = 1
Items = []
blockIDs = {
    1: 'Plantgrass',
    2: 'bush',
    3: 'soil',
    4: 'path',
    5: 'grass',
    6: 'tallGrass'
}
plantsTag = [1,2]
plantTimes = [10000,5000]
plantStages = [5,2]
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
    def __init__(self,x,y,ID):
        self.x = x + r.randint(-10,10)
        self.y = y + r.randint(-10,10)
        self.ID = ID
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
            

Map = grid.Grid(100,100)
for C in range(100):
    for R in range(100):
        ran = r.randint(0,5)
        if ran == 0:
            Map.change(R,C,"bushstarter")
        elif ran == 1:
            Map.change(R,C,"grassStarter")
        else:
            Map.change(R,C, Block(5))


        


def changeStarters():
    for i in range(len(Map.list)):
        if Map.list[i] == "bushstarter":
            Map.list[i] = Block(2, 2)
            if r.randint(1,5) == 1:
                if r.randint(1,2) == 1:
                    modifier = [-1,-10][r.randint(0,1)]
                    Map.list[1+modifier] = "bushstarter"
                    changeStarters()
                else:
                    modifier = [-1,-10][r.randint(0,1)]
                    Map.list[1-modifier] = "bushstarter"
    for i in range(len(Map.list)):
        if Map.list[i] == "grassStarter":
            Map.list[i] = Block(6)
            if r.randint(1,5) == 1:
                if r.randint(1,2) == 1:
                    modifier = [-1,-10][r.randint(0,1)]
                    Map.list[1+modifier] = "grassStarter"
                    changeStarters()
                else:
                    modifier = [-1,-10][r.randint(0,1)]
                    Map.list[1-modifier] = "grassStarter"

changeStarters()
scrollX = 0
scrollY = 0

itemIDs = {
    1: "grassSeeds",
    2: "hoe",
    3: 'berrySeeds'

}

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
    'tallGrass': sprite.newImage('tallGrass.png')
}


inventory = {
    1: Item(2,1),
    2: Item(3,5),
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
    'berrySeeds': sprite.newImage('berrySeeds.png')
}

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
                if Map.get(R,C).ticks != 0:
                    image.image = blockTextures[str(blockIDs[Map.get(R,C).ID])+str(Map.get(R,C).lvl)]
                else:
                    image.image = blockTextures[blockIDs[Map.get(R,C).ID]]
                image.updateImage()
                Map.get(R,C).tick()
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
                                        Map.change(R,C,Block(3))
                                if itemIDs[inventory[selectedSlot].ID] == 'grassSeeds':
                                    if Map.get(R,C).ID == 3:
                                        Map.change(R,C,Block(1))
                                        inventory[selectedSlot].used()
                                        if inventory[selectedSlot].count < 1:
                                            inventory[selectedSlot] = 0
                                            stop = True
                                if stop == False:
                                    if itemIDs[inventory[selectedSlot].ID] == 'berrySeeds':
                                        if Map.get(R,C).ID == 5:
                                            Map.change(R,C,Block(2))
                                            inventory[selectedSlot].used()
                                            if inventory[selectedSlot].count < 1:
                                                inventory[selectedSlot] = 0
                            if pygame.mouse.get_pressed()[2] == 1:
                                if Map.get(R,C).ID == 2:
                                    if Map.get(R,C).lvl == 2:
                                        Map.get(R,C).lvl = 1
                                        Items.append(DroppedItem(C*50, R*50, 3))
                            if pygame.mouse.get_pressed()[0] == 1:
                                if Map.get(R,C).ID == 6:
                                    Map.get(R,C).ID = 5
                                    Items.append(DroppedItem(C*50, R*50, 1))

def itemLoop():
    deleteItems = []
    for item in Items:
        image = sprite.Sprite(screen, (0,0,0), 50, item.x-scrollX+25, item.y-scrollY+25)
        image.image = itemImages[itemIDs[item.ID]]
        image.updateImage()
        if round(player.x) > image.x - 50 and round(player.x) < image.x + 50:
            if round(player.y) > image.y - 50 and round(player.y) < image.y + 50:
                item.pickUp()
                deleteItems.append(item)
    for item in deleteItems:
        Items.remove(item)

def move(keys):
    if keys[K_RIGHT] or keys[K_d]:
        player.realX += 5
    if keys[K_LEFT] or keys[K_a]:
        player.realX -= 5
    if keys[K_UP] or keys[K_w]:
        player.realY -= 5
    if keys[K_DOWN] or keys[K_s]:
        player.realY += 5
    
while True:
    drawBackground()
    sprite.run()
    move(sprite.getKeys())
    itemLoop()
    scrollX = player.realX
    scrollY = player.realY
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
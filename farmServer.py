# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging

import grpc

import farmServerMethods_pb2
import farmServerMethods_pb2_grpc

import random as r
import grid

import google

import time

plantsTag = [1,2,7]
plantTimes = [5000,5000,100 ]
plantStages = [5,2,2]
Players = []
Items = []

class Player():
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

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
        self.degrees = r.randint(0,360)
        self.ID = ID

Map = grid.Grid(100,100)
for C in range(100):
    for R in range(100):
        ran = r.randint(0,10)
        if ran == 0 or ran == 5:
            Map.change(R,C,"bushstarter")
        elif ran == 1 or ran == 6:
            Map.change(R,C,"grassStarter")
        elif ran == 2:
            Map.change(R,C,"lettucestarter")
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
    for i in range(len(Map.list)):
        if Map.list[i] == "lettucestarter":
            Map.list[i] = Block(7)
            if r.randint(1,5) == 1:
                if r.randint(1,2) == 1:
                    modifier = [-1,-10][r.randint(0,1)]
                    Map.list[1+modifier] = "lettucestarter"
                    changeStarters()
                else:
                    modifier = [-1,-10][r.randint(0,1)]
                    Map.list[1-modifier] = "lettucestarter"

changeStarters()


class FarmServer(farmServerMethods_pb2_grpc.FarmingServicer):

    def GetMap(self, request, context):
        #print(request)
        print('GOT MAP')
        BlocksFromMap = []
        R = 0
        C = 0
        i = 0
        for block in Map.list:
            BlocksFromMap.append(farmServerMethods_pb2.SpecificBlock(r=R,c=C, block=farmServerMethods_pb2.Block(ID=block.ID, Lvl=block.lvl)))
            C += 1
            if C > 99:
                C = 0
                R += 1
            i += 1
        return farmServerMethods_pb2.Map(block=BlocksFromMap)
    
    def SendPlayer(self, request, context):
        stop = False
        for i in range(len(Players)):
            player = Players[i]
            if player.name == request.name:
                stop = True
                Players[i].x = request.x
                Players[i].y = request.y
        if stop == False:
            Players.append(Player(request.name, request.x, request.y))
        return google.protobuf.empty_pb2.Empty()
    
    def PlayerLeave(self, request, context):
        for i in range(len(Players)):
            if request.name == Players[i].name:
                Players.pop(i)
                break
        return google.protobuf.empty_pb2.Empty()
    
    def GetPlayers(self, request, context):
        print('GOT Players')
        protoPlayer = []
        for player in Players:
            protoPlayer.append(farmServerMethods_pb2.Player(x=player.x,y=player.y, name=player.name))
        return farmServerMethods_pb2.Players(player=protoPlayer)


    def changeStuff(self, changed, context):
        global Map
        print("got", changed.changedto.ID, "current block is", Map.get(changed.r, changed.c).ID)
        print("changing R: "+str(changed.r), 'C: ' + str(changed.c))
        ID = Map.get(changed.r, changed.c).ID
        if ID == 5 and changed.changedto.ID == 3:
            Map.change(changed.r, changed.c, Block(3))
            print("action till grass")
        elif ID == 5 and changed.changedto.ID == 2:
            Map.change(changed.r, changed.c, Block(2))
            print("action plant bush")
        elif ID == 2 and changed.changedto.ID == 2:
            Map.change(changed.r, changed.c, Block(2))
            Items.append(DroppedItem(changed.c*50, changed.r*50, 3))
            print("action get berries")
        elif ID == 7 and changed.changedto.ID == 5:
            print("action break lettuce")
            Map.change(changed.r, changed.c, Block(5))
            Items.append(DroppedItem(changed.c*50, changed.r*50, 4))
        elif ID == 3 and changed.changedto.ID == 1:
            Map.change(changed.r, changed.c, Block(1))
            print("action plant grass")
        elif ID == 6 and changed.changedto.ID == 5:
            Map.change(changed.r, changed.c, Block(5))
            print("action break grass")
            Items.append(DroppedItem(changed.c*50, changed.r*50, 1))
        else:
            print("no action found :/")
        MapOfBlocks = []
        for r in range(100):
            for c in range(100):
                MapOfBlocks.append(farmServerMethods_pb2.SpecificBlock(r=r,c=c,block=farmServerMethods_pb2.Block(ID=Map.get(r,c).ID,Lvl=Map.get(r,c).lvl)))
        return farmServerMethods_pb2.Map(block=MapOfBlocks)
    def GetItems(self, request, context):
        print('GOT ITEMS')
        ItemList = []
        for item in Items:
            Item = farmServerMethods_pb2.Item(ID=item.ID, x=item.x, y=item.y, ro=item.degrees)
            ItemList.append(Item)
            #print("x:", item.x, "y:", item.y)
        return farmServerMethods_pb2.Items(item=ItemList)
    
    def DeleteItems(self, request, context):
        global Items
        print("SIZE OF ITEMS BEFORE", len(Items))
        deleteItem = []
        y = request.y
        x = request.x
        ID = request.ID
        for check in Items:
            #print(x, y, check.x, check.y)
            if ID == check.ID and x == check.x and y == check.y:
                #print('found item to be deleted')
                deleteItem.append(check)
                break
        for item in deleteItem:
            Items.remove(item)
        #print("SIZE OF ITEMS AFTER", len(Items))
        return request

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    farmServerMethods_pb2_grpc.add_FarmingServicer_to_server(FarmServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    while True:
        for item in Items:
            item.degrees += 1
        time.sleep(1/60)




if __name__ == '__main__':
    logging.basicConfig()
    serve()

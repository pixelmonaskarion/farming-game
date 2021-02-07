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
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function
import logging
import time

import grpc

import farmServerMethods_pb2
import farmServerMethods_pb2_grpc

import google
import google.protobuf.json_format as json_format
'24.16.205.170'
global stub
channel = grpc.insecure_channel('farm.themagicdoor.org:50051')
stub = farmServerMethods_pb2_grpc.FarmingStub(channel)

def generate_messages(message):
    messages = message
    
    for msg in messages:
        print("Asking for R %s and C %s" % (msg.r, msg.c))
        yield msg


def changeStuff(change=[farmServerMethods_pb2.MapUpdate(r=1,c=1, changedto=farmServerMethods_pb2.Block(ID=1, Lvl=1))]):
    startTime = time.perf_counter_ns()
    response = stub.changeStuff(change)
    Map = []
    for response in responses:
        Map.append(response)
    print("took %f seconds" % ((time.perf_counter_ns() - startTime)/1.0e9))
    Map = Map[0]
    #print(Map.block)
    return Map

def GetMapAsync():
    response_future = stub.GetMap.future(google.protobuf.empty_pb2.Empty())
    #response = response_future.result()
    return response_future

def GetItemsAsync():
    response_future = stub.GetItems.future(google.protobuf.empty_pb2.Empty())
    #response = response_future.result()
    return response_future

def GetPlayersAsync():
    response_future = stub.GetPlayers.future(google.protobuf.empty_pb2.Empty())
    #response = response_future.result()
    return response_future

def ChangeStuffAsync(change=[farmServerMethods_pb2.MapUpdate(r=1,c=1, changedto=farmServerMethods_pb2.Block(ID=1, Lvl=1))]):
    print('send change')
    Map_future = stub.changeStuff.future(change)
    #print(Map.block)
    #print("sending change request")
    #response = response_future.result()
    return Map_future

def GetMapSync():
    startTime = time.perf_counter_ns()
    response_future = GetMapAsync()
    response = response_future.result()
    print("took %f seconds" % ((time.perf_counter_ns() - startTime)/1.0e9))
    if (time.perf_counter_ns() - startTime)/1.0e9 > 1/60:
        print("not good enough :(")
    return response

def GetItemsSync():
    startTime = time.perf_counter_ns()
    response_future = GetItemsAsync()
    response = response_future.result()
    print("took %f seconds" % ((time.perf_counter_ns() - startTime)/1.0e9))
    if (time.perf_counter_ns() - startTime)/1.0e9 > 1/60:
        print("not good enough :(")
    return response

def GetItem():
    startTime = time.perf_counter_ns()
    response = stub.GetItems(google.protobuf.empty_pb2.Empty())
    print("took %f seconds" % ((time.perf_counter_ns() - startTime)/1.0e9))
    if (time.perf_counter_ns() - startTime)/1.0e9 > 1/60:
        print("not good enough :(")
    return response

def DeleteItemAsync(Item):
    response_future = stub.DeleteItems.future(farmServerMethods_pb2.Item(x=Item.x, y=Item.y, ID=Item.ID))
    #response = response_future.result()
    return response_future

def SendPlayerAsync(player):
    response_future = stub.SendPlayer.future(farmServerMethods_pb2.Player(x=player.x, y=player.y, name=player.name))
    #response = response_future.result()
    return response_future

def PlayerLeave(player):
    response_future = stub.SendPlayer.future(farmServerMethods_pb2.Player(x=player.x, y=player.y, name=player.name))
    #response = response_future.result()
    return response_future



def run():
    global stub
    channel = grpc.insecure_channel('localhost:50051')
    stub = farmServerMethods_pb2_grpc.FarmingStub(channel)
    #response = stub.GetMap(google.protobuf.empty_pb2.Empty())
    #print("Greeter client received:", json_format.MessageToJson(response))
    print("hello, I am doing the chat thing now")
    guide_route_chat()


if __name__ == '__main__':
    logging.basicConfig()
    run()
    

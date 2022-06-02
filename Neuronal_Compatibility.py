

# -*- coding: utf-8 -*-
"""
Created on Thu May  5 10:17:42 2022

@author: User
"""
import grpc
import minecraft_pb2_grpc
from minecraft_pb2 import *
from random import randrange
from random import random
import random
import numpy as np 
import math

channel = grpc.insecure_channel('localhost:5001')
client = minecraft_pb2_grpc.MinecraftServiceStub(channel)

# our sigmoid function, tanh is a little nicer than the standard 1/(1+e^-x)


def sigmoid(x):
    return np.tanh(x)
 
# derivative of our sigmoid function
def dsigmoid(x):
    return 1.0 - x**2
     
def round_numb(number):
    return np.round(number * 2) / 2
class MLP:
    def __init__(self, *args):
        self.args = args
        n = len(args)
         
        self.layers = [np.ones(args[i] + (i==0)) for i in range(0, n)]
         
        self.weights = list()
        for i in range(n-1):
            R = np.random.random((self.layers[i].size, self.layers[i+1].size))
            self.weights.append((2*R-1)*0.20)
             
        self.m = [0 for i in range(len(self.weights))]
             
         
    def update(self, inputs):
        self.layers[0][:-1] = inputs
         
        for i in range(1, len(self.layers)):
            self.layers[i] = sigmoid(np.dot(self.layers[i-1], self.weights[i-1]))
 
             
        return self.layers[-1]
         
         
    def backPropagate(self, inputs, outputs, a=0.1, m=0.1):
         
        error = outputs - self.update(inputs)
        de = error*dsigmoid(self.layers[-1])
        deltas = list()
        deltas.append(de)
         
         
        for i in range(len(self.layers)-2, 0, -1):
 
            deh = np.dot(deltas[-1], self.weights[i].T) * dsigmoid(self.layers[i])
            deltas.append(deh)
             
        deltas.reverse()
         
        for i, j in enumerate(self.weights):
             
            layer = np.atleast_2d(self.layers[i])
            delta = np.atleast_2d(deltas[i])
             
            dw = np.dot(layer.T,delta)
            self.weights[i] += a*dw + m*self.m[i]
            self.m[i] = dw
             
 
 
 
pat = (((0,0), 0),
    ((0,0.5), -1),
    ((0,1), -1),
    ((0.5,0.5), 0.5),
    ((0.5,0), -1),
    ((0.5,1), -1),
    ((1,1), 1),
    ((1,0.5), -1),
    ((1,0), -1),
    )
 
 
n = MLP(2, 3, 1)

checkColor=np.array([0,0])
for i in range(1000):
    for p in pat:
        
        n.backPropagate(p[0], p[1])
         
for p in pat:
    print (n.update(p[0]))

print(n.backPropagate(0, 1))
    
client.fillCube(FillCubeRequest(  # Clear a 20x10x20 working area
    cube=Cube(
        min=Point(x=-100, y=4, z=-100),
        max=Point(x=100, y=14, z=100)
    ),
    type=AIR
  
))
client.fillCube(FillCubeRequest(  # Clear a 20x10x20 working area
    cube=Cube(
        min=Point(x=-100, y=0, z=-100),
        max=Point(x=50, y=3, z=50)
    ),
    type=GRASS
))
client.fillCube(FillCubeRequest(  # Clear a 20x10x20 working area
    cube=Cube(
        min=Point(x=-0, y=0, z=0),
        max=Point(x=9, y=3, z=9)
    ),
    type=OBSIDIAN
))


          
def initPopulationa(nIndividuals, nChromosome, valMaxXChromosome,valMaxZChromosome):
    client = minecraft_pb2_grpc.MinecraftServiceStub(channel)
    population = [[0] * nChromosome for n in range(nIndividuals)]
    
    for i in range(0, nIndividuals):
            randomColor=random.randint(0,2)
            color=0
            if randomColor==0:
                color=0
            if randomColor==1:
                color=0.5
            if randomColor==2:
                color=1
            population[i] = (random.randint(0, valMaxXChromosome),5,random.randint(0, valMaxZChromosome),color)
            row=population[i][0]
            
            height=population[i][1]
       
            column=population[i][2]
            if randomColor==0:
                client.spawnBlocks(Blocks(blocks=[Block(position=Point(x=row, y=5, z=column), type=REDSTONE_BLOCK, orientation=NORTH),
                ]))
            if randomColor==1:
                client.spawnBlocks(Blocks(blocks=[Block(position=Point(x=row, y=5, z=column), type=LAPIS_BLOCK, orientation=NORTH),
                ]))
            if randomColor==2:
                client.spawnBlocks(Blocks(blocks=[Block(position=Point(x=row, y=5, z=column), type=EMERALD_BLOCK, orientation=NORTH),
                ]))
               
    return population
                        
# Fonction initPopulation() :


NB_CHROMOSOME_MAX = 20
VAL_CHROMOSOME_MAX = 6
NB_INDIVIDUAL_MAX = 20

X=9
Y=14
Z=9
# p est l'individu qui atteint l'objectif 
# si p = cible on a trouvÃ© un individu
p = 0
# compteur de nombre de tentatives
attempts = 1


def moveRandom(pop):
    
    
    newPopulation = [[0] * len(pop[0]) for n in range(len(pop))]
    

    
    listToDelete=[]
    listIndex=[]
    samePos=False
    for p in range(0, len(newPopulation)):

        newPopulation[p][0] = pop[p][0]
        newPopulation[p][1] = pop[p][1]
        newPopulation[p][2] = pop[p][2]
        newPopulation[p][3] = pop[p][3]
        
        ran=random.randint(1, 4)

        if(ran==1 and newPopulation[p][0]<=9):
            newPopulation[p][0] += 1 
 
        if(ran==2 and newPopulation[p][2]<=9):
            newPopulation[p][2] += 1 
        if(ran==3 and newPopulation[p][0]>=0):
            newPopulation[p][0] -= 1 
        if(ran==4 and newPopulation[p][2]>=0):
            newPopulation[p][2] -= 1
        row=pop[p][0]
       
        height=pop[p][1]
      
        column=pop[p][2]
        
        row1=newPopulation[p][0]
       
        height1=newPopulation[p][1]
      
        column1=newPopulation[p][2]
        
        if pop[p][3]==0:
        

            client.spawnBlocks(Blocks(blocks=[Block(position=Point(x=row, y=height, z=column), type=AIR, orientation=NORTH),
            ]))
            client.spawnBlocks(Blocks(blocks=[Block(position=Point(x=row1, y=height1, z=column1), type=REDSTONE_BLOCK, orientation=NORTH),
            ]))
        elif pop[p][3]==0.5:
            client.spawnBlocks(Blocks(blocks=[Block(position=Point(x=row, y=height, z=column), type=AIR, orientation=NORTH),
            ]))
            client.spawnBlocks(Blocks(blocks=[Block(position=Point(x=row1, y=height1, z=column1), type=LAPIS_BLOCK, orientation=NORTH),
            ]))
        elif pop[p][3]==1:
            client.spawnBlocks(Blocks(blocks=[Block(position=Point(x=row, y=height, z=column), type=AIR, orientation=NORTH),
            ]))
            client.spawnBlocks(Blocks(blocks=[Block(position=Point(x=row1, y=height1, z=column1), type=EMERALD_BLOCK, orientation=NORTH),
            ]))
        
        
        for j in range(0, len(newPopulation)):
            
                
            if(newPopulation[p][0]==newPopulation[j][0] and 
               newPopulation[p][1]==newPopulation[j][1] and 
               newPopulation[p][2]==newPopulation[j][2] and
               
               p!=j):
                samePos=True
                
                listToDelete.append(newPopulation[p])
                listIndex.append(p)
                listToDelete.append(newPopulation[j])
                listIndex.append(j)
                print("test")
                print(listToDelete)
                """
                for j in range(0, len(newPopulation)):
                
                    if(newPopulation[p]==newPopulation[j] and p!=j):

                        newX=newPopulation[p][0]
                        newY=newPopulation[p][1]
                        newZ=newPopulation[p][2]
                        print("delete")
                        del newPopulation[p]
                        del newPopulation[j]
                        client.spawnBlocks(Blocks(blocks=[Block(position=Point(x=newX, y=newY, z=newZ), type=AIR, orientation=NORTH),
                        ]))
                        client.spawnBlocks(Blocks(blocks=[Block(position=Point(x=newX, y=newY+1, z=newZ), type=DIAMOND_BLOCK, orientation=NORTH),
                        ]))
                        break
            return newPopulation
                """
                
                
        if(samePos==True and p==(len(newPopulation))-1):
                taille=int(len(listToDelete)/2)

                
                for k in range(0,taille):
                    print("list to delete")
                    print(listToDelete)
                    newX=listToDelete[k][0]
                    newY=listToDelete[k][1]
                    newZ=listToDelete[k][2]
                    checkColor[0]=listToDelete[k][3]
                    checkColor[1]=listToDelete[k+1][3]
                    print("check")
                    print(checkColor[0])
                    print(checkColor[1])
                    for p in pat:
                        
                        var =n.update(checkColor[0])
                        var1=round_numb(var)
                        print("var")
                        print(var)
                    if listToDelete[k][3]==listToDelete[k+1][3]:
                        
                        
                        if listToDelete[k][3]==0:
                            print("red")
                            client.spawnBlocks(Blocks(blocks=[Block(position=Point(x=newX, y=newY, z=newZ), type=AIR, orientation=NORTH),
                                                          ]))
                            client.spawnBlocks(Blocks(blocks=[Block(position=Point(x=newX, y=newY+1, z=newZ), type=RED_GLAZED_TERRACOTTA, orientation=NORTH),
                                                          ]))
                        if listToDelete[k][3]==0.5:
                            print("blue")
                            client.spawnBlocks(Blocks(blocks=[Block(position=Point(x=newX, y=newY, z=newZ), type=AIR, orientation=NORTH),
                                                          ]))
                            client.spawnBlocks(Blocks(blocks=[Block(position=Point(x=newX, y=newY+1, z=newZ), type=BLUE_GLAZED_TERRACOTTA, orientation=NORTH),
                                                          ]))
                        if listToDelete[k][3]==1:
                            print("green")
                            client.spawnBlocks(Blocks(blocks=[Block(position=Point(x=newX, y=newY, z=newZ), type=AIR, orientation=NORTH),
                                                          ]))
                            client.spawnBlocks(Blocks(blocks=[Block(position=Point(x=newX, y=newY+1, z=newZ), type=GREEN_GLAZED_TERRACOTTA, orientation=NORTH),
                                                          ]))
                       
                    else:
                        print("delete")
                        client.spawnBlocks(Blocks(blocks=[Block(position=Point(x=newX, y=newY, z=newZ), type=AIR, orientation=NORTH),
                                                          ]))
                        
                    k+=1

                    
                for l in range(0,len(listToDelete)):
                

                    del newPopulation[listIndex[l]]

                        
                    
                

                
                
       
    return newPopulation
# MAIN
print("### BUILDING POPULATION")

pop = initPopulationa(NB_INDIVIDUAL_MAX, NB_CHROMOSOME_MAX, X,Z)
for i in range(1000):
    pop = moveRandom(pop)
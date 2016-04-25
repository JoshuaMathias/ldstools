from __future__ import division
import sys
import os
import random
import copy

class Apt:
    def __init__(self,num,gender):
        self.gender=gender
        self.houses={'Morley':0,'Martin':0,'Brown':0,'Bett':0,'Eggett':0}
        self.num=num

def assignGroups(groups,apts):
    for apt in apts:
        assigned=False
        while not assigned:
            index=random.randint(0,2)
            if (index==0 and len(groups['Morley'])<10):
                newGroups['Morley'].append(apts[apt])
                assigned=True
            # if (index==1 and len(groups['Martin'])<8):
            #     newGroups['Martin'].append(apts[apt])
            #     assigned=True
            if (index==1 and len(groups['Brown'])<10):
                newGroups['Brown'].append(apts[apt])
                assigned=True
            # if (index==3 and len(groups['Bett'])<5):
            #     newGroups['Bett'].append(apts[apt])
            #     assigned=True
            if (index==2 and len(groups['Eggett'])<10):
                newGroups['Eggett'].append(apts[apt])
                assigned=True
    return groups

def calcGroups(groups):
    cost=0
    for name in groups:
        f=0
        m=0
        for apt in groups[name]:
            if apt.gender=='f':
                f+=1
            else:
                m+=1
            cost+=(apt.houses[name])**2
        cost+=2*(f-m)**2
    return cost

def printGroups(groups):
    for name in groups:
        if name is "Morley":
            print "Bishop "+name+": Apartments",
        else:
            print "Brother "+name+": Apartments",
        f=0
        m=0
        for apt in groups[name]:
            if apt.gender=='f':
                f+=1
            else:
                m+=1
            sys.stdout.write(" "+str(apt.num))
            if apt!=groups[name][len(groups[name])-1]:
                sys.stdout.write(",")
        print "\n males: "+str(m)+" females: "+str(f)

# groups={'Morley':[],'Martin':[],'Brown':[],'Bett':[],'Eggett':[]}
groups={'Martin':[],'Brown':[],'Morley':[],'Eggett':[]}
mApts=[1,2,3,4,9,10,11,12,104,105,215,216,217,333,334,335]
fApts=[5,6,7,8,13,14,15,16,106,107,218,219,336,337]
apts={}
for apt in mApts:
    apts[apt]=Apt(apt,'m')
for apt in fApts:
    apts[apt]=Apt(apt,'f')

pastFile=open('past_fhes.txt','r')
pastCount=0
for line in pastFile:
    if len(line)>1:
        words=line.split()
        name=words[1].replace(":","")
        if name in groups.keys():
            for i in range(3,len(words)):
                num=int(words[i].replace(',',''))
                if pastCount==0: # If they visited this house last time
                    apts[num].houses[name]+=4
                else:
                    apts[num].houses[name]+=2
    else:
        pastCount+=1

bestCost=1000000
bestGroups={}
numTries=1000000
for rounds in range(numTries):
    if rounds%(numTries/10)==0:
        print(str(rounds/numTries*100)+"% done")
    random.seed()
    newGroups=copy.deepcopy(groups)
    newGroups=assignGroups(newGroups,apts)
    cost=calcGroups(newGroups)
    # print "Cost: "+str(cost)
    if cost<bestCost:
        bestCost=cost
        bestGroups=newGroups
    # printGroups(bestGroups)
print "Best cost: "+str(bestCost)
printGroups(bestGroups)
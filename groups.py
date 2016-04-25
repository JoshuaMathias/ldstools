from __future__ import division
import sys
import os
import random
import copy
import re

# Take into account who was in their previous group, what apartment they were in, and how many men and women are in the group.
class Person:
    def __init__(self,name,gender,apt,phone,canHost):
        self.name=name
        self.gender=gender
        self.apt=apt
        self.phone=phone
        if canHost=="Yes" or canHost=="y" or canHost=="Y":
          self.canHost=True
        else:
          self.canHost=False
        self.hostCount=0
        self.persons=persons
        self.previousApts={0:0,1:0,2:0,3:0,4:0,9:0,10:0,11:0,12:0,104:0,105:0,215:0,216:0,217:0,333:0,334:0,335:0,5:0,6:0,7:0,8:0,13:0,14:0,15:0,16:0,106:0,107:0,218:0,219:0,336:0,337:0}
        self.groups=[]

    def setPersons(self,persons):
      self.persons=persons

    def addGroup(self,groupNum):
      self.groups.append(groupNum)

    def addApt(self,apt,num):
      self.previousApts[apt]+=num

    def addPerson(self,name):
      self.persons[name]+=1

    def addHostCount(self):
      self.hostCount+=1

    def getPrevAptVal(self,apt):
      if apt in self.previousApts:
        return self.previousApts[apt]
      return 0


class Group:
  def __init__(self,persons,hostApt,hostName):
    self.persons=persons
    self.hostApt=hostApt
    self.host=hostName

  def addPerson(self,person):
    self.persons.append(person)

  def addHost(apt,name):
    self.hostApt=apt
    self.host=name

def getPerson(persons,name):
  for person in persons:
    if person.name==name:
      return person
  return -1

def assignGroups(persons,numGroups):
  random.shuffle(persons)
  hosts=[]
  for person in persons:
    if person.canHost:
      hosts.append(person)
  groupSize=len(persons)/numGroups
  personCount=0
  newGroups={}
  chosenHosts=[]
  numExtra=len(persons)-groupSize*numGroups
  extras=0
  foundAHost=False
  hostCount=0
  for group in range(1,numGroups+1):
    chosenHosts.append(hosts[group])

  for group in range(1,numGroups+1):
    newGroupPersons=[]
    newGroupPersons.append(chosenHosts[group-1])
    # print "Creating group "+str(group)
    extra=0
    if extras<numExtra:
      extra=1
      extras+=1
    while len(newGroupPersons)<(groupSize+extra): # Minus 1 because a host was already added
      # print persons[personCount].canHost
      if persons[personCount] not in chosenHosts:
        newGroupPersons.append(persons[personCount])
      personCount+=1
    newGroups.update({group:Group(newGroupPersons,newGroupPersons[0].apt,newGroupPersons[0].name)})
  return newGroups

def calcGroups(persons,groups,hostApts):
    cost=0
    for group in groups:
        f=0
        m=0
        for person in groups[group].persons:
            # print person.name
            # print person.persons
            # print person.previousApts
            # print person.groups
            # print person.hostCount
            if isGirl(person.gender):
                f+=1
            else:
                m+=1
            for groupMate in groups[group].persons:
              if groupMate.name!=person.name:
                cost+=(person.persons[groupMate.name])**2 # Prefer to not be with the same people.
            cost+=getPerson(persons,person.name).hostCount**2 # Prefer to not be a host multiple times
            cost+=getPerson(persons,person.name).getPrevAptVal(groups[group].hostApt)**2 # Prefer to not go to the same apartment multiple times
        cost+=((f-m)*10)**2 # Prefer an even amount of males and females in each group
        cost+=hostApts.count(groups[group].hostApt)**2 # Prefer for the same apartment to not host multiple times
    return cost

def isGirl(gender):
  if gender=='Female' or gender=='F' or gender=='f':
    return True
  else:
    return False

def printGroups(groups,outFileName):
    outFile=open(outFileName,'w')
    total=0
    for group in groups:
        f=0
        m=0
        for person in groups[group].persons:
            if isGirl(person.gender):
                f+=1
            else:
                m+=1
            if groups[group].host==person.name:
              outFile.write("Host")
            canHost="No"
            if person.canHost:
              canHost="Yes"
            outFile.write(","+person.name+","+str(group)+","+person.gender+","+person.phone+","+str(person.apt)+","+str(canHost)+"\n")
        print "Males: "+str(m)+" Females: "+str(f)
        total+=f+m
    print "Total in groups: "+str(total)

def outputMessage(groups,messageFileName):
  outFile=open(messageFileName,'w')
  outFile.write("Dinner Groups\n")
  for group in groups:
    outFile.write("Group #"+str(group)+":\n")
    outFile.write("Host: \n")
    outFile.write("Members: \n")
    for person in groups[group].persons:
      outFile.write(person.name+", apartment: "+str(person.apt)+", phone: "+person.phone+"\n")
    outFile.write("\n")

def getPastData(prevGroupsFile,names,persons,hostApts):
  groups={}
  hostApts=[]
  groupHosts={}
  removeWhiteS = re.compile(r'\s+')
  for line in prevGroupsFile:
    if len(line)>1:
        data=line.split(",")
        name=data[1]
        if name in names: # This also skips the first line with column titles
          group=data[2]
          if group not in groups:
            groups[group]=[]
          groups[group].append(name)
          if data[0]=="Host":
            curPerson=getPerson(persons,name)
            if curPerson!=-1:
              curPerson.addHostCount()
            apt=re.sub(removeWhiteS, '', data[5])
            if apt!="":
              hostApts.append(int(apt))
              groupHosts[group]=apt


  for group in groups:
    for person in groups[group]:
      # print person
      curPerson=getPerson(persons,person)
      # print groupHosts
      # print group
      if group in groupHosts:
        curPerson.addApt(int(groupHosts[group]),1)
      for name in groups[group]:
        curPerson.addPerson(name)
  return hostApts

removeWhiteS = re.compile(r'\s+')
persons=[]
names={}
personsFile=open('dinnergroupspersons.csv','r')
outFileName='NewGroups.csv'
messageFileName='Dinner Groups.txt'
pastCount=0
fCount=0
mCount=0

for line in personsFile:
    if len(line)>1:
        data=line.split(",")
        name=data[0]
        if name=="Name": # Skip first line with column titles
          continue
        gender=data[1].upper()
        if isGirl(gender):
          fCount+=1
        else:
          mCount+=1
        aptNum=0
        if data[2]!="":
          aptNum=int(data[2])
        phone=data[3]

        canHost=re.sub(removeWhiteS, '', data[4].lower())
        persons.append(Person(name,gender,aptNum,phone,canHost))
        names[name]=0
for person in persons:
  person.setPersons(names)
print "Males: "+str(mCount)
print "Females: "+str(fCount)
print "Total: "+str(mCount+fCount)

NovGroupsFile=open('NovemberDinnerGroups.csv')
JanGroupsFile=open('JanDinnerGroups.csv')
FebGroupsFile=open('FebDinnerGroups.csv')
MarGroupsFile=open('MarDinnerGroups.csv')
hostApts=[]
hostApts=getPastData(NovGroupsFile,names,persons,hostApts)
hostApts=getPastData(JanGroupsFile,names,persons,hostApts)
hostApts=getPastData(FebGroupsFile,names,persons,hostApts)
hostApts=getPastData(MarGroupsFile,names,persons,hostApts)
bestCost=1000000
bestGroups={}
numTries = 10
numGroups=10
for rounds in range(numTries):
    if rounds%(numTries/10)==0:
        print(str(rounds/numTries*100)+"% done")
    random.seed()
    newGroups=assignGroups(persons,numGroups)
    cost=calcGroups(persons,newGroups,hostApts)
    # print "Cost: "+str(cost)
    if cost<bestCost:
        bestCost=cost
        bestGroups=newGroups
    # printGroups(bestGroups)
print "Best cost: "+str(bestCost)
printGroups(bestGroups,outFileName)
outputMessage(bestGroups,messageFileName)
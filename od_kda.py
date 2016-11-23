import json
import requests
import time
from steamTools import getUserInput32withShortcuts as getInput
from dotaTools import getLegs

#a list of 4 lists of 5 lists of 4 ints
#0 level is game state (0 rad win, 1 rad loss, 2 dire win, 3 dire loss)
#1 level is number of legs
#2 level is games kills deaths assists
#masterList[side/win State][leg group][game count/k/d/a]
#so the number assists in games where the player is radiant and wins, on a hero with 2 legs
#is at list[0][1][3]
masterList = []
for i in range(4):
    masterList.append([])
    for j in range(5):
        masterList[i].append([])
        for k in range(4):
            masterList[i][j].append(0)


def getMatches(account32):
    return requests.get("https://api.opendota.com/api/players/"+str(account32)+"/matches?significant=1").json()

def parseMatchData(match,relevantList):
    relevantList[0] += 1
    relevantList[1] += match["kills"]
    relevantList[2] += match["deaths"]
    relevantList[3] += match["assists"]

def analyzeMatch(match):
    if int(match['hero_id']):
        legVector = getLegs(match["hero_id"])/2
        if match["player_slot"] < 64 and match["radiant_win"]:
            parseMatchData(match,masterList[0][legVector])
        if match["player_slot"] < 64 and not match["radiant_win"]:
            parseMatchData(match,masterList[1][legVector])
        if match["player_slot"] > 64 and not match["radiant_win"]:
            parseMatchData(match,masterList[2][legVector])
        if match["player_slot"] > 64 and match["radiant_win"]:
            parseMatchData(match,masterList[3][legVector])
    else:
        print "Discarding an insignificant match"

def getTotalMatches():
    m = 0
    for i in range(4):
        for j in range(5):
            m += masterList[i][j][0]
    return m

def getWinrateList():
    #returns a list of two lists containing radiant and dire winrates per leg group
    wrlist = []
    for i in range (2):
        wrlist.append([])
        for j in range (5):
            wrlist[i].append(0)
            try:
                wrlist[i][j] = round(masterList[i*2][j][0]/float(masterList[i*2][j][0]+masterList[i*2+1][j][0]),3)
            except ZeroDivisionError:
                pass
    return wrlist

def getPerformanceList(state):
    #returns a list of 4 lists: kills,deaths,assists,and ka/d ratio by leg group
    perfList = []
    for i in range(3):
        perfList.append([])
        for j in range(5):
            perfList[i].append(0)
            try:
                perfList[i][j] = round(masterList[state][j][i+1]/float(masterList[state][j][0]),3)
            except ZeroDivisionError:
                pass
    #add an extra list for kill+assist / death ratio
    perfList.append([round((k+a)/d if d else -1,3) for k,d,a in zip(perfList[0],perfList[1],perfList[2])])

    return perfList


def displayData():
    print "Analyzed "+str(getTotalMatches())+" matches"
    print "Radiant Winrate:",getWinrateList()[0]
    print "Dire Winrate:",getWinrateList()[1]
    print "Performance k+a/d"
    print "in radiant wins:",getPerformanceList(0)[3]
    print "in radiant loss:",getPerformanceList(1)[3]
    print "in dire wins:",getPerformanceList(2)[3]
    print "in dire loss:",getPerformanceList(3)[3]


map(analyzeMatch,getMatches(getInput()))
displayData()


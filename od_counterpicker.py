import dotaTools
import steamTools
import requests
import json


def getWinrates(account,againstHeroID=None,radiant=None):
    #returns a dict of winrates identified by heroid, containing id, winrate, and number of games
    url = "https://api.opendota.com/api/players/"+str(account)+"/heroes"
    payload = {'significant':1}
    if againstHeroID:
        payload['against_hero_id'] = againstHeroID
    if not radiant == None:
        payload['is_radiant'] = int(radiant)
    heroes = requests.get(url,params=payload).json()
    winrates = {}
    for hero in heroes:
        winrates[int(hero['hero_id'])] = {}
        try:
            winrates[int(hero['hero_id'])]['winrate'] = hero['win']/float(hero['games'])
        except ZeroDivisionError:
            winrates[int(hero['hero_id'])]['winrate'] = None
        winrates[int(hero['hero_id'])]['games'] = int(hero['games'])
        winrates[int(hero['hero_id'])]['id'] = int(hero['hero_id'])
    return winrates

def getNextTop(winrates,sortKey='winrate'):
    return winrates.pop(max(winrates.keys(),key=lambda k:winrates[k][sortKey]))

def getWinratesWithDeltas(account,againstHeroID,radiant=None):
    #essentially returns a general winrates dict with deltas for the given hero appended
    winrates = getWinrates(account,None,radiant)
    winratesAgainstAntagonist = getWinrates(account,againstHeroID,radiant)
    for hero in winrates:
        try:
            winrates[hero]['winrateDelta'] = winratesAgainstAntagonist[hero]['winrate'] - winrates[hero]['winrate']
        except TypeError:
            winrates[hero]['winrateDelta'] = 0
    return winrates

def avgDeltas(winrates1,winrates2,multiplierForWinrates1=1):
    #modifies the winrates1 dict to average winrateDelta of both passed dicts
#    print "averaging deltas for new hero and "+str(multiplierForWinrates1)+" old heroes"
    for hero in winrates1:
        winrates1[hero]['winrateDelta'] = (winrates1[hero]['winrateDelta'] * multiplierForWinrates1 + winrates2[hero]['winrateDelta'])/(multiplierForWinrates1+1)

def printTopHeroes(winrates,sortKey='winrate',numHeroes=3):
    #prints the top n heroes by creating a copy of the dict passed in, 
    winratesCopy = winrates
    for num in range(numHeroes):
        hero = getNextTop(winratesCopy,sortKey)
        if not hero[sortKey] == None and hero[sortKey] > 0:
            print "#"+str(num+1)+": "+dotaTools.translateHeroID(hero['id']),hero[sortKey]

#def getWinratesDelta(account,againstHeroID,radiant=None):
#    generalWinrates = getWinrates(account,None,radiant)
#    specificWinrates = getWinrates(account,againstHeroID,radiant)
#    winrateDeltas = {}
#    for heroID in generalWinrates:
#        winrateDeltas[heroID] = {'id':heroID,'generalWinrate':generalWinrates[heroID]['winrate'],'totalGamesOnHero':generalWinrates[heroID]['games'],'gamesAgainstAntagonist':specificWinrates[heroID]['games']}
#        try:
#            winrateDeltas[heroID]['winrateDelta'] = specificWinrates[heroID]['winrate'] - generalWinrates[heroID]['winrate']
#        except TypeError:
#            winrateDeltas[heroID]['winrateDelta'] = None
#        try:
##            winrateDeltas[heroID]['weightedWinrate'] = (generalWinrates[heroID]['winrate'] * specificWinrates[heroID]['games'] + winrateDeltas[heroID]['winrateDelta'] * (generalWinrates[heroID]['games']-specificWinrates[heroID]['games'])) / generalWinrates[heroID]['games']
#            winrateDeltas[heroID]['weightedWinrate'] = (generalWinrates[heroID]['winrate'] * (generalWinrates[heroID]['games']-specificWinrates[heroID]['games']) + winrateDeltas[heroID]['winrateDelta'] * specificWinrates[heroID]['games']) / generalWinrates[heroID]['games']
#        except TypeError:
#            winrateDeltas[heroID]['weightedWinrate'] = None
#    return winrateDeltas
#
#def avgWinrateDeltas(winrate1,winrate2,iterationsOfWinrate1=0):
#    averagedWinrates = {}
#    for heroID in winrate1:
#        averagedWinrates[heroID] = {'id':heroID,'generalWinrate':winrate1[heroID]['generalWinrate'],'totalGamesOnHero':winrate1[heroID]['totalGamesOnHero']}
#        try:
#            averagedWinrates[heroID]['weightedWinrate'] = (winrate1[heroID]['weightedWinrate']*(iterationsOfWinrate1+1) + winrate2[heroID]['weightedWinrate']) / (iterationsOfWinrate1+2)
#        except TypeError:
#            averagedWinrates[heroID]['weightedWinrate'] = None
#        try:
#            averagedWinrates[heroID]['winrateDelta'] = (winrate1[heroID]['winrateDelta']*(iterationsOfWinrate1+1) + winrate2[heroID]['winrateDelta']) / (iterationsOfWinrate1+2)
#        except TypeError:
#            averagedWinrates[heroID]['winrateDelta'] = None
#    return averagedWinrates
#
def getFiveHeroes():
    account32 = steamTools.getUserInput32withShortcuts()
    aggregateWinrates = {}
    sideStr = raw_input("Dire or Radiant? any other input will ignore side: ")
    side = None
    if sideStr.lower() == 'radiant':
        side = True
        print "Using radiant stats"
    elif sideStr.lower() == 'dire':
        side = False
        print "using dire stats"
    else:
        print "ignoring side"
    heroes = []
    for heronum in range(5):
        heroes.append(dotaTools.parseHeroName(raw_input("Opponent hero #"+str(heronum+1)+": ")))
        if len(heroes) > 1:
            avgDeltas(aggregateWinrates,getWinratesWithDeltas(account32,heroes[-1],side),heronum)
        else:
            aggregateWinrates = getWinratesWithDeltas(account32,heroes[0],side)
        printTopHeroes(aggregateWinrates,'winrateDelta',10)

getFiveHeroes()

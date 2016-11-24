import dotaTools
import requests
import json

##SIDE IS TRUE FOR RADIANT FALSE FOR DIRE

def getMatches(account,side=None,heroID=None,projectHeroes=False,won=None):
    url = 'https://api.opendota.com/api/players/'+str(account)+'/matches'
    payload = {'significant':1}
    if not side == None:
        payload['is_radiant'] = int(side)
    if projectHeroes:
        payload['project'] = 'heroes'
    if not won == None:
        payload['win'] = int(won)
    if not heroID == None:
        payload['hero_id'] = heroID
    return requests.get(url,params=payload).json()

def getEnemyHeroes(matches):
    #REQUIRES MATCHES OBJECT WHERE PROJECTHEROES WAS PASSED AS TRUE
    enemyHeroes = {}
    for match in matches:
        radiant = match['player_slot'] < 64
        enemyHeroes[match['match_id']] = []
        for player in match['heroes']:
            if radiant:
                if int(player) > 64:
                    enemyHeroes[match['match_id']].append(match['heroes'][player]['hero_id'])
            if not radiant:
                if int(player) < 64:
                    enemyHeroes[match['match_id']].append(match['heroes'][player]['hero_id'])
    return enemyHeroes

def getGeneralHeroWinrate(heroID,account,side=None):
    #returns none if no games played
    totalGames = 0
    wonGames = 0
    allMatches = getMatches(account,side,heroID)
    wonMatches = getMatches(account,side,heroID,False,True)
    for match in allMatches:
        totalGames += 1
    for match in wonMatches:
        wonGames += 1
    print totalGames,wonGames
    try:
        return wonGames/float(totalGames)
    except ZeroDivisionError:
        return None

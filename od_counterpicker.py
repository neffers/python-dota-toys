import dotaTools
import requests
import json

##SIDE IS TRUE FOR RADIANT FALSE FOR DIRE

def getMatches(account,side=None):
    url = 'https://api.opendota.com/api/players/'+str(account)+'/matches'
    payload = {'significant':1}
    if not side == None:
        payload['is_radiant'] = side
    return requests.get(url,params=payload).json()

def getMatchesWithHeroes(account32,side=None):
    url = 'https://api.opendota.com/api/players/'+str(account32)+'/matches'
    payload = {'significant':1,'project':'heroes'}
    if not side == None:
        payload['is_radiant'] = side
    return requests.get(url,params=payload).json()

def getWinratesForHero(heroID,account32):
    #return a heroid indexed dict of winrates (against the index hero), for the given hero
    winRates = {}
    matches = getMatches(account32)

def getGeneralHeroWinrate(heroID,account,side=None):
    #returns none if no games played
    totalGames = 0
    wonGames = 0
    matches = getMatches(account,side)
    for match in matches:
        if int(match['hero_id'])==heroID:
            totalGames += 1
            if match["player_slot"] < 64 and match["radiant_win"]:
                wonGames += 1
            if match["player_slot"] > 64 and not match["radiant_win"]:
                wonGames += 1
    try:
        return wonGames/float(totalGames)
    except ZeroDivisionError:
        return None

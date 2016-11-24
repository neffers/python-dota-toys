import dotaTools
import steamTools
import requests
import json


def getWinratesAgainstHero(account,heroID,radiant=None):
    url = "https://api.opendota.com/api/players/"+str(account)+"/heroes"
    payload = {'significant':1,'against_hero_id':heroID}
    if not radiant == None:
        payload['is_radiant'] = int(radiant)
    heroes = requests.get(url,params=payload).json()
    winrates = {}
    for hero in heroes:
        try:
            winrates[int(hero['hero_id'])] = hero['win']/float(hero['games'])
        except ZeroDivisionError:
            winrates[int(hero['hero_id'])] = None
    return winrates

def getNextTopWinrate(winrates):
    nextTop = max(winrates.keys(),key=winrates.get)
    del winrates[nextTop]
    return nextTop

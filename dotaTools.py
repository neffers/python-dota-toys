import requests
import json
import re

masterHeroList = None


def getLegsLegacy(heroid):
    #get legs from manually built list
    legArray = []
    for i in range(113):
        legArray.append(0)
    legArray[0] = 2
    legArray[1] = 2
    legArray[2] = 4
    legArray[3] = 2
    legArray[4] = 2
    legArray[5] = 2
    legArray[6] = 2
    legArray[7] = 2
    legArray[8] = 2
    legArray[9] = 0
    legArray[10] = 0
    legArray[11] = 2
    legArray[12] = 2
    legArray[13] = 2
    legArray[14] = 0
    legArray[15] = 6
    legArray[16] = 2
    legArray[17] = 2
    legArray[18] = 2
    legArray[19] = 2
    legArray[20] = 2
    legArray[21] = 2
    legArray[22] = 2
    legArray[23] = 1024
    legArray[24] = 2
    legArray[25] = 2
    legArray[26] = 2
    legArray[27] = 0
    legArray[28] = 2
    legArray[29] = 2
    legArray[30] = 2
    legArray[31] = 2
    legArray[32] = 0
    legArray[33] = 2
    legArray[34] = 2
    legArray[35] = 2
    legArray[36] = 2
    legArray[37] = 2
    legArray[38] = 2
    legArray[39] = 0
    legArray[40] = 2
    legArray[41] = 2
    legArray[42] = 2
    legArray[43] = 2
    legArray[44] = 2
    legArray[45] = 2
    legArray[46] = 0
    legArray[47] = 2
    legArray[48] = 2
    legArray[49] = 2
    legArray[50] = 2
    legArray[51] = 4
    legArray[52] = 2
    legArray[53] = 2
    legArray[54] = 2
    legArray[55] = 2
    legArray[56] = 2
    legArray[57] = 4
    legArray[58] = 2
    legArray[59] = 2
    legArray[60] = 8
    legArray[61] = 2
    legArray[62] = 4
    legArray[63] = 2
    legArray[64] = 2
    legArray[65] = 2
    legArray[66] = 0
    legArray[67] = 2
    legArray[68] = 2
    legArray[69] = 2
    legArray[70] = 2
    legArray[71] = 2
    legArray[72] = 2
    legArray[73] = 2
    legArray[74] = 2
    legArray[75] = 4
    legArray[76] = 2
    legArray[77] = 2
    legArray[78] = 2
    legArray[79] = 2
    legArray[80] = 2
    legArray[81] = 2
    legArray[82] = 2
    legArray[83] = 2
    legArray[84] = 2
    legArray[85] = 2
    legArray[86] = 2
    legArray[87] = 6
    legArray[88] = 0
    legArray[89] = 2
    legArray[90] = 0
    legArray[91] = 2
    legArray[92] = 2
    legArray[93] = 0
    legArray[94] = 2
    legArray[95] = 4
    legArray[96] = 4
    legArray[97] = 2
    legArray[98] = 2
    legArray[99] = 2
    legArray[100] = 2
    legArray[101] = 2
    legArray[102] = 2
    legArray[103] = 2
    legArray[104] = 6
    legArray[105] = 2
    legArray[106] = 2
    legArray[107] = 4
    legArray[108] = 2
    legArray[109] = 2
    legArray[110] = 2
    legArray[111] = 2
    legArray[112] = 2

    return legArray[heroid-1]


def buildList():
    #use requests to get json of hero data from github
    url = "https://raw.githubusercontent.com/dotabuff/d2vpkr/master/dota/scripts/npc/npc_heroes.json"
    r = requests.get(url)
    j = r.json()
    heroes = j["DOTAHeroes"]
    global masterHeroList
    masterHeroList = {}
    for hero in heroes:
        herodata = heroes[hero]
        if not (herodata == "1" or hero == 'npc_dota_hero_base' or hero == 'npc_dota_hero_target_dummy'):
            masterHeroList[herodata['HeroID']] = {}
            masterHeroList[herodata['HeroID']]['names'] = [herodata['url']]
            if "_" in herodata['url']:
                masterHeroList[herodata['HeroID']]['names'].append(herodata['url'].replace('_',' '))
            try:
                masterHeroList[herodata['HeroID']]['names'].append(herodata['NameAliases'])
            except KeyError:
                pass
            try:
                masterHeroList[herodata['HeroID']]['legs'] = herodata['Legs']
            except KeyError:
                masterHeroList[herodata['HeroID']]['legs'] = heroes['npc_dota_hero_base']['Legs']

def getLegs(heroID):
    if not masterHeroList:
        buildList()
    return int(masterHeroList[str(heroID)]['legs'])

def parseHeroName(heroInput):
    if not masterHeroList:
        buildList()
    for hero in masterHeroList:
        for name in masterHeroList[hero]['names']:
            if heroInput.lower() == name.lower():
                return int(hero)
    #regex this time
    for hero in masterHeroList:
        for name in masterHeroList[hero]['names']:
            if re.search(heroInput,name,re.I):
                return int(hero)

def getHeroes():
    #return the list of heroes
    if not masterHeroList:
        buildList()
    return masterHeroList

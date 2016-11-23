import json
import requests
from dotaTools import getLegs
from steamTools import getUserInput32

initialInput = raw_input("Enter whose stats you want, or enter a different account: ")
if initialInput == "jake":
    account = 100944432
elif initialInput == 'mary':
    account = 104426156
elif initialInput == 'me':
    account = 50557119
elif initialInput == 'ccnc':
    account = 221666230
else:
    account = getUserInput32(initialInput)
url = "https://api.opendota.com/api/players/"+str(account)+"/matches?significant=1"
totalDeaths = 0
winDeaths = 0
lossDeaths = 0
#winKills = 0
#lossKills = 0
#winAssists = 0
#lossAssists = 0
legGames = [0,0,0,0,0]
legWins = [0,0,0,0,0]
legLosses = [0,0,0,0,0]
legDeaths = [0,0,0,0,0]
lossLegDeaths = [0,0,0,0,0]
winLegDeaths = [0,0,0,0,0]
won = False
wins = 0
losses = 0


r = requests.get(url)
j = r.json()
for m in j:
    if m["player_slot"] < 64:
        if m["radiant_win"]:
            winDeaths += m["deaths"]
            winLegDeaths[getLegs(m["hero_id"])/2] += m["deaths"]
            won = True
            wins += 1
            legWins[getLegs(m["hero_id"])/2] += 1
        else:
            lossDeaths += m["deaths"]
            lossLegDeaths[getLegs(m["hero_id"])/2] += m["deaths"]
            won = False
            losses += 1
            legLosses[getLegs(m["hero_id"])/2] += 1
    else:
        if m["radiant_win"]:
            lossDeaths += m["deaths"]
            lossLegDeaths[getLegs(m["hero_id"])/2] += m["deaths"]
            won = False
            losses += 1
            legLosses[getLegs(m["hero_id"])/2] += 1
        else:
            winDeaths += m["deaths"]
            winLegDeaths[getLegs(m["hero_id"])/2] += m["deaths"]
            won = True
            wins += 1
            legWins[getLegs(m["hero_id"])/2] += 1

    legGames[getLegs(m["hero_id"])/2] += 1
    legDeaths[getLegs(m["hero_id"])/2] += m["deaths"]
    totalDeaths += m["deaths"]
    print j.index(m),m["match_id"],m["deaths"],won,getLegs(m["hero_id"])

legAvgs = [0,0,0,0,0]
legWinAvgs = [0,0,0,0,0]
legLossAvgs = [0,0,0,0,0]
legWinrate = [0,0,0,0,0]
for i in range(5):
    try:
        legAvgs[i] = round(legDeaths[i]/float(legGames[i]),3)
        legWinAvgs[i] = round(winLegDeaths[i]/float(legWins[i]),3)
        legLossAvgs[i] = round(lossLegDeaths[i]/float(legLosses[i]),3)
        legWinrate[i] = round(legWins[i]/float(legGames[i]),3)
    except ZeroDivisionError:
        pass

print "Total:",totalDeaths,totalDeaths / float(len(j)),"in",len(j),wins/float(len(j))*100
print "Won:",winDeaths,winDeaths / float(wins),"in",wins
print "Lost:",lossDeaths,lossDeaths / float(losses),"in",losses
print "Deaths per leg group (0,2,4,6,8):",legDeaths,legAvgs
#print "this should match the first array above:",[x+y for x,y in zip(winLegDeaths,lossLegDeaths)]
print "Games, wins, losses, winrate per leg group:",legGames,legWins,legLosses,legWinrate
print "Deaths per leg group (wins):",winLegDeaths,legWinAvgs
print "Deaths per leg group (losses):",lossLegDeaths,legLossAvgs

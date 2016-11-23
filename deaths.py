import json
import requests

key = "9CE5753981573AA07519A73EE377341B"
#account = 76561198064691884
account = input("Enter your steamid64: ")
dota_account = account - 76561197960265728
payload = {'key':key,'account_id':account,'matches_requested':99999,'start_at_match_id':"null"}
url="http://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1"
done = False
matches = []
totalDeaths = 0

while done == False:
    r = requests.get(url,params=payload)
    j = r.json()
    m = j["result"]["matches"]

    for n in m:
        print n["match_id"]
        matches.append(n["match_id"])

    payload["start_at_match_id"] = m[-1]["match_id"]-1
    if j["result"]["results_remaining"] == 0:
        done = True

#match = 2784041045
url = "http://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1"
for match in matches:
#while match == 2784041045:
    payload = {'key':key,'match_id':match}
    r = requests.get(url,params=payload)
    j = r.json()
    p = j['result']['players']
    for player in p:
        #print player, "\n\n"
        if player['account_id'] == dota_account:
            totalDeaths += player['deaths']
            print matches.index(match),player['deaths'],totalDeaths
            #print player['deaths']
    match = 0
print totalDeaths
print totalDeaths / float(len(matches))
#print len(matches)
#print 12

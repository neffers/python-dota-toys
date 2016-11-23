import secret
import re
import requests
import json

magicSteamNumber = 76561197960265728

def getUserInput():
    return raw_input("Enter Steam id: ")

def sanitizeURL(url):
    sanitizeCheck = re.compile('/')
    if sanitizeCheck.search(url):
        return url[:sanitizeCheck.search(url).end()-1]
    else:
        return url

def getUserInput64(argInput):
    if argInput:
        genericInput = argInput
    else:
        genericInput = getUserInput()

    #if userinput is what appears to be a steamid32/64, return it (64)
    #or convert from 32 to 64 and then return

    try:
        genericInput = int(genericInput)
        if genericInput > magicSteamNumber:
            return genericInput
        if genericInput < magicSteamNumber:
            return genericInput + magicSteamNumber
    except ValueError:
        pass
    
    #attempt to parse and convert using steam web API
    vanityCheck = re.compile('id/')
    profileCheck = re.compile('profiles/')
    if vanityCheck.search(genericInput):
        vanityURL = sanitizeURL(genericInput[vanityCheck.search(genericInput).end():])
        
        #use steam web api to get steam id from vanity url
        apiURL = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/"
        payload = {'key':secret.steamKey,'vanityurl':vanityURL}
        r = requests.get(apiURL,params=payload)
        j = r.json()
        return int(j['response']['steamid'])

    elif profileCheck.search(genericInput):
        return int(sanitizeURL(genericInput[profileCheck.search(genericInput).end():]))

    #check if string entered was the vanity url
    else:
        apiURL = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/"
        payload = {'key':secret.steamKey,'vanityurl':sanitizeURL(genericInput)}
        r = requests.get(apiURL,params=payload)
        j = r.json()
        return int(j['response']['steamid'])

        
def getUserInput32(argInput):
    return getUserInput64(argInput) - magicSteamNumber

def getUserInput32withShortcuts():
    i = raw_input("Whose stats are we getting: ")
    if i == 'jake':
        return 100944432
    elif i == 'mary':
        return 104426156
    elif i == 'me':
        return 50557119
    elif i == 'ccnc':
        return 221666230
    else:
        return getUserInput32(i)


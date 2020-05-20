from json import load
from random import randint
from functools import reduce
from math import ceil

SIDE = 'side'

def loadRoles():
	with open('roles.json') as roles:
		return load(roles)

def createEvil(numPlayers, roles):
	possibleRoles = list(filter(lambda x: x[SIDE] == 'werewolf' or x[SIDE] == 'vampire', roles))
	return selectRandomRoles(possibleRoles, ceil(numPlayers / 7))

def createGood(sumEvil, roles, numGoodPlayers):
	goodRoles = list(filter(lambda role: role[SIDE] == 'villagers', roles))
	beneficialRoles = list(filter(lambda role: role['value'] > 0, goodRoles))
	harmfulRoles = list(filter(lambda role: role['value'] <= 0, goodRoles))
	sumGood = 0
	selectedRoles = []
	while (len(selectedRoles) < numGoodPlayers):
		playersRemaining =  numGoodPlayers - len(selectedRoles)
		role = tryToAutoBalanceRoles(beneficialRoles, harmfulRoles, sumGood, sumEvil, playersRemaining == 1)
		sumGood += role['value']
		selectedRoles.append(role)
	return selectedRoles
 
def tryToAutoBalanceRoles(beneficialRoles, harmfulRoles, sumGood, sumEvil, lastRound):
	totalSum = sumGood + sumEvil
	if (totalSum <= 0):
		if (lastRound):
			return balanceLastRound(beneficialRoles, totalSum)
		return selectRandomRole(beneficialRoles)
	else:
		if (lastRound):
			return balanceLastRound(harmfulRoles, totalSum)
		return selectRandomRole(harmfulRoles)

def balanceLastRound(roles, totalSum):
	bestRole = {}
	currentValue = None
	for role in roles:
		roleValue = role['value']
		totalValue = abs(totalSum + roleValue)
		if (currentValue is None):
			currentValue = totalValue
			bestRole = role
		elif (currentValue > totalValue):
			currentValue = totalValue
			bestRole = role
	return bestRole

def selectRandomRoles(roles, playersOnSide):
	selectedRole = []
	for player in range(playersOnSide):
		selectedRole.append(selectRandomRole(roles))
	return selectedRole

def selectRandomRole(roles):
	return roles[randint(0, len(roles) - 1)]

def determineAdvantage(sumEvil, goodRoles):
	sumGood = sum(map(lambda role: role['value'], goodRoles))
	totalAdvantage = sumEvil + sumGood
	print("Total advantage is %d" % (sumEvil + sumGood))
	if (totalAdvantage == 0):
		return 'Neither side'
	elif (totalAdvantage < 0):
		return "Evil"
	else:
		return "Good"

def generateRoles():
	with open('players.json') as playerData:
		players = load(playerData)
		roles = loadRoles()
		evilRoles = createEvil(len(players), roles)
		sumEvil = reduce((lambda role, sum: role['value'] + role['value']), evilRoles)
		goodRoles = createGood(sumEvil, roles, len(players) - len(evilRoles))
		print("%s has the advantage" % determineAdvantage(sumEvil, goodRoles))
		totalRoles = evilRoles + goodRoles
		writeRoles(players, totalRoles)
		
def writeRoles(players, allRoles):
	roleDescriptions = {}
	playerRolesOutput = []
	for player in players:
		role = allRoles.pop(randint(0, len(allRoles) - 1))
		roleName = role['role']
		playerRolesOutput.append("%s - %s" % (player, roleName))
		roleDescriptions[roleName] = role['description']
	writeArrayToFile(playerRolesOutput, "playerRoles.txt")
	writeJsonToFile(roleDescriptions, 'roleDescription.txt')


def writeArrayToFile(arrayOutput, filename):
	arrayAsString = "\n".join(arrayOutput)
	with open(filename, 'w') as outputFile:
		outputFile.write(arrayAsString)

def writeJsonToFile(jsonOutput, filename):
	outputStr = ""
	for key in jsonOutput:
		outputStr += "%s: %s\n" % (key, jsonOutput[key])
	with open(filename, 'w') as outputFile:
		outputFile.write(outputStr)

			
generateRoles()
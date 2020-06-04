from cricVis.models import *

def checkIfKeyExists(dictionary,key):
	try:
		check = dictionary[key]
		return True
	except:
		return False

def getSetOfOvers(match):
	overs={}
	for over in match:
		overs[over]=0
	return overs

def getColumnValue(column_value):
	value = column_value.split("_")[1]
	return int(value)

def getImageName(team):
	return teamImageName[team]

def convertValueToColumn(value,columnName):
	return columnName+"_"+str(value)

def getTeamName(matchID,team):
	match = db.reference('/MatchDescription').child(matchID).get()
	return str(match[team])

# gets the runs, breakdown of runs, and over number for a team in a given over
def getOverStatsOfTeam(overDetails,team,over):
	overStats = {}
	overStats["over"] = over
	overStats["runs"] = overDetails[team]["runs"]
	overStats["breakdownRuns"] = overDetails[team]["breakdownRuns"]
	return overStats

# gets the player dismissed, bowler, type of dismissal, non-striker player, over number and ball for a team at a given over and ball
def getWicketDetailsOfTeam(wicketDetails,over,ball):
	wicket = {}
	for detail in wicketDetails:
		wicket[detail] = wicketDetails[detail]
	wicket["over"] = over
	wicket["ball"] = ball
	return wicket

def getPlayerTeam(playerName):
	return db.reference('/PlayerDescription').child(playerName).child("team").get()

# get the previous over's cummulative runs, used to calculate current over's cumulative runs
def getPrevOverCumulativeRuns(innings,overNumber):
	for over in innings:
		if over["over"]==overNumber:
			return over["cumulativeRuns"]

# add run rate and cummulative runs statistics to a given innings' stats
def addStatsToInnings(innings):
	for over in innings:
		overNumber = over["over"]
		if overNumber==1:
			over["cumulativeRuns"] = over["runs"]
			over["runRate"] = over["runs"]
			continue
		over["cumulativeRuns"] = over["runs"] + getPrevOverCumulativeRuns(innings,overNumber-1)
		over["runRate"] = over["cumulativeRuns"]/overNumber
	return innings

# Fetches the data for populating the frontend dropdown with matches, which will be list of {matchID:, matchDate:, team1:,team2:}
def getAllData():
	allData = []
	allMatches = ref.child("MatchDescription").get()
	for matchID in allMatches:
		matchData = {}
		match = allMatches[matchID]
		matchData["matchID"] = matchID
		matchData["team1"] = getTeamName(matchID,"team1")
		matchData["team2"] = getTeamName(matchID,"team2")
		# matchData["team1_image"] = getImageName(matchData["team1"])
		# matchData["team2_image"] = getImageName(matchData["team2"])
		matchData["matchDate"] = match["matchDate"]
		allData.append(matchData)
	return allData

# gets the match statistics for batting: for an over, the runs scored and breakdown of runs for each team
def getMatchStats(match_ID):
	matchStats = {}
	team1 = getTeamName(match_ID,"team1")
	team2 = getTeamName(match_ID,"team2")
	matchStats[team1] = []
	matchStats[team2] = []
	match = db.reference('/MatchStats').child(match_ID).get()
	# the set of overs in which any of teams played
	overs = getSetOfOvers(match)
	for over in overs:
		overDetails = match[over]
		overNumber = getColumnValue(over)
		if checkIfKeyExists(overDetails,team1):
			team1OverStats = getOverStatsOfTeam(overDetails,team1,overNumber)
			matchStats[team1].append(team1OverStats)
		if checkIfKeyExists(overDetails,team2):
			team2OverStats = getOverStatsOfTeam(overDetails,team2,overNumber)
			matchStats[team2].append(team2OverStats)
	matchStats[team1] = addStatsToInnings(matchStats[team1])
	matchStats[team2] = addStatsToInnings(matchStats[team2])
	return matchStats
# gets the match statistics for bowling: for an over and ball, the player dismissed, the bowler, type of dismissal and non striker for each team
def getPlayersDismissed(match_ID):
	playersDismissed = {}
	teamNames = getTeamNames(match_ID)
	team1, team2 = teamNames["team1"], teamNames["team2"]
	playersDismissed[team1], playersDismissed[team2] = [], []
	match = db.reference('/MatchDismissal').child(match_ID).get()
	# the set of overs in which any of teams played
	overs = getSetOfOvers(match)
	for over in overs:
		overDetails = match[over]
		for ball in range(1,7):
			ballColumn = convertValueToColumn(ball,"ball")
			if checkIfKeyExists(overDetails, ballColumn):
				wicketDetails = overDetails[ballColumn]
				overNumber = getColumnValue(over)
				if checkIfKeyExists(wicketDetails,team1):
					playersDismissed[team1].append(getWicketDetailsOfTeam(wicketDetails[team1],overNumber,ball))
				if checkIfKeyExists(wicketDetails,team2):
					playersDismissed[team2].append(getWicketDetailsOfTeam(wicketDetails[team2],overNumber,ball))
	return playersDismissed

# gets teamNames of the given match in a JSON format (a helper function needed in views.py)
def getTeamNames(match_ID):
	teamNames = {}
	teamNames["team1"] = getTeamName(match_ID,"team1")
	teamNames["team2"] = getTeamName(match_ID,"team2")
	return teamNames

# gets the players playing in a particular match and group them by their team
def getPlayersPlaying(match_ID):
	teamNames = getTeamNames(match_ID)
	team1 = teamNames["team1"]
	team2 = teamNames["team2"]
	playersPlaying = {team1: [], team2: []}
	playersOfMatch = db.reference('/PlayerMatch').child(match_ID).get()
	for player in playersOfMatch:
		team = getPlayerTeam(player)
		playersPlaying[team].append(player)
	return playersPlaying

# gets the details: innings, match date, player of match, result of match, season, first team, second team, venue, win by runs, win by wickets for a given match
def getMatchDetails(match_ID):
	match = db.reference('/MatchDescription').child(match_ID).get()
	matchDetails = {}
	matchDetails["matchID"] = getColumnValue(match_ID)
	for detail in match:
		matchDetails[detail] = match[detail]
	return matchDetails

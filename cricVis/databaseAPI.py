import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate('cricVis/static/cricVis/cricvistesting-firebase-adminsdk-b4xg8-af8c48bb20.json')

firebase_admin.initialize_app(cred, {
	'databaseURL' : 'https://cricvistesting.firebaseio.com/'
})

ref = db.reference('/')

def getColumnValue(column_value):
	value = column_value.split("_")[1]
	return int(value)

def convertValueToColumn(value,columnName):
	return columnName+"_"+str(value)

def getTeamName(matchID,team):
	match = db.reference('/MatchDescription').child(matchID).get()
	return str(match[team])

def getOverStatsOfTeam(overDetails,team,over):
	overStats = {}
	overStats["over"] = over
	overStats["runs"] = overDetails[team]["runs"]
	overStats["breakdownRuns"] = overDetails[team]["breakdownRuns"]
	return overStats

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
		if over["over"]==1:
			over["cumulativeRuns"] = over["runs"]
			over["runRate"] = over["runs"]
			break
	for over in innings:
		overNumber = over["over"]
		if overNumber==1:
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
		matchData["matchDate"] = match["matchDate"]
		allData.append(matchData)
	return allData

def getMatchStats(match_ID,numOvers=20):
	matchStats = {}
	team1 = getTeamName(match_ID,"team1")
	team2 = getTeamName(match_ID,"team2")
	matchStats[team1] = []
	matchStats[team2] = []
	match = db.reference('/MatchStats').child(match_ID).get()
	for over in range(1,numOvers+1):
		overDetails = match[convertValueToColumn(over,"over")]
		team1OverStats = getOverStatsOfTeam(overDetails,team1,over)
		team2OverStats = getOverStatsOfTeam(overDetails,team2,over)
		matchStats[team1].append(team1OverStats)
		matchStats[team2].append(team2OverStats)
	matchStats[team1] = addStatsToInnings(matchStats[team1])
	matchStats[team2] = addStatsToInnings(matchStats[team2])
	return matchStats

def getPlayersDismissed(match_ID,numOvers=20):
	playersDismissed = {}
	teamNames = getTeamNames(match_ID)
	team1, team2 = teamNames["team1"], teamNames["team2"]
	playersDismissed[team1], playersDismissed[team2] = [], []
	match = db.reference('/MatchDismissal').child(match_ID).get()
	print(match,team1,team2)
	for over in range(1,numOvers+1):
		try:
			overDetails = match[convertValueToColumn(over,"over")]
			print(overDetails)
			for ball in range(1,7):
				try:
					wicketDetails = overDetails[convertValueToColumn(ball,"ball")]
					try:
						playersDismissed[team1].append(getWicketDetailsOfTeam(wicketDetails[team1],over,ball))
					except:
						pass

					try:
						playersDismissed[team2].append(getWicketDetailsOfTeam(wicketDetails[team2],over,ball))
					except:
						pass
				except:
					pass
		except:
			pass
	return playersDismissed

# gets teamNames of the given match in a JSON format (a helper function needed in views.py)
def getTeamNames(match_ID):
	teamNames = {}
	teamNames["team1"] = getTeamName(match_ID,"team1")
	teamNames["team2"] = getTeamName(match_ID,"team2")
	return teamNames

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

def getMatchDetails(match_ID):
	match = db.reference('/MatchDescription').child(match_ID).get()
	matchDetails = {}
	matchDetails["matchID"] = getColumnValue(match_ID)
	for detail in match:
		matchDetails[detail] = match[detail]
	return matchDetails
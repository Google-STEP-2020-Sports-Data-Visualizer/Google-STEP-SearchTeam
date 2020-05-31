import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate('static/cricVis/firebase-sdk.json')

firebase_admin.initialize_app(cred, {
	'databaseURL' : 'https://trial-1-9f3d9.firebaseio.com/'
})

ref = db.reference('/')

x = ref.child("-M8J1KnUyAQY4s7UxoJl").get()
print(x)

def getTeamName(matchID,team):
	allMatches = ref.child("MatchDescription").get()
	return allMatches[matchID][team]

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



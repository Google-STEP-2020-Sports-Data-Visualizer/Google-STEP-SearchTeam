from django.shortcuts import render

# Create your views here.
def index(request):
    # sent a GET request to get match_ID, team1, team2, match date
    # assemble this data like [{match_ID: , team1: , team2: ,date: }, {....}]
    allMatches=[{"match_ID":1,"team1":"Sunrisers Hyderbad", "team2": "Mumbai Indians","date":"18/04/2017"},{"match_ID":2,"team1":"Rajasthan Royals", "team2": "Mumbai Indians","date":"20/04/2017"}]
    context = { "allMatches": allMatches}
    return render(request,'cricVis/index.html',context)

def fetchGraphData(request):
    if request.method == "GET":
        matchID = request.GET['matchID']
        matchStats = getMatchStats(matchID)
        playersDismissed =  playerDismissed(match_ID)
        teams = teamNames(matchID)
        
from django.shortcuts import render
from django.http import Http404, HttpResponse
import json
from cricVis.databaseAPI import *
# Create your views here.
def index(request):
    # sent a GET request to get match_ID, team1, team2, match date
    # assemble this data like [{match_ID: , team1: , team2: ,date: }, {....}]
    allMatches = getAllData()
    context = { "allMatches": allMatches}
    return render(request,'cricVis/index.html',context)

# creates the inningsDetails JSON in the required format
def getInnningsDetails(matchStats,playersDismissed,teamName,chartParameter):
    inningsDetails = {}
    inningsDetails["teamName"] = teamName
    overs=[]
    for record in matchStats:
        over={}
        over["overNumber"]=record["over"]
        over[chartParameter]=record[chartParameter]
        over["playersDismissed"]=[]
        for wicket in playersDismissed:
            if wicket["over"]==record["over"] and wicket["playerDismissed"]!="":
                over["playersDismissed"].append(wicket["playerDismissed"])
        overs.append(over)
    inningsDetails["overs"]=overs
    return inningsDetails

# creates the chartData JSON for the entire match ie both the innnings in the required chart format
def getChartData(matchID,matchStats,playersDismissed,teams,chartParameter):
    chartData={}
    chartData["matchID"]=matchID
    team1=teams["team1"]
    team2=teams["team2"]
    chartData["team1"]=getInnningsDetails(matchStats[team1],playersDismissed[team1],team1,chartParameter)
    chartData["team2"]=getInnningsDetails(matchStats[team2],playersDismissed[team2],team2,chartParameter)
    return chartData

def getChartResponse(matchID,matchStats,playersDismissed,teams):
    wormChartData = getChartData(matchID,matchStats,playersDismissed,teams,"cumulativeRuns")
    manhattanChartData = getChartData(matchID,matchStats,playersDismissed,teams,"runs")
    runRateChartData = getChartData(matchID,matchStats,playersDismissed,teams,"runRate")
    chartData={"wormChartData": wormChartData, "manhattanChartData": manhattanChartData, "runRateChartData": runRateChartData}
    return chartData

# returns the chart response for all three kinds of charts in their described JSON format
def fetchGraphData(request):
    if request.method == "GET":
        matchID = request.GET['matchID']
        matchStats = getMatchStats(matchID)
        playersDismissed =  getPlayersDismissed(matchID)
        teams = getTeamNames(matchID)

        return HttpResponse(json.dumps(getChartResponse(matchID,matchStats,playersDismissed,teams)))

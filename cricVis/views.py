from django.shortcuts import render
from django.http import Http404, HttpResponse
import json

# Create your views here.
def index(request):
    # sent a GET request to get match_ID, team1, team2, match date
    # assemble this data like [{match_ID: , team1: , team2: ,date: }, {....}]
    allMatches=[{"match_ID":1,"team1":"Sunrisers Hyderbad", "team2": "Mumbai Indians","date":"18/04/2017"},{"match_ID":2,"team1":"Rajasthan Royals", "team2": "Mumbai Indians","date":"20/04/2017"}]
    context = { "allMatches": allMatches}
    return render(request,'cricVis/index.html',context)

def getInnningsDetails(matchStats,playersDismissed,teamName,chartParameter):
    inningsDetails = {}
    inningsDetails["teamName"] = teamName
    overs=[]
    for record in matchStats:
        over={}
        over["overNumber"]=record["over"]
        over[chartParameter]=record[chartParameter]
        over["players_dismissed"]=[]
        for wicket in playersDismissed:
            if wicket["over"]==record["over"] and wicket["player_dismissed"]!="":
                over["player_dismissed"].append(wicket["player_dismissed"])
        overs.append(over)
    inningsDetails["overs"]=overs
    return inningsDetails

def getChartData(matchID,matchStats,playersDismissed,teams,chartParameter):
    chartData={}
    chartData["matchID"]=matchID
    inningsDetails1=getInnningsDetails(matchStats["team1"],playersDismissed["team1"],teams["team1"],chartParameter)
    inningsDetails2=getInnningsDetails(matchStats["team2"],playersDismissed["team2"],teams["team2"],chartParameter)
    chartData["team1"]=inningsDetails1
    chartData["team2"]=inningsDetails2
    return chartData

def fetchGraphData(request):
    if request.method == "GET":
        matchID = request.GET['matchID']
        matchStats = getMatchStats(matchID)
        playersDismissed =  playerDismissed(match_ID)
        teams = teamNames(matchID)
        wormChartData = getChartData(matchID,matchStats,playersDismissed,teams,"cumulativeRuns")
        manhattanChartData = getChartData(matchID,matchStats,playersDismissed,teams,"runs")
        runRateChartData = getChartData(matchID,matchStats,playersDismissed,teams,"runRate")
        chartData={"wormChartData": wormChartData, "manhattanChartData": manhattanChartData, "runRateChartData": runRateChartData}
        return HttpResponse(json.dumps(chartData))
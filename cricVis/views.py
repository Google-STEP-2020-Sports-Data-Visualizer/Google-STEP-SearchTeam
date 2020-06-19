from django.shortcuts import render
from django.http import Http404, HttpResponse
import json, threading, queue
from cricVis.databaseAPI import *
from cricVis.timeSeriesAPI import *
# Create your views here.

""" sent a GET request to get match_ID, team1, team2, match date """

def index(request):
    allMatches = getAllData()
    context = { "allMatches": allMatches}
    return render(request,'cricVis/index.html',context)

def iplStats(request):
    return render(request,'cricVis/iplStats.html')

def timeSeries(request):
    return render(request,'cricVis/timeSeries.html')

""" creates the inningsDetails JSON in the required format """

def getInningsDetails(matchStats,playersDismissed,teamName,chartParameter):
    inningsDetails = {}
    inningsDetails["teamName"] = teamName
    overs=[]
    for record in matchStats:
        over={}
        over["overNumber"]=record["over"]
        over["breakdownRuns"]=record["breakdownRuns"]
        over[chartParameter]=record[chartParameter]
        over["playersDismissed"]=[]
        for wicket in playersDismissed:
            if wicket["over"]==record["over"] and wicket["playerDismissed"]!="":
                over["playersDismissed"].append(wicket)
        overs.append(over)
    inningsDetails["overs"]=overs
    return inningsDetails

""" creates the chartData JSON for the entire match ie both the innings in the required chart format """

def getChartData(matchID,matchStats,playersDismissed,teams,chartParameter):
    chartData={}
    chartData["matchID"]=matchID
    team1=teams["team1"]
    team2=teams["team2"]
    chartData["team1"]=getInningsDetails(matchStats[team1],playersDismissed[team1],team1,chartParameter)
    chartData["team2"]=getInningsDetails(matchStats[team2],playersDismissed[team2],team2,chartParameter)
    return chartData

def getChartResponse(matchID,matchStats,playersDismissed,teams):
    wormChartData = getChartData(matchID,matchStats,playersDismissed,teams,"cumulativeRuns")
    manhattanChartData = getChartData(matchID,matchStats,playersDismissed,teams,"runs")
    runRateChartData = getChartData(matchID,matchStats,playersDismissed,teams,"runRate")
    chartData={"wormChartData": wormChartData, "manhattanChartData": manhattanChartData, "runRateChartData": runRateChartData}
    return chartData

""" returns the chart response for all three kinds of charts in their described JSON format """

def fetchGraphData(request):
    if request.method == "GET":
        matchID = request.GET['matchID']
        teams = getTeamNames(matchID)
        matchStats = getMatchStats(matchID,teams)
        playersDismissed =  getPlayersDismissed(matchID,teams)
        allData = {}
        allData["playersPlaying"] = getPlayersPlaying(matchID)
        allData["matchDetails"] = getMatchDetails(matchID)
        allData["chartData"] = getChartResponse(matchID,matchStats,playersDismissed,teams)

        return HttpResponse(json.dumps(allData))
    
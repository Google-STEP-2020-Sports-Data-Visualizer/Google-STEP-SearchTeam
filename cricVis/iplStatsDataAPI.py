from cricVis.models import *

teamsList = []

""" get all the data for graphs to be plotted on IPL charts"""

def getIPLStatsData():
    allTeamsData = getTeamsData()
    allSeaonsData = getSeasonsData()
    allVenuesData = getVenuesData()
    allData = {}
    allData.update(allTeamsData)
    allData.update(allSeaonsData)
    allData.update(allVenuesData)
    allData["teamColour"] = teamColour
    return allData

""" get all data from the TeamWise table in the required format """

def getTeamsData():
    teamsData = db.reference('/TeamWise').get()
    setTeamsList(teamsData)
    print(teamsList)
    allTeamsData = {}
    allTeamsData["teamWins"] = getTeamsWins(teamsData)
    allTeamsData["tossWinsTeams"] = getTeamsTossWins(teamsData)
    allTeamsData["seasonsWinsTeams"] = getTeamsSeasonWins(teamsData)
    allTeamsData["averageScoreTeams"] = getTeamsAvgScore(teamsData)
    return allTeamsData

""" get the list of teams, which will be used later in helper functions """

def setTeamsList(teamsData):
    for team in teamsData:
        teamsList.append(team)

""" get all data from the SeasonWise table in the required format """

def getSeasonsData():
    seasonsData = db.reference('/SeasonWise').get()
    allSeasonsData = {}
    allSeasonsData["finalScoreBatFirst"] = getFinalScoreBatFirst(seasonsData)
    allSeasonsData["lowestScoreTeams"] = getScoreTeamPerSeason(seasonsData,"lowestScore")
    allSeasonsData["highestScoreTeams"] = getScoreTeamPerSeason(seasonsData,"highestScore")
    return allSeasonsData

""" get all data from the VenueWise table in the required format """

def getVenuesData():
    venuesData = db.reference('/VenueWise').get()
    allVenuesData = {}
    allVenuesData["gamesPlayedStadium"]  = getGamesPlayedVenueWise(venuesData)
    return allVenuesData

""" get the total number of matches won by a team: { teamName: numberOfMatchesWon } """

def getTeamsWins(teamsData):
    teamsWins = {}
    for team in teamsData:
        teamsWins[team] = teamsData[team]["matchWins"]
    return teamsWins

""" get the total number of tosses won by a team: { teamName: numberOfTossesWon } """

def getTeamsTossWins(teamsData):
    teamsTossWins = {}
    for team in teamsData:
        teamsTossWins[team] = teamsData[team]["tossWins"]
    return teamsTossWins

""" get the total number of seasons won by a team: { teamName: numberOfSeasonsWon } """

def getTeamsSeasonWins(teamsData):
    teamsSeasonWins = {}
    for team in teamsData:
        if teamsData[team]["seasonWins"] != 0:
            teamsSeasonWins[team] = teamsData[team]["seasonWins"]
    return teamsSeasonWins

""" get the average score of every team over all the seasons: { teamName: averageScore } """

def getTeamsAvgScore(teamsData):
    teamsAvgScore = {}
    for team in teamsData:
        teamsAvgScore[team] = teamsData[team]["averageScore"]
    return teamsAvgScore

""" get the score of a team in the season's final when it batted first {season: {teamName: finalMatchScore }} """

def getFinalScoreBatFirst(seasonsData):
    finalScoreBatFirst = {}
    for season in seasonsData:
        seasonData = seasonsData[season]
        for team in teamsList:
            if team in seasonData and seasonData[team]["finalMatchScoreBatting"] != 0:
                finalScoreBatFirst[season] = {team: seasonData[team]["finalMatchScoreBatting"]}
                break
    return finalScoreBatFirst

""" get the lowest or highest score of every team throughout all the seasons {teamName: {season: score, season: score }} """

def getScoreTeamPerSeason(seasonsData,scoreType):
    teamsScore = {}
    for team in teamsList:
        teamsScore[team] = {}
    for season in seasonsData:
        seasonData = seasonsData[season]
        for team in seasonData:
            teamsScore[team][season] = seasonData[team][scoreType]
    return teamsScore

""" get the number of games played in each city and each stadium { cityName: numberOfMatches }, { stadiumName: numberOfMatches }"""

def getGamesPlayedVenueWise(venuesData):
    stadiumMatches = {}
    for city in venuesData:
        cityData = venuesData[city]
        for stadium in cityData:
            stadiumMatches[stadium] = cityData[stadium]["numberOfMatches"]
    return stadiumMatches

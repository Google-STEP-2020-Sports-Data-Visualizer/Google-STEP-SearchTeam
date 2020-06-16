import pandas as pd
from collections import defaultdict
import json

############# Final Collection
def dataframes_to_json(final_dataframes_grouped):
    match_stats_grouped = final_dataframes_grouped["match_stats_grouped"]
    match_dismissal_grouped = final_dataframes_grouped["match_dismissal_grouped"]
    player_desc_grouped = final_dataframes_grouped["player_desc_grouped"]
    player_match_grouped = final_dataframes_grouped["player_match_grouped"]
    match_desc_grouped = final_dataframes_grouped["match_desc_grouped"]
    season_wise_grouped = final_dataframes_grouped["season_wise_grouped"]
    team_wise_grouped = final_dataframes_grouped["team_wise_grouped"]
    venue_wise_grouped = final_dataframes_grouped["venue_wise_grouped"]
    stadium_city = final_dataframes_grouped["stadium_city"]

    def nested_dict():
        return defaultdict(nested_dict)

    results = nested_dict()

    ###### Define all utility functions
    def match_stats_to_json(match_stats_grouped):
        for row in match_stats_grouped.itertuples():
            matchID = getattr(row, 'Index')[0]
            over = getattr(row, 'Index')[1]
            team = getattr(row, 'Index')[2]
            results["MatchStats"][matchID][over][team]['runs'] = row.runs
            results["MatchStats"][matchID][over][team]['breakdownRuns'] = row.breakdownRuns

        r = json.dumps(results["MatchStats"])
        r = json.loads(r)
        out_file = open("json_output/MatchStats.json", "w")
        json.dump(r, out_file, indent=2)

    def match_dismissal_to_json(match_dismissal_grouped):
        for row in match_dismissal_grouped.itertuples():
            matchID = getattr(row, 'Index')[0]
            over = getattr(row, 'Index')[1]
            ball = getattr(row, 'Index')[2]
            team = getattr(row, 'Index')[3]
            results["MatchDismissal"][matchID][over][ball][team]['playerDismissed'] = row.playerDismissed
            results["MatchDismissal"][matchID][over][ball][team]['nonStriker'] = row.nonStriker
            results["MatchDismissal"][matchID][over][ball][team]['type'] = row.type
            results["MatchDismissal"][matchID][over][ball][team]['bowler'] = row.bowler
            results["MatchDismissal"][matchID][over][ball][team]['fielder'] = row.fielder


        r = json.dumps(results["MatchDismissal"])
        r = json.loads(r)
        out_file = open("json_output/MatchDismissal.json", "w")
        json.dump(r, out_file, indent=2)

    def player_desc_to_json(player_desc_grouped):
        for row in player_desc_grouped.itertuples():
            player = getattr(row, 'Index')[0]
            season = getattr(row, 'Index')[1]
            results["PlayerDescription"][player][season]['team'] = row.team


        r = json.dumps(results["PlayerDescription"])
        r = json.loads(r)
        out_file = open("json_output/PlayerDescription.json", "w")
        json.dump(r, out_file, indent=2)

    def player_match_to_json(player_match_grouped):
        for name, df_group in player_match_grouped:
            player_index = 1

            for row in df_group.itertuples():
                matchID = row.matchID
                results["PlayerMatch"][matchID]["player" + str(player_index)] = row.player
                player_index = player_index + 1


        r = json.dumps(results["PlayerMatch"])
        r = json.loads(r)
        out_file = open("json_output/PlayerMatch.json", "w")
        json.dump(r, out_file, indent=2)

    def match_desc_to_json(match_desc_grouped):
        for name, df_group in match_desc_grouped:
            for row in df_group.itertuples():
                matchID = row.matchID
                results["MatchDescription"][matchID]['matchDate'] = row.matchDate
                results["MatchDescription"][matchID]['season'] = row.season
                results["MatchDescription"][matchID]['venue'] = row.venue
                results["MatchDescription"][matchID]['team1'] = row.team1
                results["MatchDescription"][matchID]['team2'] = row.team2
                results["MatchDescription"][matchID]['tossWinner'] = row.tossWinner
                results["MatchDescription"][matchID]['tossDecision'] = row.tossDecision
                results["MatchDescription"][matchID]['result'] = row.result
                results["MatchDescription"][matchID]['playerOfMatch'] = row.playerOfMatch
                results["MatchDescription"][matchID]['winByRuns'] = row.winByRuns
                results["MatchDescription"][matchID]['winByWickets'] = row.winByWickets


        r = json.dumps(results["MatchDescription"])
        r = json.loads(r)
        out_file = open("json_output/MatchDescription.json", "w")
        json.dump(r, out_file, indent=2)

    def season_wise_to_json(season_wise_grouped):
        for row in season_wise_grouped.itertuples():
            season = getattr(row, 'Index')[0]
            team = getattr(row, 'Index')[1]
            results["SeasonWise"][season][team]['finalMatchScoreBatting'] = row.finalMatchScoreBatting
            results["SeasonWise"][season][team]['lowestScore'] = row.lowestScore
            results["SeasonWise"][season][team]['highestScore'] = row.highestScore


        r = json.dumps(results["SeasonWise"])
        r = json.loads(r)
        out_file = open("json_output/SeasonWise.json", "w")
        json.dump(r, out_file, indent=2)

    def team_wise_to_json(team_wise_grouped):
        for row in team_wise_grouped.itertuples():
            team = row.Index
            results["TeamWise"][team]['matchWins'] = int(row.matchWins)
            results["TeamWise"][team]['seasonWins'] = int(row.seasonWins)
            results["TeamWise"][team]['runnerUps'] = int(row.runnerUps)
            results["TeamWise"][team]['tossWins'] = int(row.tossWins)
            results["TeamWise"][team]['averageScore'] = row.averageScore



        r = json.dumps(results["TeamWise"])
        r = json.loads(r)
        out_file = open("json_output/TeamWise.json", "w")
        json.dump(r, out_file, indent=2)

    def venue_wise_to_json(venue_wise_grouped):
        for row in venue_wise_grouped.itertuples():
            city = getattr(row, 'Index')[0]
            stadium = getattr(row, 'Index')[1]
            results["VenueWise"][city][stadium]['numberOfMatches'] = row.numberOfMatches
            results["VenueWise"][city][stadium]['averageScore'] = row.averageScore



        r = json.dumps(results["VenueWise"])
        r = json.loads(r)
        out_file = open("json_output/VenueWise.json", "w")
        json.dump(r, out_file, indent=2)

    def stadium_city_to_json(stadium_city):
        for name, df_group in stadium_city:
            for row in df_group.itertuples():
                stadium = row.stadium
                results["StadiumCity"][stadium] = row.city


        r = json.dumps(results["StadiumCity"])
        r = json.loads(r)
        out_file = open("json_output/StadiumCity.json", "w")
        json.dump(r, out_file, indent=2)


    # Created dictionaries of same name inside results
    match_stats_to_json(match_stats_grouped)
    match_dismissal_to_json(match_dismissal_grouped)
    player_desc_to_json(player_desc_grouped)
    player_match_to_json(player_match_grouped)
    match_desc_to_json(match_desc_grouped)
    season_wise_to_json(season_wise_grouped)
    team_wise_to_json(team_wise_grouped)
    venue_wise_to_json(venue_wise_grouped)
    stadium_city_to_json(stadium_city)

    # results dictionary is converted to json
    final_collection_json = json.dumps(results)
    final_collection_json = json.loads(final_collection_json)
    out_file = open("json_output/cricVisDatabase.json", "w")
    json.dump(final_collection_json, out_file, indent=2)

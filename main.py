#! /usr/bin/env python3

import race
import graph

tournamentcode = input("Tournament code:")
only_these_players = input("Players to include (lowercase):").split()

#get tournament data from lichess
gamelist = race.getTournamentData(tournamentcode)
starttime, endtime, leaders, teams = race.getTournamentInfo(tournamentcode)

teamdata = None
if leaders:
    teamdata = race.getTeamData(tournamentcode)

#reverse results of removed players
gamelist = race.fixResults(gamelist, only_these_players)

#calculate data points for graphing
graphdata = race.generateRaceData(gamelist)


#generate csv output in flourish format
filename = graph.graphDataFormat(graphdata, starttime, endtime, tournamentcode, teamdata, leaders, teams)

print(f"Data saved to {filename}")

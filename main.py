#! /usr/bin/env python3

import race
import graph

tournamentcode = input("Tournament code:")
removed_players = input("Removed players (lowercase):").split()

#get tournament data from lichess
gamelist = race.getTournamentData(tournamentcode)
starttime, endtime = race.getTournamentTimes(tournamentcode)

#reverse results of removed players
gamelist = race.fixResults(gamelist, removed_players)

#calculate data points for graphing
graphdata = race.generateRaceData(gamelist)


#generate csv output in flourish format
graph.graphDataFormat(graphdata, starttime, endtime, tournamentcode)

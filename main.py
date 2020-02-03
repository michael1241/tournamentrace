#! /usr/bin/env python3

import race
import graph

tournamentcode = input("Tournament code:")

#get tournament data from lichess
gamelist = race.getTournamentData(tournamentcode)
starttime, endtime = race.getTournamentTimes(tournamentcode)

#calculate data points for graphing
graphdata = race.generateRaceData(gamelist)


#generate csv output in flourish format
graph.graphDataFormat(graphdata, starttime, endtime, tournamentcode)

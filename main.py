#! /usr/bin/env python3

import race
import graph

tournamentcode = input("Tournament code:")

#get tournament data from lichess
gamelist = race.getTournamentData(tournamentcode)

#calculate data points for graphing
graphdata = race.generateRaceData(gamelist)


starttime = 1580635800000
endtime =  1580637420000 +1

#generate csv output in flourish format
graph.graphDataFormat(graphdata, starttime, endtime, tournamentcode)

#! /usr/bin/env python3

import os
import json
from datetime import datetime
import random

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation


def graphDataFormat(graphdata, starttime, endtime, tournamentcode, teamdata, leaders, teams):
    resolution = 10000 #every 10 seconds

    timepoints = range(starttime, endtime + 1, resolution)

    players = {p: [[starttime, 0]] for p in graphdata.keys()}

    for timepoint in timepoints[1:]:
        for player, scores in graphdata.items():
            if scores:
                if scores[0][0] < timepoint:
                    players[player].append([timepoint, scores.pop(0)[1]]) #append with current timepoint score
                else:
                    players[player].append([timepoint, players[player][-1][-1]]) #append current timepoint with with last recorded score
            else:
                players[player].append([timepoint, players[player][-1][-1]])

    frames = []

    for player, scores in players.items():
        df = pd.DataFrame(scores, columns =['time', 'score'], dtype = int)
        df['player'] = player
        frames.append(df)
    data = pd.concat(frames)
    data = data.pivot(index='player', columns='time', values='score')

    new_format = []
    for col in data.columns:
        relative_time = endtime - col
        timeleft = datetime.utcfromtimestamp(relative_time//1000).strftime('%H:%M')
        new_format.append(timeleft)
    data.columns = new_format

    if teamdata:
        teamdict = {}
        for player in teamdata:
            player = json.loads(player)
            title = player.get('title')
            teamdict[title + " " + player['username'] if title else player['username']] = teams[player['team']]
        data = data.reset_index()
        data.insert(loc=1, column='team', value=data['player'].map(teamdict))
        data = data.drop(columns=['player'])
        data = data.set_index('team')
        teamdata = data.iteritems()
        cols = []
        for col in teamdata:
            col = pd.Series(col[1])
            col = col.groupby('team').apply(lambda grp: grp.nlargest(leaders).sum())
            cols.append(col)
        data = pd.concat(cols, axis=1, keys=[s.name for s in cols])
        data = data.reset_index()

    filename = f'{tournamentcode}_output.csv'
    data.to_csv(filename, index=True)

    return filename


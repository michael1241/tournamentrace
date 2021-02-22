#! /usr/bin/env python3

import os
import json
from datetime import datetime
import random

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation


def graphDataFormat(graphdata, starttime, endtime, tournamentcode):
    resolution = 10000 #every 10 seconds

    timepoints = range(starttime, endtime, resolution)

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

    data.to_csv(f'{tournamentcode}_output.csv')


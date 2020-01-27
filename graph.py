#! /usr/bin/env python3

import os
import json
from datetime import datetime
import random

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation

from race import generateRaceData

if os.path.exists('graphdata'):
    with open('graphdata', 'r') as f:
        graphdata = json.load(f)
else:
    graphdata = generateRaceData()
    with open('graphdata', 'w') as f:
        json.dump(graphdata, f)


resolution = 60000 #every 60 seconds
starttime = 1579114800000 #maybe generate automatically from first game end time
endtime = 1579122000000

players = {p: [[starttime, 0]] for p in graphdata.keys()}


for timepoint in range(starttime, endtime, resolution):
    for player, scores in graphdata.items():
        try:
            if scores[0][0] < timepoint:
                players[player].append([timepoint, scores.pop(0)[1]]) #append with current timepoint score
            else:
                players[player].append([timepoint, players[player][-1][-1]]) #append current timepoint with with last recorded score
        except IndexError:
            pass

frames = []

for player, results in players.items():
    df = pd.DataFrame(results, columns =['time', 'score'], dtype = int)
    df['player'] = player
    frames.append(df)
data = pd.concat(frames)

r = lambda: random.randint(0,255)
colors = dict(zip(players.keys(), ['#%02X%02X%02X' % (r(),r(),r()) for x in range(len(players))]))

def drawChart(current_time):
    dff = (data[data['time'].eq(current_time)]
           .sort_values(by='score', ascending=False)
           .head(10))
    ax.clear()

    dff = dff[::-1]
    ax.barh(dff['player'], dff['score'], color=[colors[x] for x in dff['player']])

    clock = datetime.utcfromtimestamp(current_time//1000).strftime('%H:%M') #%H:%M:%S if adding seconds

    for i, (score, player) in enumerate(zip(dff['score'], dff['player'])):
        ax.text(score, i, player, ha='right')
        ax.text(score, i, score, ha='left')
    ax.text(1, 0.4, clock, transform=ax.transAxes, color='#777777', size=46, ha='right', weight=800)
    ax.tick_params(axis='x', colors='#777777', labelsize=12)
    ax.set_yticks([])
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    ax.text(0, 1.05, 'Lichess Titled Arena Jan 2020 Replay', transform=ax.transAxes, size=24, weight=600, ha='left')

fig, ax = plt.subplots(figsize=(15, 8))
animator = animation.FuncAnimation(fig, drawChart, frames=range(starttime+resolution, endtime, resolution))

animator.save('file.mp4')

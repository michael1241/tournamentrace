#! /usr/bin/env python3

import json

#start with JSON
#generate list for each player with (game end time, result, berserk)
#convert to player: (time, points) for graphing

def generateRaceData():
    with open('jan20lta.json', 'r') as f:
        gamelist = f.readlines()

    with open('berserktest', 'r') as r:
        berserks = json.load(r)

    players = {}

    def appendOrCreate(player, gamedata):
        if players.get(player):
            players[player].append(gamedata)
        else:
            players[player] = [gamedata]

    def getResult(game):
        winner = game.get('winner')
        if winner:
            if winner == 'white':
                return {'white': 'w', 'black': 'l'}
            if winner == 'black':
                return {'white': 'l', 'black': 'w'}
        return {'white': 'd', 'black': 'd'}

    def scoreConvert(results):
        chronoresults = sorted(results, key=lambda results: results['time'])
        scores = []
        score = 0
        streak = 0
        for game in chronoresults:
            if game['result'] == 'w':
                score += 2
                if streak >= 2:
                    score += 2
                if game['berserk']:
                    score += 1
                scores.append((game['time'], score))
                streak += 1
            elif game['result'] == 'd':
                if streak >= 2:
                    score += 2
                else:
                    score += 1
                scores.append((game['time'], score))
                streak = 0
            elif game['result'] == 'l':
                scores.append((game['time'], score))
                streak = 0
        return scores

    for g in gamelist:
        game = json.loads(g)
        result = getResult(game)
        berserk = berserks[game['id']]
        appendOrCreate(game['players']['white']['user']['id'], {'time': game['lastMoveAt'], 'result': result['white'], 'berserk': berserk['white']})
        appendOrCreate(game['players']['black']['user']['id'], {'time': game['lastMoveAt'], 'result': result['black'], 'berserk': berserk['black']})

    graphdata = {}

    for player, results in players.items():
        graphdata[player] = scoreConvert(results)
    return graphdata

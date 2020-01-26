#! /usr/bin/env python3
import sys
import chess.pgn
import json

def getBerserks():
    pgn = open('jan20lta.pgn')
    berserks = {} #{'in1s28aj': {'white': true, 'black': false}}

    while True:
        game = chess.pgn.read_game(pgn)
        if not game:
            break
        idnum = game.headers['Site'][-8:]
        blackberserk = whiteberserk = False
        for n, move in enumerate(game):
            if n == 0:
                whiteberserk = move.comment[-3] == '3'
            elif n == 1:
                blackberserk = move.comment[-3] == '3'
            else:
                break
        berserks[idnum] = {'white': whiteberserk, 'black': blackberserk}
    return json.dump(berserks)

print(getBerserks())

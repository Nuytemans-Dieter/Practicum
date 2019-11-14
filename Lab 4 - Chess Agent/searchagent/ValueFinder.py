import chess
import math
import random
import sys

def evaluate(board):

    totalValue = 0

    for i in range(0, 63):
        white = True
        if (board.piece_at(i) != None):
            white = bool(board.piece_at(i).color)
            multiplier = 1
            if not white:
                multiplier = -1
            totalValue += multiplier * getPieceValue(str(board.piece_at(i)))

    return totalValue

    i = 0
    evaluation = 0
    x = True
    try:
        x = bool(board.piece_at(i).color)
    except AttributeError as e:
        x = x
    while i < 63:
        i += 1
        evaluation = evaluation + (getPieceValue(str(board.piece_at(i))) if x else -getPieceValue(str(board.piece_at(i))))
    return evaluation


def getPieceValue(piece):
    if(piece == None):
        return 0
    value = 0
    if piece == "P" or piece == "p":
        value = 10
    if piece == "N" or piece == "n":
        value = 30
    if piece == "B" or piece == "b":
        value = 32
    if piece == "R" or piece == "r":
        value = 50
    if piece == "Q" or piece == "q":
        value = 90
    if piece == 'K' or piece == 'k':
        value = 9000

    return value
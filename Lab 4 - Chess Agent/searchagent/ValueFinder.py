import chess
import math
import random
import sys

pieceValues = {
    'k': 9000,  # King   /  Koning
    'q': 90,    # Queen  /  Koningin
    'r': 50,    # Rook   /  Toren
    'b': 32,    # Bishop /  Loper
    'n': 30,    # Knight /  Paard
    'p': 10,    # Pawn   /  Pion
}

def evaluate(board):

    totalValue = 0

    for i in range(0, 63):
        white = True
        if board.piece_at(i) != None:
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

# Get the value of the piece
def getPieceValue(piece):
    return pieceValues.get(piece.lower(), 0);
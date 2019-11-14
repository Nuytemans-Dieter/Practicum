import chess
import math
import random
import sys

# Based on Hans Berliner's system
# See: https://en.wikipedia.org/wiki/Chess_piece_relative_value
pieceValues = {
    'k': 9000,  # King   /  Koning
    'q': 88,    # Queen  /  Koningin
    'r': 51,    # Rook   /  Toren
    'b': 33,    # Bishop /  Loper
    'n': 32,    # Knight /  Paard
    'p': 10,    # Pawn   /  Pion
}

def evaluate(board):

    totalValue = 0

    for i in range(0, 63):
        isWhite = True
        piece = board.piece_at(i)
        if piece != None:
            isWhite = bool(board.piece_at(i).color)
            if isWhite:
                multiplier = 1
            else:
                multiplier = -1
            totalValue += multiplier * getPieceValue( str(piece) )

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
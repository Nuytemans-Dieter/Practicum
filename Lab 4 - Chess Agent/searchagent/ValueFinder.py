import chess
from time import sleep

maxValue = 999999                   # The max value to be returned from the evaluation function
pieces = ['q', 'r', 'b', 'n', 'p']  # A list of all chess pieces

# Based on Hans Berliner's system
# See: https://en.wikipedia.org/wiki/Chess_piece_relative_value
pieceValues = {
    # WHITE piece values
    #'k': 9000,  # King   /  Koning
    'q': 88,    # Queen  /  Koningin
    'r': 51,    # Rook   /  Toren
    'b': 33,    # Bishop /  Loper
    'n': 32,    # Knight /  Paard
    'p': 10,    # Pawn   /  Pion
    # BLACK piece values
    #'K': 9000,  # King   /  Koning
    'Q': -88,    # Queen  /  Koningin
    'R': -51,    # Rook   /  Toren
    'B': -33,    # Bishop /  Loper
    'N': -32,    # Knight /  Paard
    'P': -10,    # Pawn   /  Pion
}

posValue = [
     1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1,
     2, 2, 2, 4, 4, 2, 2, 2,
     2, 2, 4, 5, 5, 4, 2, 2,
     2, 2, 4, 5, 5, 4, 2, 2,
     2, 2, 2, 4, 4, 2, 2, 2,
     1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1]

# Openings in FEN notation
# Starting position: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
# opening = chess.Board('rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1')


# Useful functions:
# - a position is an int in [0, 64[
# - board.piece_at( position )                          -> Get the piece at a location
# - board.attacks( position )                           -> Get the attacked fields for the piece on the given position
# A piece is received from the second item in this list
# - bool(piece.color)                                   -> Get if the piece color is white
# - board.turn                                          -> Check if it is white's turn
# - board.is_checkmate()                                -> Check if the board is in checkmate
# A piece type is for example Chess.QUEEN, a pieceColor is chess.WHITE or chess.BLACK
# - board.pieces( pieceType,  pieceColor)               -> Get the position of all pieces of these types
# - len(board.pieces( pieceType,  pieceColor))          -> Get the amount of all pieces of these types

def evaluate(board):

    # If checkmate on white: return -maxValue   -> Would be a loss! (and an illegal move at that!)
    # else white wins: return maxValue          -> Will be a win!
    if board.is_checkmate():
        if board.turn:
            return -maxValue
        else:
            return maxValue

    totalValue = 0

    # Count the number of white pieces currently on the board
    numPieces = dict()
    numPieces['q'] = len(board.pieces( chess.QUEEN,  chess.WHITE))
    numPieces['r'] = len(board.pieces( chess.ROOK,   chess.WHITE))
    numPieces['b'] = len(board.pieces( chess.BISHOP, chess.WHITE))
    numPieces['n'] = len(board.pieces( chess.KNIGHT, chess.WHITE))
    numPieces['p'] = len(board.pieces( chess.PAWN,   chess.WHITE))

    # Count the number of black pieces currently on the board
    numPieces['Q'] = len(board.pieces( chess.QUEEN,  chess.BLACK))
    numPieces['R'] = len(board.pieces( chess.ROOK,   chess.BLACK))
    numPieces['B'] = len(board.pieces( chess.BISHOP, chess.BLACK))
    numPieces['N'] = len(board.pieces( chess.KNIGHT, chess.BLACK))
    numPieces['P'] = len(board.pieces( chess.PAWN,   chess.BLACK))

    # Loop all possible pieces: ['q', 'r', 'b', 'n', 'p']
    for piece in pieces:
        num = numPieces.get(piece) - numPieces.get(piece.upper())   # Get # white pieces - # black pieces
        totalValue += num * getPieceValue(piece)                    # Add the value multiplied with the piece value to the total board value

    return totalValue

# Get the value of the piece
def getPieceValue(piece):
    return pieceValues.get(piece, 0)

pawnPosValue = [
     0,  0,  0,  0,  0,  0,  0,  0,
     5, 10, 10,-20,-20, 10, 10,  5,
     5, -5,-10,  0,  0,-10, -5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5,  5, 10, 25, 25, 10,  5,  5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
     0,  0,  0,  0,  0,  0,  0,  0]

knightPosValue = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50]

bishopPosValue = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -20,-10,-10,-10,-10,-10,-10,-20]

rookPosValue = [
      0,  0,  0,  5,  5,  0,  0,  0,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
      5, 10, 10, 10, 10, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0]

queenPosValue = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  5,  5,  5,  5,  5,  0,-10,
      0,  0,  5,  5,  5,  5,  0, -5,
     -5,  0,  5,  5,  5,  5,  0, -5,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20]

kingPosValue = [
     20, 30, 10,  0,  0, 10, 30, 20,
     20, 20,  0,  0,  0,  0, 20, 20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30]
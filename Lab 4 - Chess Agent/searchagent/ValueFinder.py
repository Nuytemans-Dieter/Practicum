import chess
from time import sleep

maxValue = 999999                   # The max value to be returned from the evaluation function
pieces = ['q', 'r', 'b', 'n', 'p']  # A list of all chess pieces

# Based on Hans Berliner's system
# See: https://en.wikipedia.org/wiki/Chess_piece_relative_value
pieceValues = {
    # WHITE piece values
    #'k': 9000,  # King   /  Koning
    'Q': 880,    # Queen  /  Koningin
    'R': 510,    # Rook   /  Toren
    'B': 330,    # Bishop /  Loper
    'N': 320,    # Knight /  Paard
    'P': 100,    # Pawn   /  Pion
    # BLACK piece values
    #'K': 9000,  # King   /  Koning
    'q': -880,    # Queen  /  Koningin
    'r': -510,    # Rook   /  Toren
    'b': -330,    # Bishop /  Loper
    'n': -320,    # Knight /  Paard
    'p': -100,    # Pawn   /  Pion
}

posValue = {
     1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1,
     2, 2, 2, 4, 4, 2, 2, 2,
     2, 2, 4, 5, 5, 4, 2, 2,
     2, 2, 4, 5, 5, 4, 2, 2,
     2, 2, 2, 4, 4, 2, 2, 2,
     1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1}



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

# This function uses our own custom made evaluation function
def evaluate(board):

    # If checkmate on white: return -maxValue   -> Would be a loss! (and an illegal move at that!)
    # else white wins: return maxValue          -> Will be a win!
    if board.is_checkmate():
        if board.turn:
            return -maxValue
        else:
            return maxValue

    if board.is_stalemate():
        return 0

    totalValue = 0

    for position in chess.SQUARES:                  # Loop all board positions
        piece = board.piece_at(position)  # Get the piece at each position

        if piece is not None:             # Make sure a piece is present

            numAttacks = len(board.attacks(position))       # Get the number of attacked squares by this piece

            if piece.color:                                 # If it is white's turn
                totalValue += numAttacks                    # Add the number of white attacked fields
            else:                                           # Else
                totalValue -= numAttacks                    # Subtract the number of black attacked fields

            totalValue += getPosValue(piece, position)  # Get the value of this position

    return totalValue

engine = chess.engine.SimpleEngine.popen_uci("stockfish")
stockfish_time = 0.01

# This function uses Stockfish' evaluation function for a set time and returns the value (PoV: White player)
def stockfishEvaluate(board):
    #Use the Stockfish engine  to find a board value for white
    info = engine.analyse(board, chess.engine.Limit(stockfish_time))
    print(info["score"])
    return info["score"].white().score()

# Get the value of the piece
def getPieceValue(piece):
    return pieceValues.get(piece, 0)

# Get the value of this piece and its position
def getPosValue(piece, position):

    if piece is None:
        return 0

    symbol = piece.symbol()                     # Get the symbol
    positionValue = positionMapping.get(symbol) # Get the array with each positional value for a given piece
    # This variable is located at the bottom of this page

    value = getPieceValue(symbol)                # Get the value of this piece
    value += positionValue[position]             # Get the position value for this piece

    return value

pawnPosValue = [
      0,  0,  0,  0,  0,  0,  0,  0,
     10, 10, 10, 10, 10, 10, 10, 10,
      2,  2,  4,  6,  6,  4,  2,  2,
      1,  1,  2,  5,  5,  2,  1,  1,
      0,  0,  0,  4,  4,  0,  0,  0,
      1, -1, -2,  0,  0, -2, -1,  1,
      1,  2,  2, -4, -4,  2,  2,  1,
      0,  0,  0,  0,  0,  0,  0,  0]

knightPosValue = [
    -10, -8, -6, -6, -6, -6, -8,-10,
     -8, -4,  0,  0,  0,  0, -4, -8,
     -6,  0,  2,  3,  3,  2,  0, -6,
     -6,  1,  3,  4,  4,  3,  1, -6,
     -6,  0,  3,  4,  4,  3,  0, -6,
     -6,  1,  2,  3,  3,  2,  1, -6,
     -8, -4,  0,  1,  1,  0, -4, -8,
    -10, -8, -6, -6, -6, -6, -8, -10]

bishopPosValue = [
     -4, -2, -2, -2, -2, -2, -2, -4,
     -2,  0,  0,  0,  0,  0,  0, -2,
     -2,  0,  1,  2,  2,  1,  0, -2,
     -2,  1,  1,  2,  2,  1,  1, -2,
     -2,  0,  2,  2,  2,  2,  0, -2,
     -2,  2,  2,  2,  2,  2,  2, -2,
     -2,  1,  0,  0,  0,  0,  1, -2,
     -4, -2, -2, -2, -2, -2, -2, -4]

rookPosValue = [
      0,  0,  0,  0,  0,  0,  0,  0,
      1,  2,  2,  2,  2,  2,  2,  1,
     -1,  0,  0,  0,  0,  0,  0, -1,
     -1,  0,  0,  0,  0,  0,  0, -1,
     -1,  0,  0,  0,  0,  0,  0, -1,
     -1,  0,  0,  0,  0,  0,  0, -1,
     -1,  0,  0,  0,  0,  0,  0, -1,
      0,  0,  0,  1,  1,  0,  0,  0]

queenPosValue = [
     -4, -2, -2, -1, -1, -2, -2, -4,
     -2,  0,  0,  0,  0,  0,  0, -2,
     -2,  0,  1,  1,  1,  1,  0, -2,
     -1,  0,  1,  1,  1,  1,  0, -1,
     -0,  0,  1,  1,  1,  1,  0, -1,
     -2,  0,  1,  1,  1,  1,  0, -2,
     -2,  0,  1,  0,  0,  0,  0, -2,
     -4, -2, -2, -1, -1, -2, -2, -4]

kingPosValue = [
     -6, -8, -8, -10, -10, -8, -8, -6,
     -6, -8, -8, -10, -10, -8, -8, -6,
     -6, -8, -8, -10, -10, -8, -8, -6,
     -6, -8, -8, -10, -10, -8, -8, -6,
     -4, -6, -6, -8, -8, -6, -6, -4,
     -2, -4, -4, -4, -4, -4, -4, -2,
      4,  4,  0,  0,  0,  0,  4,  4,
      4,  6,  2,  0,  0,  2,  6,  4]

positionMapping = {'P': pawnPosValue,       'N': knightPosValue,       'B': bishopPosValue,       'R': rookPosValue,       'Q': queenPosValue,       'K': kingPosValue,
                   'p': pawnPosValue[::-1], 'n': knightPosValue[::-1], 'b': bishopPosValue[::-1], 'r': rookPosValue[::-1], 'q': queenPosValue[::-1], 'k': kingPosValue[::-1]}
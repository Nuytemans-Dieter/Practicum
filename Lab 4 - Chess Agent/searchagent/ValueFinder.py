import chess
from time import sleep

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

# Openings in FEN notation
# Starting position: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
opening = chess.Board('rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1')


def evaluate(board):

    totalValue = 0

    for i in range(0, 64):
        piece = board.piece_at(i)
        if piece != None:
            isWhite = bool( piece.color )
            value = getPieceValue( str(piece) )
            #print("---")
            #print(board)
            #print("---")
            #sleep(0.2)  # Time in seconds
            #if opening == board:
            #    return 50000
            if isWhite:
                totalValue += value
                attacks = board.attacks(i)

                #print('---')
                #print("For position: ", i)
                #print("Row: ", (i-i%8)/8, " - Column:", i%8)
                #print(board)
                #print('')
                #print(attacks)
                #print("---")

            else:
                totalValue -= value

    return totalValue

# Get the value of the piece
def getPieceValue(piece):
    return pieceValues.get(piece.lower(), 0)

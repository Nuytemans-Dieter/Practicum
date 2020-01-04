import chess

piece_values = {
    # White pieces
    'K': 100,     # King   /  Koning
    'Q': 88,  # Queen  /  Koningin
    'R': 51,  # Rook   /  Toren
    'B': 33,  # Bishop /  Loper
    'N': 32,  # Knight /  Paard
    'P': 10,   # Pawn   /  Pion
    # Black pieces
    'k': -100,     # King   /  Koning
    'q': -88,  # Queen  /  Koningin
    'r': -51,  # Rook   /  Toren
    'b': -33,  # Bishop /  Loper
    'n': -32,  # Knight /  Paard
    'p': -10,  # Pawn   /  Pion
}

# This function will return a flattened version of the board and substitute all pieces for numerical values (as strings)
def QuantifyBoard(board):

    flatBoard = []
    for position in chess.SQUARES:
        piece = board.piece_at( position )

        if piece is None:
            flatBoard.append(str(0))
        else:
            piece_value = str(piece_values.get(piece.symbol(), 0))
            flatBoard.append( piece_value )

    return flatBoard

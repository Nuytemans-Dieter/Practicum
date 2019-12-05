import chess

piece_values = {
    'K': 1,     # King   /  Koning
    'Q': 0.88,  # Queen  /  Koningin
    'R': 0.51,  # Rook   /  Toren
    'B': 0.33,  # Bishop /  Loper
    'N': 0.32,  # Knight /  Paard
    'P': 0.1,   # Pawn   /  Pion
    # Black pieces
    'k': -1,     # King   /  Koning
    'q': -0.88,  # Queen  /  Koningin
    'r': -0.51,  # Rook   /  Toren
    'b': -0.33,  # Bishop /  Loper
    'n': -0.32,  # Knight /  Paard
    'p': -0.1,   # Pawn   /  Pion
}

# This function will return a flattened version of the board and substitute all pieces for numerical values
def QuantifyBoard(board):

    flatBoard = []
    for position in chess.SQUARES:
        piece = board.piece_at( position )

        if piece is None:
            flatBoard.append(0)
        else:
            piece_value = piece_values.get(piece.symbol(), 0)
            flatBoard.append( piece_value )

    return flatBoard

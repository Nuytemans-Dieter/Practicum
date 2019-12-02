import random
import chess
from searchagent.ValueFinder import evaluate
from searchagent.ValueFinder import getPieceValue

class SearchAgent(object):

    def __init__(self, time_limit=5):
        """Setup the Search Agent"""
        self.time_limit = time_limit
        self.name = "Chess Engine"
        self.author = "S. Vanneste"

    def minimax(self, board: chess.Board, depth, maximizingPlayer):
        if depth == 0 or board.is_game_over():
            return evaluate(board), None

        bestMove = None  # This variable will be used to track the best move so far
        bestVal = None   # This variable will be used to track the board value after the best move so far

        # Find an optimal move
        for moveUCI in board.legal_moves:               # Iterate through all possible moves of all pieces
            move = chess.Move.from_uci( str(moveUCI) )  # Convert the move to the right input
            board.push(move)                            # Execute the move
            boardValue, foundMove = self.minimax(board, depth - 1, not maximizingPlayer)    # Test possible moves for the other player

            if maximizingPlayer:                            # If calculating the best move for the agent

                if bestVal is None or boardValue > bestVal: # If this is the first iteration OR a better move has been found
                    bestVal = boardValue                    # Update the best move

                if boardValue == bestVal:                   # These are equal if the current move is better
                    bestMove = move                         # Set the current best move
            else:

                if bestVal is None or boardValue < bestVal: # If this is the first iteration OR a better move has been found for the opponent
                    bestVal = boardValue                    # Update the enemy's best move

            board.pop()                                     # Undo the move
        return bestVal, bestMove                            # Return the value of the best move and the best move

    def AlphaBeta(self, board: chess.Board, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or board.is_game_over():
            return evaluate(board), None
            # return self.quis(board, alpha, beta), None

        bestMove = None     # This variable will be used to track the best move so far
        bestVal = None      # This variable will be used to track the board value after the best move so far

        # Find an optimal move
        for moveUCI in board.legal_moves:               # Iterate through all possible moves of all pieces
            move = chess.Move.from_uci( str(moveUCI) )  # Convert the move to the right input
            # print("Depth: ", depth)                   # Print information to test algorithm.
            # print("Push move: ", move)
            # print(" ")
            board.push(move)                            # Execute the move

            # Test possible moves for the other player
            boardValue, foundMove = self.AlphaBeta(board, depth - 1, alpha, beta, not maximizingPlayer)
            # print("Move: ", move)
            # print("Value: ", boardValue)
            # print(" ")

            if maximizingPlayer:                            # If calculating the best move for the agent

                if bestVal is None or boardValue > bestVal: # If this is the first iteration OR a better move has been found
                    bestVal = boardValue                    # Update the best move
                    alpha = boardValue

                if boardValue == bestVal:                   # These are equal if the current move is better
                    bestMove = move                         # Set the current best move
            else:

                if bestVal is None or boardValue < bestVal: # If this is the first iteration OR a better move has been found for the opponent
                    bestVal = boardValue                    # Update the enemy's best move
                    beta = boardValue

            board.pop()                                     # Undo the move

            if beta <= alpha:                               # White or black already has a better option available to him.
                break                                       # Don't process unnecessary nodes. Prune positions.

        # print("Depth: ", depth)
        # print("Best value: ", bestVal)
        # print("Best move: ", bestMove)
        return bestVal, bestMove                            # Return the value of the best move and the best move

    def quis(self, board: chess.Board(), alpha, beta):
        eval = evaluate(board)
        if eval >= beta:            # Cutoff: white or black already found a better value.
            return beta
        delta = getPieceValue('q')  # Queen value.
        if eval < alpha - delta:    # Delta pruning.
            return alpha
        if alpha < eval:            # Better move than our last move.
            alpha = eval

        for moveUCI in board.legal_moves:   # For every capture:

            if board.is_capture(moveUCI):   # Keep searching until all captures are made or we get a cutoff.
                move = chess.Move.from_uci( str(moveUCI) )
                board.push(move)
                score = -self.quis(board, -beta, -alpha)
                board.pop()
                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score   # Capture that improves our last best move.

        return alpha

    def random_move(self, board: chess.Board):
        return random.sample(list(board.legal_moves), 1)[0]

    def random_with_first_level_search(self, board: chess.Board):
        moves = list(board.legal_moves)

        best_move = random.sample(moves, 1)[0]
        best_move_value = 0

        for move in moves:
            board.push(move)
            if board.is_checkmate():
                move_value = 100
                if move_value > best_move_value:
                    best_move = move
            board.pop()

            if board.is_into_check(move):
                move_value = 90
                if move_value > best_move_value:
                    best_move = move

            if board.is_capture(move):
                move_value = 80
                if move_value > best_move_value:
                    best_move = move

            if board.is_castling(move):
                move_value = 70
                if move_value > best_move_value:
                    best_move = move

        return best_move

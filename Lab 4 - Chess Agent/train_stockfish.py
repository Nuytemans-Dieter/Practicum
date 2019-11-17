#!/usr/bin/python3
import chess
import chess.engine
from searchagent.search_agent import SearchAgent
from searchagent.ValueFinder import evaluate

def main():
    board = chess.Board()
    white_player = SearchAgent(time_limit=5)
    black_player = chess.engine.SimpleEngine.popen_uci("stockfish")
    limit = chess.engine.Limit(time=5.0)

    running = True
    turn_white_player = True

    while running:
        move = None

        if turn_white_player:
            # value, move = white_player.minimax(board, 3, turn_white_player)
            value, move = white_player.AlphaBeta(board, 3, None, None, turn_white_player)
            print("The current board value is", evaluate(board))
            print("The best move gives value", value)
            turn_white_player = False

        else:
            move = black_player.play(board, limit).move
            turn_white_player = True

        board.push(move)
        print("The value after moving is", evaluate(board))
        print(board)
        print("###########################")

        if board.is_checkmate():
            running = False

            if turn_white_player:
                print("Stockfish wins!")
            else:
                print("{} wins!".format(white_player.name))

        if board.is_stalemate():
            running = False
            print("Stalemate")

    black_player.quit()


if __name__ == "__main__":
    main()

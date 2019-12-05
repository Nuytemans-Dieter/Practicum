#!/usr/bin/python3
import chess
import chess.engine
from searchagent.search_agent import SearchAgent
from searchagent.ValueFinder import evaluate
from searchagent.neural_network_util import QuantifyBoard
import time

def main():
    board = chess.Board()
    engine = chess.engine.SimpleEngine.popen_uci("stockfish")

    white_player = SearchAgent(time_limit=5)
    black_player = engine
    limit = chess.engine.Limit(time=0.1)

    inf = float('inf')
    running = True
    turn_white_player = True

    while running:
        move = None

        if turn_white_player:
            start = time.time()

            # value, move = white_player.minimax(board, 3, turn_white_player)
            value, move = white_player.AlphaBeta(board, 3, -inf, inf, turn_white_player)
            #print("The current board value is", evaluate(board))
            #print("The best move gives value", value)
            turn_white_player = False

            end = time.time()
        else:
            start = time.time()

            move = black_player.play(board, limit).move
            turn_white_player = True

            end = time.time()

        board.push(move)
        #print("The value after moving is", evaluate(board))
        #print("This turn took", round((end - start) * 1000, 2), "milliseconds")
        #print(board)

        print(' '.join( QuantifyBoard(board) ))
        info = engine.analyse(board, chess.engine.Limit(time=0.1))
        print(info["score"].white().score())
        #print("###########################")

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

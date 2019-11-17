#!/usr/bin/python3
import chess

from searchagent.ValueFinder import evaluate
from searchagent.search_agent import SearchAgent


def run_episode():
    board = chess.Board()
    white_player = SearchAgent(time_limit=5)
    white_player.name = "White Player"
    black_player = SearchAgent(time_limit=5)
    black_player.name = "Black Player"

    running = True
    turn_white_player = True
    counter = 0

    while running:
        counter += 1
        move = None

        if turn_white_player:
            # value, move = white_player.minimax(board, 3, turn_white_player)
            value, move = white_player.AlphaBeta(board, 3, None, None, turn_white_player)
            print("The current board value is", evaluate(board))
            # print("The best move gives value", value)
            # print("white")
        else:
            # value, move = black_player.minimax(board, 3, turn_white_player)
            value, move = white_player.AlphaBeta(board, 3, None, None, turn_white_player)
            print("The current board value is", evaluate(board))
            # print("The best move gives value", value)
            # print("Black")

        board.push(move)
        print(board)
        print("###########################")
        print(board.piece_at(chess.QUEEN))
        print("###########################")

        if board.is_checkmate():
            running = False

            if turn_white_player:
                print("{} wins!".format(black_player.name))
            else:
                print("{} wins!".format(white_player.name))

        if board.is_stalemate() or counter > 1000:
            running = False
            print("Stalemate")


def main():
    run_episode()


if __name__ == "__main__":
    main()

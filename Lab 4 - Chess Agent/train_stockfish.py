#!/usr/bin/python3
import chess
import chess.engine
from searchagent.search_agent import SearchAgent
from searchagent.ValueFinder import evaluate
from searchagent.neural_network_util import QuantifyBoard
import time

def main():

    numGames = 10

    for gameNumber in range(numGames):

        board = chess.Board()
        engine = chess.engine.SimpleEngine.popen_uci("stockfish")

        boardData = []
        valueData = []

        white_player = SearchAgent(time_limit=5)
        black_player = engine
        limit = chess.engine.Limit(time=0.1)

        inf = float('inf')
        running = True
        turn_white_player = True

        print("Starting game:", gameNumber)

        while running:

            if turn_white_player:
                #start = time.time()
                #value, move = white_player.AlphaBeta(board, 3, -inf, inf, turn_white_player)
                move = white_player.random_with_first_level_search(board)
                turn_white_player = False
                #end = time.time()
            else:
                #start = time.time()
                move = black_player.play(board, limit).move
                turn_white_player = True
                #end = time.time()

            board.push(move)
            #print("This turn took", round((end - start) * 1000, 2), "milliseconds")
            print(board)

            # Keep track of the data
            info = engine.analyse(board, chess.engine.Limit(time=0.1))
            boardData.append(QuantifyBoard(board))
            valueData.append(info["score"].white().score())

            print("###########################")

            if board.is_checkmate():
                running = False

                if turn_white_player:
                    print("Stockfish wins!")
                else:
                    print("{} wins!".format(white_player.name))

                saveData(boardData, valueData)


            if board.is_stalemate():
                running = False
                print("Stalemate")

        black_player.quit()


# Append training data to boardData.txt and valueData.txt
def saveData(boardData, valueData):
    print("Saving board data...")

    boards = open("boardData.txt", "a")
    for b in boardData:
        boards.write(str(b) + "\n")
    boards.close()

    print("Saving value data...")

    values = open("valueData.txt", "a")
    for val in valueData:
        values.write(str(val) + "\n")
    values.close()

if __name__ == "__main__":
    main()

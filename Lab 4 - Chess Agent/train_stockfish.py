#!/usr/bin/python3
# Import libraries
import chess
import chess.engine
import tensorflow as ts
import time

# Local imports
from searchagent.search_agent import SearchAgent
from searchagent.ValueFinder import evaluate
from searchagent.neural_network_util import QuantifyBoard
from searchagent.neural_network import prepare_network

def main():

    # Train the neural network
    prepare_network()

    numGames = 1                    # Choose the amount of games to be played
    do_append_data = False          # Choose whether or not to gather and save data

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
                value, move = white_player.AlphaBeta(board, 3, -inf, inf, turn_white_player)
                #move = white_player.random_with_first_level_search(board)
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
            info = engine.analyse(board, chess.engine.Limit(time=0.3))      # Analyse for a specified time period
            boardData.append(QuantifyBoard(board))                          # Add a quantified version of the board to the data
            valueStr = info["score"].white()                                # Get the score for white's perspective

            print("SF:", valueStr)
            print("ML:", evaluate(board))

            value = valueStr.score()                                        # Convert to a score
            if value is None:                                               # If someone is winning in x moves
                if '-' in str(valueStr):                                    # If black is winning
                    value = -5000                                           # Set the value to the minimum value
                else:
                    value = 5000                                            # If white is winning: set the value to the maximum value
                offset = str(valueStr).strip('#')                           # Remove the hash symbol from the value
                offset = int(offset)                                        # Convert the number to an offset
                value = value - offset                                      # Offset the max value (so that the last move will be the highest value)

            valueData.append(value)

            print("###########################")

            if board.is_checkmate():
                running = False

                if turn_white_player:
                    print("Stockfish wins!")
                else:
                    print("{} wins!".format(white_player.name))

                if do_append_data:
                    saveData(boardData, valueData)

            if board.is_stalemate():
                running = False
                print("Stalemate")



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

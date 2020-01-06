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
from searchagent.convolutional_neural_network import prepare_network as prepare_CNN

def main():

    # Train the neural network
    prepare_network()
    prepare_CNN()

    # Choose the amount of games to be played
    numGames = 4
    wins = 0
    gelijk = 0
    aantalmoves=0
    # Choose whether or not to gather and save data
    do_append_data = True

    for gameNumber in range(numGames):

        board = chess.Board()
        engine = chess.engine.SimpleEngine.popen_uci("stockfish")

        boardData = []
        valueData = []

        white_player = SearchAgent(time_limit=5)
        black_player = engine

        inf = float('inf')
        running = True
        turn_white_player = True

        gameProgress = str(gameNumber+1) + '/' + str(numGames)
        print("Starting game:", gameProgress)

        value = 0               # The previous evaluation
        numSameValue = 0        # The amount of times the evaluation was equal in a row

        while running:

            previousValue = value       # Get the previous value

            # start = time.time()
            if turn_white_player:
                value, move = white_player.AlphaBeta(board, 2, -inf, inf, turn_white_player)
                #move = black_player.play(board, chess.engine.Limit(time=0.1)).move
                turn_white_player = False
            else:
                move = black_player.play(board, chess.engine.Limit(time=0.1,depth=1)).move
                #move = white_player.random_with_first_level_search(board)
                turn_white_player = True
            #end = time.time()

            board.push(move)
            aantalmoves+=1
            #print("This turn took", round((end - start) * 1000, 2), "milliseconds")
            #print(board)

            # Keep track of the data
            info = engine.analyse(board, chess.engine.Limit(time=0.5))      # Analyse for a specified time period
            valueStr = info["score"].white()                                # Get the score for white's perspective

            print("Stockfish:", valueStr)
            print("Our prediction:", evaluate(board))

            value = valueStr.score()                                        # Convert to a score
            if value is None:                                               # If someone is winning in x moves
                if '-' in str(valueStr):                                    # If black is winning
                    value = -5000                                           # Set the value to the minimum value
                else:
                    value = 5000                                            # If white is winning: set the value to the maximum value
                offset = str(valueStr).strip('#')                           # Remove the hash symbol from the value
                offset = int(offset)                                        # Convert the number to an offset
                value = value - offset                                      # Offset the max value (so that the last move will be the highest value)

            if previousValue == value:                                      # Keep track of the amount of equal evaluations in a row
                numSameValue += 1
            else:
                numSameValue = 0

            if numSameValue <= 5:                                               # Only append data if not too many equal evaluations have been made
                boardData.append(QuantifyBoard(board))                          # Add a quantified version of the board to the data
                valueData.append(value)                                         # Add the approximated value data
            elif numSameValue == 25:                                            # Prevent infinite stuck loops
                running = False                                                 # Quit running
                print("This game has been stopped due to being stuck for too long")
            else:
                print("This state was discarded due to too many equal evaluations")

            print("###########################")

            if board.is_checkmate():
                running = False

                if turn_white_player:
                    print("Stockfish (black player) wins!")
                else:
                    print("{} (white player) wins!".format(white_player.name))
                    wins+=1


            # If stalemate OR only the kings are left
            if board.is_stalemate() or getNumPieces( board ) == 2:
                running = False
                print("Stalemate")
                gelijk+=1

            if not running:
                if do_append_data:
                    saveData(boardData, valueData)
                else:
                    print("Data is not being saved! (do_append_data == False)")
    print("aantal games: " + str(numGames))
    print("Wins: "+ str(wins))
    print("Losses: " + str(numGames-wins-gelijk))
    print("gelijk: " + str(gelijk))
    print("aantalmoves: " + str(aantalmoves/numGames))



# Append training data to boardDataOld.txt and valueDataOld.txt
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

    print("All data is now saved!")


def getNumPieces( board ):
    # Count the number of white pieces
    numPieces  = 2      # There are ALWAYS 2 kings (white + black)
    numPieces += len(board.pieces( chess.QUEEN,  chess.WHITE))
    numPieces += len(board.pieces( chess.ROOK,   chess.WHITE))
    numPieces += len(board.pieces( chess.BISHOP, chess.WHITE))
    numPieces += len(board.pieces( chess.KNIGHT, chess.WHITE))
    numPieces += len(board.pieces( chess.PAWN,   chess.WHITE))
    # Count the number of black pieces
    numPieces += len(board.pieces( chess.QUEEN,  chess.BLACK))
    numPieces += len(board.pieces( chess.ROOK,   chess.BLACK))
    numPieces += len(board.pieces( chess.BISHOP, chess.BLACK))
    numPieces += len(board.pieces( chess.KNIGHT, chess.BLACK))
    numPieces += len(board.pieces( chess.PAWN,   chess.BLACK))
    return numPieces

if __name__ == "__main__":
    main()

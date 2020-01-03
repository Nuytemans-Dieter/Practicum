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

    # Choose the amount of games to be played
    numGames = 1
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

        while running:

            if turn_white_player:
                #start = time.time()
                value, move = white_player.AlphaBeta(board, 2, -inf, inf, turn_white_player)
                #move = black_player.play(board, chess.engine.Limit(time=0.1)).move
                turn_white_player = False
                #end = time.time()
            else:
                #start = time.time()
                move = black_player.play(board, chess.engine.Limit(time=0.1)).move
                turn_white_player = True
                #end = time.time()

            board.push(move)
            #print("This turn took", round((end - start) * 1000, 2), "milliseconds")
            print(board)

            # Keep track of the data
            info = engine.analyse(board, chess.engine.Limit(time=0.5))      # Analyse for a specified time period
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

            # If stalemate OR only the kings are left
            if board.is_stalemate() or getNumPieces( board ) == 2:
                running = False
                print("Stalemate")



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

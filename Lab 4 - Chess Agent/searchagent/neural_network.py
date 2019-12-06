from tensorflow import keras
# noinspection PyUnresolvedReferences
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split

# Helper libraries
import ast
import numpy as np

# Local imports
from searchagent.neural_network_util import QuantifyBoard

model = keras.Sequential()

def prepare_network():
    print("Loading data...")

    # Open the data
    boardText = open("data/boardData.txt", "r")  # Open file contents (boards)
    valueText = open("data/valueData.txt", "r")  # Open file contents (values)

    # Create neural network input variables
    boards = []
    values = []

                                        # Read and interpret the data
                                        # Get data of the board
    for line in boardText:
      stripped = line.strip('\n')       # Strip the newline character
      arr =  ast.literal_eval(stripped) # Interpret the string as an array, not as a string
      arr = np.array(arr)               # Convert to numpy for the next step
      arr = arr.astype(np.float)        # Convert all contents to float instead of string
      boards.append(arr)                # Append data to the list

                                        # Get data of the board values
    for line in valueText:
      stripped = line.strip('\n')       # Strip the newline character
      if stripped == 'None':            # Filter None values
        values.append(float(0))         # Append 0 instead of 'None'
      else:
        values.append(float(stripped))  # Convert to int and add the data to the list

    print("Normalizing data...")
    normValues = []
    high = max(values, key=abs)         # Get the highest (absolute) number from all values
    for val in values:
      percentage = val / high           # Normalize each element
      normValues.append( percentage )   # Add each normalized value to the new list

    values = normValues                 # Overwrite all values by the normalized list

    #print("Boards:", boards)            # Print the loaded boards
    #print("Values:", values)            # Print the loaded values

    print("Selecting training and testing data...")

    train_boards, test_boards, train_values, test_values = train_test_split(boards, values, test_size=0.10, shuffle= True)
    train_boards = np.array(train_boards)
    test_boards = np.array(test_boards)
    train_values = np.array(train_values)
    test_values = np.array(test_values)

    print("Creating neural network...")


    model = keras.Sequential([
        #layers.Input(shape=(None,64)),
        keras.layers.Dense(256, activation='tanh'),
        #layers.Conv1D(128, kernel_size=8 ,activation='tanh'),
        keras.Dense(256, activation='tanh'),
        keras.Dense(256, activation='tanh'),
        keras.Dense(1, activation='softmax')
    ])

    print("Compiling the model...")

    # For documentation, see https://keras.io/models/model/
    model.compile(optimizer='adam',
                  loss='mean_squared_error',
                  metrics=['accuracy'])

    print("Training and testing the model...")

    model.fit(train_boards, train_values, epochs=3)

    test_loss, test_acc = model.evaluate(test_boards,  test_values, verbose=2)
    print('\nTest loss (MSE)', test_loss)

# Predict a value for a given board
def predict(board):
    quantified = QuantifyBoard(board)
    return model.predict(np.array(quantified))
from tensorflow import keras
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split

# Helper libraries
import ast
import numpy as np

# Local imports
from searchagent.neural_network_util import QuantifyBoard

model = keras.Sequential()
highest_value = 0

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

    #print("Values:", values)            # Print the loaded values

    # Reshape a 2D tuple to matrix
    boards = np.asarray(boards)
    matBoards = np.reshape(boards, (boards.shape[0], 8, 8, 1))

    print("Selecting training and testing data...")

    train_boards, test_boards, train_values, test_values = train_test_split(matBoards, values, test_size=0.10, shuffle= True)
    train_boards = np.array(train_boards)
    test_boards = np.array(test_boards)
    train_values = np.array(train_values)
    test_values = np.array(test_values)

    print("Creating neural network...")

    model.add(layers.Conv2D(64, kernel_size=3, activation='selu', input_shape=(8, 8, 1)))
    model.add(layers.Conv2D(64, kernel_size=3, activation='selu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(layers.Conv2D(64, kernel_size=2, activation='selu'))
    model.add(layers.Flatten())
    model.add(layers.Dense(1, activation='linear'))



    print("Compiling the model...")

    optimizer = keras.optimizers.RMSprop(0.001)

    # For documentation, see https://keras.io/models/model/
    model.compile(optimizer=optimizer,
                  loss='mean_squared_error',
                  metrics=['mean_squared_error'])

    model.summary()

    print("Training and testing the model...")

    model.fit(matBoards, np.array(values), epochs=10)

    test_loss = model.evaluate(test_boards,  test_values, verbose=2)
    print('\nTest loss (MSE)', test_loss)


# Predict a value for a given board
def predict(board):
    quantified = QuantifyBoard(board)
    #return highest_value * model.predict(np.expand_dims(quantified, axis=0), batch_size=1)[0]
    npQuantified = np.array(quantified)
    sampleMatrix = [[51, 0, 33, 0, 100, 33, 0, 51],
                    [10, 10, 10, 0, 0, 10, 10, 10, ],
                    [0, 0, 32, 0, 0, 32, 0, 0, ],
                    [0, 0, 0, 88, 10, 0, 0, 0, ],
                    [0, 0, 0, 0, 0, 0, 0, 0, ],
                    [0, 0, 0, -10, 0, -32, 0, 0, ],
                    [-10, -10, -10, 0, 0, -10, -10, -10, ],
                    [-51, -32, -33, -88, -100, -33, 0, -51, ]]
    # return highest_value * model.predict(np.expand_dims(quantified, axis=0), batch_size=1)[0]
    npQuantified = np.array(sampleMatrix)
    npQuantified = npQuantified.astype(float)
    npQuantified = np.reshape(npQuantified, (1, 8, 8, 1))
    prediction = model.predict(npQuantified, batch_size=1)
    return prediction[0][0]

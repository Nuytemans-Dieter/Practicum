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

    #print("Normalizing data...")
    #normValues = []
    #highest_value = max(values, key=abs)# Get the highest (absolute) number from all values
    #for val in values:
    #  percentage = val / highest_value  # Normalize each element
    #  normValues.append( percentage )   # Add each normalized value to the new list

    #values = normValues                 # Overwrite all values by the normalized list

    #print("Boards:", boards)            # Print the loaded boards
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

    model = keras.Sequential([
        layers.Conv2D(64, kernel_size=3, activation='selu', input_shape=(8, 8, 1)),
        layers.Conv2D(64, kernel_size=3, activation='selu'),    # Kernel operation
        layers.MaxPooling2D(pool_size=(2, 2)),                  # Convert to (4,4)
        layers.Conv2D(64, kernel_size=2, activation='selu'),    # Kernel operation
        layers.Flatten(),
        layers.Dense(1, activation='linear')
    ])


    print("Compiling the model...")

    optimizer = keras.optimizers.RMSprop(0.001)

    # For documentation, see https://keras.io/models/model/
    model.compile(optimizer=optimizer,
                  loss='mean_squared_error',
                  metrics=['mean_absolute_error', 'mean_squared_error'])

    model.summary()

    print("Training and testing the model...")

    model.fit(matBoards, np.array(values), epochs=1)

    test_loss = model.evaluate(test_boards,  test_values, verbose=2)
    print('\nTest loss (MSE)', test_loss)


# Predict a value for a given board
def predict(board):
    quantified = QuantifyBoard(board)
    #return highest_value * model.predict(np.expand_dims(quantified, axis=0), batch_size=1)[0]
    quantified = np.array(quantified)
    quantified = quantified.astype(float)
    npQuantified = np.reshape(quantified, (8, 8))
    prediction = model.predict(npQuantified)
    #print(prediction)
    return prediction
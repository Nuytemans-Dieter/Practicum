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

    print("Selecting training and testing data...")

    train_boards, test_boards, train_values, test_values = train_test_split(boards, values, test_size=0.10, shuffle= True)
    train_boards = np.array(train_boards)
    test_boards = np.array(test_boards)
    train_values = np.array(train_values)
    test_values = np.array(test_values)

    train_boards = np.expand_dims(train_boards, axis=0)
    test_boards = np.expand_dims(test_boards, axis=0)
    train_values = np.expand_dims(train_values, axis=0)
    test_values = np.expand_dims(test_values, axis=0)

    print(train_boards)
    print(train_values)

    print("Creating neural network...")
    model = keras.Sequential([
        layers.Dense(256, input_shape=(None, 8, 8), activation='relu'),
        layers.Dense(256, activation='relu'),
        layers.Dense(256, activation='relu'),
        layers.Dense(1, activation='linear'),
    ])

    print("Compiling the model...")

    optimizer = keras.optimizers.RMSprop(0.001)

    # For documentation, see https://keras.io/models/model/
    model.compile(optimizer=optimizer,
                  loss='mean_absolute_error',
                  metrics=['mean_absolute_error'])

    print("Training and testing the model...")

    model.fit(train_boards, train_values, epochs=10)

    model.summary()

    test_loss = model.evaluate(test_boards,  test_values, verbose=2)
    print('\nTest loss (MSE)', test_loss)


# Predict a value for a given board
def predict(board):
    quantified = QuantifyBoard(board)
    #return highest_value * model.predict(np.expand_dims(quantified, axis=0), batch_size=1)[0]
    npQuantified = np.array(quantified)
    prediction = model.predict(npQuantified, batch_size=1)
    print(prediction)
    return prediction

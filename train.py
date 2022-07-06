import os
import argparse
import logging
import json

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Conv1D, MaxPool1D, Flatten, Dense
from tensorflow.keras.optimizers import Adam

from libs.argparser import checkarch, checkloglevel
from libs.logger import initlogger
from libs.nnmodule import NN, NormTrain, Rot90

def initargparser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "arch",
        metavar="ARCH",
        type=checkarch,
        help=(
            "Provide NN architecture type. "
            "Available options CNN | DNN | RNN. "
        ),
    )
    parser.add_argument(
        "dataset",
        metavar="DATASET_PATH",
        help=(
            "Provide dataset path. "
            "DATASET_PATH must contain properties.txt. "
        ),
    )
    parser.add_argument(
        "-log",
        "--log",
        type=checkloglevel,
        default="info",
        help=(
            "Provide logging level. "
            "Example --log debug, default='warning'"
        )
    )
    options = parser.parse_args()
    return options

#CNN model
def createcnn(input_shape, n_output):
    """
    Create CNN model
    """
    cnn_model = Sequential([
        Input(shape=input_shape),                                   # 128 x 87      | 128 x 44      |   O = output, I = input, H = kernel
        NormTrain(),                                                #                               |   Normalize data from 0-255 to 0-1 during training
        Rot90(k=3),                                                 # 87 x 128      | 44 x 128      |   Rotate -90deg times (Matching the data structure with time)
        Conv1D(filters=64, kernel_size=7, activation='relu'),       # 81 x 64       | 38 x 64       |   (O_height = I_height - H_height + 1), n_filter
        MaxPool1D(pool_size=3),                                     # 27 x 64       | 12 x 64       |   (O_height = I_height / H_strides), I_depth
        Conv1D(filters=32, kernel_size=3, activation='relu'),       # 25 x 32       | 10 x 32       |   (O_height = I_height - H_height + 1), n_filter
        MaxPool1D(pool_size=3),                                     #  8 x 32       |  3 x 32       |   (O_height = I_height / H_strides), I_depth
        Flatten(),
        Dense(units=128, activation='elu'),
        Dense(units=n_output, activation='softmax')
    ])

    return cnn_model

#DNN model
def creatednn(input_shape, n_output):
    """
    Create DNN model
    """
    dnn_model = Sequential([
        Input(shape=input_shape),                                   # 128 x 87      | 128 x 44      |   O = output, I = input, H = kernel
        Rot90(k=3),                                                 # 87 x 128      | 44 x 128      |   Rotate -90deg times (Matching the data structure with time)
        Flatten(),
        Dense(units=3400, activation='elu'),
        Dense(units=1020, activation='elu'),
        Dense(units=306, activation='elu'),
        Dense(units=n_output, activation='softmax')
    ])

    return dnn_model

#RNN model
def creaternn(input_shape, n_output):
    """
    Create RNN model
    """
    rnn_model = Sequential([
        Input(shape=input_shape),                                   # 128 x 87      | 128 x 44      |   O = output, I = input, H = kernel
        Rot90(k=3),                                                 # 87 x 128      | 44 x 128      |   Rotate -90deg times (Matching the data structure with time)
        LSTM(input_shape[0], return_sequences=True),                #Using activation=tanh, recurrent_activation=sigmoid, recurrent_dropout=0, unroll=False, use_bias=True to use CUDNN
        LSTM(input_shape[0]),
        Dense(units=n_output, activation='softmax')
    ])

    return rnn_model

logger = logging.getLogger(__name__)

def main():
    """
    Audio-based detection and crime detection system
    Training system
    """
    options = initargparser()
    initlogger(options.log)

    #Params
    BATCH_SIZE = 128
    LEARNING_RATE = 0.0001
    EPOCHS = 100
    OUTPUT_PATH = "Models"
    
    #Load dataset config
    dataset_conf = {}
    with open(options.dataset + '/properties.txt') as f:
        dataset_conf = json.load(f)
    if dataset_conf == {}:
        raise FileNotFoundError("Failed to read %s", (options.dataset + '/properties.txt'))
    
    #Load dataset
    (x_train, y_train), (x_val, y_val), (x_test, y_test), classes = NN.loaddataset(options.dataset)

    #Get input size
    input_shape = x_train[0].shape[0:2]
    logger.info(input_shape)

    #Create model
    if options.arch == "cnn":
        model = createcnn(input_shape, len(classes))
    elif options.arch == "dnn":
        model = creatednn(input_shape, len(classes))
    elif options.arch == "rnn":
        model = creaternn(input_shape, len(classes))
    model.summary()
    logger.info("Model created")

    #Train
    logger.info("Training started")
    model.compile(optimizer=Adam(learning_rate=LEARNING_RATE), loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train, batch_size=BATCH_SIZE, validation_data=(x_val, y_val), epochs=EPOCHS, verbose=2)
    logger.info("Training completed")

    #Evaluate
    score = model.evaluate(x=x_test, y=y_test, batch_size=BATCH_SIZE, verbose=0)
    logger.info('Test loss: %r', score[0]) 
    logger.info('Test accuracy: %r', score[1])

    #Save model
    model_path = OUTPUT_PATH + "/" + options.arch.upper() + "_" + str(dataset_conf["spectrogram"]["chunk duration"]) + "_" + str(dataset_conf["spectrogram"]["cutoff"])
    if not os.path.exists(model_path):
        os.makedirs(model_path)
    model.save(model_path + "/model.h5")
    logger.info("Model saved to %s", (model_path + "/model.h5"))

    #Write config file
    with open(OUTPUT_PATH + "/config.file", 'w') as f:
        config = {
            "dataset" : options.dataset,
            "classes" : classes,
            "batch size" : BATCH_SIZE,
            "learning rate" : LEARNING_RATE,
            "epoch" : EPOCHS,
            "sampling rate": dataset_conf["spectrogram"]["sampling rate"],
            "chunk duration" : dataset_conf["spectrogram"]["chunk duration"],
            "overlap ratio": dataset_conf["spectrogram"]["overlap ratio"],
            "cutoff": dataset_conf["spectrogram"]["cutoff"],
            "order": dataset_conf["spectrogram"]["order"],
            "nfft": dataset_conf["spectrogram"]["nfft"],
            "hop length": dataset_conf["spectrogram"]["hop length"],
            "nmel": dataset_conf["spectrogram"]["nmel"],
        }
        f.write(json.dumps(config))
    logger.info("Train property saved to %s", OUTPUT_PATH + "/config.file")
    
    #Write architecture
    with open(OUTPUT_PATH + "/architecture.txt", 'w') as f:
        model.summary(print_fn=lambda x: f.write(x))
    logger.info("Architecture detail saved to %s", OUTPUT_PATH + "/architecture.txt")

if __name__ == '__main__':
    main()
import os
import logging
import json

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Conv1D, MaxPool1D, Flatten, Dense, LSTM, Dropout
from tensorflow.keras.optimizers import Adam, Adagrad, RMSprop, Nadam, SGD, Adamax, Ftrl, Adadelta

from libs.configmodule import saveconfig
from libs.argparser import parser, Range
from libs.logger import initlogger
from libs.nnmodule import NN, Rot90

logger = logging.getLogger(__name__)

def main():
    """
    Audio-based detection and crime detection system
    Training system
    """
    options = initargparser()
    initlogger(options.log)

    #Params
    OUTPUT_PATH = "Models"
    
    #Load dataset config
    dataset_conf = {}
    with open(options.dataset + '/properties.txt') as f:
        dataset_conf = json.load(f)
    if dataset_conf == {}:
        raise FileNotFoundError("Failed to read %s", (options.dataset + '/properties.txt'))

    #Compile train config
    config = {
        "arch" : options.arch,
        "dataset" : options.dataset.replace("\\","/"),
        "classes" : dataset_conf["enhance"]["classes"],
        "batch size" : options.batch,
        "learning rate" : options.learning_rate,
        "train-val ratio": dataset_conf["split"]["train ratio"],
        "epochs" : options.epochs,
        "cutoff": dataset_conf["spectrogram"]["cutoff"],
        "order": dataset_conf["spectrogram"]["order"],
        "nfft": dataset_conf["spectrogram"]["nfft"],
        "hop length": dataset_conf["spectrogram"]["hop length"],
        "nmel": dataset_conf["spectrogram"]["nmel"],
        "rbir" : options.rbir
    }

    try:
        config["sampling rate"] = dataset_conf["segmentation"]["sampling rate"]
        config["segment duration"] = dataset_conf["segmentation"]["chunk duration"]
        config["overlap ratio"] = dataset_conf["segmentation"]["overlap ratio"]
    except KeyError:
        config["sampling rate"] = dataset_conf["spectrogram"]["sampling rate"]
        config["segment duration"] = dataset_conf["spectrogram"]["chunk duration"]
        config["overlap ratio"] = dataset_conf["spectrogram"]["overlap ratio"]

    #Print training params
    logger.info("")
    
    #Load dataset
    (x_train, y_train), (x_val, y_val), (x_test, y_test), classes = NN.loaddataset(config["dataset"], intensity_th=config["rbir"])

    #Get input size
    input_shape = x_train[0].shape[0:2]
    logger.info(input_shape)

    #Create model
    if config["arch"] == "cnn":
        model = createcnn(input_shape, len(classes))
    elif config["arch"] == "dnn":
        model = creatednn(input_shape, len(classes))
    elif config["arch"] == "rnn":
        model = creaternn(input_shape, len(classes))
    model.summary()
    logger.info("Model created")

    #Select optimizer
    if options.optimizer == "adadelta":
        used_optimizer = Adadelta
    elif options.optimizer == "adagrad":
        used_optimizer = Adagrad
    elif options.optimizer == "adam":
        used_optimizer = Adam
    elif options.optimizer == "adamax":
        used_optimizer = Adamax
    elif options.optimizer == "ftrl":
        used_optimizer = Ftrl
    elif options.optimizer == "nadam":
        used_optimizer = Nadam
    elif options.optimizer == "rmsprop":
        used_optimizer = RMSprop
    elif options.optimizer == "sgd":
        used_optimizer = SGD

    #Train
    logger.info("Training started")
    model.compile(optimizer=used_optimizer(learning_rate=config["learning rate"]), loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train, batch_size=config["batch size"], validation_data=(x_val, y_val), epochs=config["epochs"], verbose=2)
    logger.info("Training completed")

    #Evaluate
    score = model.evaluate(x=x_test, y=y_test, batch_size=config["batch size"], verbose=0)
    logger.info('Test loss: %r', score[0]) 
    logger.info('Test accuracy: %r', score[1])

    #Save model
    model_path = OUTPUT_PATH + "/" + config["arch"].upper() + "_" + str(config["train-val ratio"]) + "_" + str(config["segment duration"]) + "_" + str(config["cutoff"])
    if not os.path.exists(model_path):
        os.makedirs(model_path)
    output_path = model_path + "/" + options.optimizer.capitalize()
    if config["rbir"] is not None:
        output_path += ("_%g" % config["rbir"])
    output_path += ("_%.1f" % (score[1]*100))
    model.save(output_path + '.h5')
    logger.info("Model saved to %s", output_path + ".h5")

    #Write config file
    saveconfig(output_path, config)
    
    #Write architecture
    with open(output_path + ".arch", 'w') as f:
        model.summary(print_fn=lambda x: f.write(x))
    logger.info("Architecture detail saved to %s", output_path + ".arch")

#CNN model
def createcnn(input_shape, n_output):
    """
    Create CNN model
    """
    cnn_model = Sequential([
        Input(shape=input_shape),                                   # 128 x 87      | 128 x 44      |   O = output, I = input, H = kernel
        Rot90(k=3),                                                 # 87 x 128      | 44 x 128      |   Rotate 90deg 3 times (270deg) (Matching the data structure with time)
        Conv1D(filters=64, kernel_size=7, activation='relu'),       # 81 x 64       | 38 x 64       |   (O_height = I_height - H_height + 1), n_filter
        MaxPool1D(pool_size=3),                                     # 27 x 64       | 12 x 64       |   (O_height = I_height / H_strides), I_depth
        Flatten(),
        Dense(units=512, activation='relu'),
        Dropout(.15),
        Dense(units=128, activation='relu'),
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
        Rot90(k=3),                                                 # 87 x 128      | 44 x 128      |   Rotate 90deg 3 times (270deg) (Matching the data structure with time)
        Flatten(),
        Dense(units=900, activation='relu'),
        Dropout(.15),
        Dense(units=300, activation='relu'),
        Dense(units=100, activation='relu'),
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
        Rot90(k=3),                                                 # 87 x 128      | 44 x 128      |   Rotate 90deg 3 times (270deg) (Matching the data structure with time)
        LSTM(128, return_sequences=True),                           #Using activation=tanh, recurrent_activation=sigmoid, recurrent_dropout=0, unroll=False, use_bias=True to use CUDNN
        LSTM(128),
        Dense(units=42, activation='relu'),
        Dropout(.15),
        Dense(units=n_output, activation='softmax')
    ])

    return rnn_model

def initargparser():
    parser.add_argument(
        "arch",
        metavar="ARCH",
        type=str.lower,
        choices=["cnn", "dnn", "rnn"],
        help=(
            "Provide NN architecture type. "
            "Available options CNN | DNN | RNN. "
        ),
    )
    parser.add_argument(
        "optimizer",
        metavar="OPTIMIZER",
        type=str.lower,
        choices=["adadelta", "adagrad", "adam", "adamax", "ftrl", "nadam", "rmsprop", "sgd"],
        help=(
            "Provide model OPTIMIZER type. "
            "Available options Adadelta | Adagrad | Adam | Adamax | Ftrl | Nadam | RMSProp | SGD. "
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
        "-rbir",
        "--rbir",
        metavar="RBIR",
        type=float,
        choices=[Range(0.0, 1.0)],
        default=None,
        help=(
            "Provide ratio-based intensity reduction value. "
        ),
    )
    parser.add_argument(
        "-batch",
        "--batch",
        metavar="BATCH",
        type=int,
        default=128,
        help=(
            "Provide BATCH value. "
        ),
    )
    parser.add_argument(
        "-lr",
        "--learning_rate",
        metavar="LR",
        type=float,
        choices=[Range(0.0, 1.0)],
        help=(
            "Provide learning rate value. "
        ),
    )
    parser.add_argument(
        "-epochs",
        "--epochs",
        metavar="EPOCHS",
        type=int,
        default=100,
        help=(
            "Provide EPOCHS value. "
        ),
    )
    options = parser.parse_args()
    return options

if __name__ == '__main__':
    main()
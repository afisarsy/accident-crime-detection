import os
import logging
import random

import numpy as np
from tensorflow.keras.layers import Layer
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical
from tensorflow.math import divide
from tensorflow.experimental.numpy import rot90
from PIL import Image

logger = logging.getLogger(__name__)

class NN:
    """
    Neural Network Object
    """
    #NN Model
    __model = None

    #Config
    __arch = None
    __model_path = None
    __labels = []
    __outputs = []

    #Input buffer
    __input = []

    def __init__(self, conf):
        """
        Create Neural Network Object
        """
        #Load config
        self.__arch = conf["arch"]
        self.__model_path = conf["model path"]
        self.__labels = conf["labels"]
        self.__outputs = conf["outputs"]
        
        #NN initialization
        self.__model = load_model(self.__model_path)
        self.__model.summary()
    
    def reshapedata(self):
        """
        Reshape batch data
        """

    def predict(self, x):
        """
        Predict x using loaded model
        """
        #Predict input x, verbose 0=silent, 1=progress bar, 2=single line
        y = self.__model.predict(x=x, verbose=0)
        return y
    
    def thresholding(self, y):
        """
        Threshold and mapping the prediction result
        """
    
    @staticmethod
    def loaddataset(dataset_path):
        """
        Load dataset from specified path
        """
        logger.info("Loading train data")
        (x_train, y_train), classes = NN.__loaddata(dataset_path, "train")
        logger.info("Loading validation data")
        (x_val, y_val), classes = NN.__loaddata(dataset_path, "val")
        logger.info("Loading test data")
        (x_test, y_test), classes = NN.__loaddata(dataset_path, "test")

        return (x_train, y_train), (x_val, y_val), (x_test, y_test), classes
    
    @staticmethod
    def __loaddata(path, data_type):
        """
        Load certain data_type of data (train, val, test)
        """
        #Preparing variables
        data = []
        #Get available classes in dataset_path
        classes = [class_name for class_name in os.listdir(path + '/' + data_type) if os.path.isdir(path + '/train/' + class_name)]

        #Load data
        for label_index, class_name in enumerate(classes):
            #Get all files in the class directory
            file_names = os.listdir(os.path.join(path, data_type, class_name).replace("\\","/"))
            for file_name in file_names:
                #Get file path
                file_path = os.path.join(path, data_type, class_name, file_name).replace("\\","/")
                try:
                    #Get spectrogram data from image file
                    spectrogram = np.array(Image.open(file_path))
                    data.append([spectrogram, label_index])
                except:
                    logger.warn("Failed to load image %s", file_path)
        
        #Shuffle loaded data
        random.shuffle(data)

        #Split X and Y
        x = np.array([spectrogram[0] for spectrogram in data])
        y = np.array([spectrogram[1] for spectrogram in data])
        y = np.array(to_categorical(y, len(classes)))

        return (x, y), classes

class NormTrain(Layer):
    """
    Normalization Layer
    Normalize input in training process from 0-255 to 0-1
    """
    def __init__(self, **kwargs):
        super(NormTrain, self).__init__(**kwargs)

    def get_config(self):
        config = super(NormTrain, self).get_config()
        return config
    
    def call(self, x, training=None):
        if training:
            norm_x =  divide(x, 255)
            return norm_x
        return x

class Rot90(Layer):
    """
    Rotation Layer
    Rotate the input 90deg counter clockwise k times
    """
    def __init__(self, k=1, **kwargs):
        self.k = k
        super(Rot90, self).__init__(**kwargs)

    def get_config(self):
        config = super(Rot90, self).get_config()
        config.update({"k": self.k})
        return config
    
    def call(self, x):
        return rot90(x, self.k, axes=(1, 2))
import os
import sys
import logging
import random

from libs.audiomodule import Audio

import numpy as np
from tensorflow.keras.layers import Layer
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical
from tensorflow.experimental.numpy import rot90 # type: ignore
from PIL import Image

logger = logging.getLogger(__name__)

class NN:
    """
    Neural Network Object
    """

    def __init__(self, model_path, custom_objects, output_map, conf):
        """
        Create Neural Network Object
        """
        #Load config
        self.__model_path = model_path
        self.__classes = conf["classes"]
        self.__output_map = output_map
        
        #NN initialization
        logger.info(self.__model_path)
        self.__model = load_model(self.__model_path, custom_objects)

        #Input buffer
        self.__buffer = []
    
    def getmodelinfo(self):
        """
        Print Model Summary
        """
        self.__model.summary() # type: ignore

    def predict(self, x):
        """
        Predict x using loaded model
        """
        #Predict input x, verbose 0=silent, 1=progress bar, 2=single line
        y = self.__model.predict(x=np.array(x), verbose=0) # type: ignore
        return y
    
    def predictbatch(self, x):
        """
        Predict x using loaded model
        """
        #Predict input x, verbose 0=silent, 1=progress bar, 2=single line
        y = self.__model.predict(x=x, verbose=0) # type: ignore
        return y
    
    def getclass(self, y):
        """
        Get prediction class name
        """
        return self.__classes[np.argmax(y)]
    
    def thresholding(self, nn_result, th):
        """
        Threshold the prediction result
        """
        return self.__classes.index("road_traffic") if np.max(nn_result) < th else np.argmax(nn_result)
    
    def mapresult(self, result):
        """
        Map thresholding result using output map
        """
        return self.__output_map[self.__classes[result]]
    
    def add2buffer(self, x):
        """
        Add feature to buffer
        """
        self.__buffer.append(x)

    def popallbuffer(self):
        """
        Pop all features from buffer
        """
        x, self.__buffer = self.__buffer, []
        return x

    @staticmethod
    def loaddataset(dataset_path, intensity_th = None):
        """
        Load dataset from specified path
        """
        logger.info("Loading train data")
        (x_train, y_train), classes = NN.__loaddata(dataset_path, "train", intensity_th)
        logger.info("Loading validation data")
        (x_val, y_val), classes = NN.__loaddata(dataset_path, "val", intensity_th)
        logger.info("Loading test data")
        (x_test, y_test), classes = NN.__loaddata(dataset_path, "test", intensity_th)

        return (x_train, y_train), (x_val, y_val), (x_test, y_test), classes
        
    @staticmethod
    def loaddatatest(dataset_path, intensity_th = None, shuffle=True):
        """
        Load test data from specified path
        """
        logger.info("Loading test data")
        (x_test, y_test), classes = NN.__loaddata(dataset_path, "test", intensity_th, shuffle)

        return (x_test, y_test), classes
    
    @staticmethod
    def __loaddata(path, data_type, intensity_th, shuffle=True):
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

                    #Normalize data
                    spectrogram = spectrogram / 255.

                    #ratio-based intensity thresholding
                    if intensity_th is not None:
                        spectrogram = Audio.RbIR(spectrogram, intensity_th)

                    data.append([spectrogram, label_index])
                except FileNotFoundError:
                    logger.warn("Failed to load image %s", file_path)
                except KeyboardInterrupt:
                    logger.info("Program terminated")
                    sys.exit(0)
        
        #Shuffle loaded data
        if shuffle:
            random.shuffle(data)

        #Split X and Y
        x = np.array([spectrogram[0] for spectrogram in data])
        y = np.array([spectrogram[1] for spectrogram in data])
        y = np.array(to_categorical(y, len(classes)))

        return (x, y), classes

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
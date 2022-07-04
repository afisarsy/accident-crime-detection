import os
import itertools
import random
import glob
from operator import itemgetter
from collections import deque

from libs.audioprocessing import Preprocessing

import numpy as np
import tensorflow as tf
from tensorflow.python.client import device_lib
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from PIL import Image

def loaddataset(dataset_dir, nn_type, rotate_image=0):
    '''Prepare Variables'''
    datasets = dict()
    datasets['train'] = []
    datasets['val'] = []
    datasets['test'] = []
    
    steps = ['train', 'val', 'test']
    classes = [class_name for class_name in os.listdir(dataset_dir + '/train') if os.path.isdir(os.path.join(dataset_dir, 'train', class_name).replace("\\","/"))]

    '''Load Image'''
    for step in steps:
        for i, class_name in enumerate(classes):
            data_files = os.listdir(os.path.join(dataset_dir, step, class_name).replace("\\","/"))
            for data_file in data_files:
                data_path = os.path.join(dataset_dir, step, class_name, data_file).replace("\\","/")
                spectrogram = np.array(Image.open(data_path))                 #Load image
                if nn_type.lower() == 'rnn':
                    spectrogram = np.rot90(spectrogram, rotate_image)
                spectrogram = spectrogram/255.0
                if nn_type.lower() == 'cnn':
                    spectrogram = np.expand_dims(spectrogram, axis=-1)        #Add last, image channel
                datasets[step].append([spectrogram, i])

        random.shuffle(datasets[step])
    
    x_train = np.array([spectrogram[0] for spectrogram in datasets['train']])
    y_train = np.array([spectrogram[1] for spectrogram in datasets['train']])
    y_train = np.array(to_categorical(y_train, len(classes)))
    x_val = np.array([spectrogram[0] for spectrogram in datasets['val']])
    y_val = np.array([spectrogram[1] for spectrogram in datasets['val']])
    y_val = np.array(to_categorical(y_val, len(classes)))
    x_test = np.array([spectrogram[0] for spectrogram in datasets['test']])
    y_test = np.array([spectrogram[1] for spectrogram in datasets['test']])
    y_test = np.array(to_categorical(y_test, len(classes)))

    return (x_train, y_train), (x_val, y_val), (x_test, y_test), classes

def loaddatatest(dataset_dir, nn_type, rotate_image=None):
    '''Prepare Variables'''
    datasets = dict()
    datasets['test'] = []
    step = 'test'
    classes = [class_name for class_name in os.listdir(dataset_dir + '/test') if os.path.isdir(os.path.join(dataset_dir, 'test', class_name).replace("\\","/"))]

    '''Load Image'''
    for i, class_name in enumerate(classes):
        data_files = os.listdir(os.path.join(dataset_dir, step, class_name).replace("\\","/"))
        for data_file in data_files:
            data_path = os.path.join(dataset_dir, step, class_name, data_file).replace("\\","/")
            spectrogram = np.array(Image.open(data_path)).astype(dtype=np.float32)      #Load image
            if rotate_image is not None:
                spectrogram = np.rot90(spectrogram, rotate_image)
            spectrogram = spectrogram/255.0
            if nn_type.lower() == 'cnn':
                spectrogram = np.expand_dims(spectrogram, axis=-1)        #Add last, image channel
            datasets[step].append([spectrogram, i])

    random.shuffle(datasets[step])
    
    x_test = np.array([spectrogram[0] for spectrogram in datasets['test']])
    y_test = np.array([spectrogram[1] for spectrogram in datasets['test']])
    y_test = np.array(to_categorical(y_test, len(classes)))

    return (x_test, y_test), classes

'''Calculate The Confusion Matrix'''
def getconfusionmatrix(predictions, y_true):
    cm = confusion_matrix(y_pred=np.argmax(predictions, axis=-1), y_true=y_true)
    return cm

'''Plot & Save Confusion Matrix'''
def plotSaveConfusionMatrix(cm, classes, output, normalize=False, title='Confusion Matrix', color_map=plt.cm.Blues):
    plt.figure()
    plt.imshow(cm, interpolation='nearest', cmap=color_map)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print('Normalized Confusion Matrix')
    else:
        print('Confusion Matrix')
    print(cm)

    thresh = cm.max() / 2
    for i,j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
            horizontalalignment='center',
            color='white' if cm[i, j] > thresh else 'black'
        )
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.savefig(output, bbox_inches='tight')
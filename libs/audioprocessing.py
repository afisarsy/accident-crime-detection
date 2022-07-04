from pydub import AudioSegment
from scipy.signal import butter, lfilter, windows
import numpy as np
from numpy import mean, std
from librosa import power_to_db, filters, resample
from librosa.feature import melspectrogram
from librosa.display import specshow
import matplotlib.pyplot as plt

'''Audio Object'''
class Audio:
    @staticmethod
    def loadaudio(path):
        audio = Audio()
        audio.filename = path
        audio.data = AudioSegment.from_wav(path)
        audio.data = audio.data.split_to_mono()[0]
        audio.duration = len(audio.data)
        audio.bitrate = audio.data.frame_rate
        return audio

'''Preprocessing methods'''
class Preprocessing:
    '''Bandpass Filter'''
    @staticmethod
    def butterbandpassfilter(chunk, sampling_rate, low_cut, high_cut, order=5):
        nyq = 0.5 * sampling_rate
        cutoff = [low_cut / nyq, high_cut / nyq]

        b, a = butter(order, cutoff, analog=False, btype='band')
        filtered_data = np.array(lfilter(b, a, chunk)).astype(np.float32) # 16 bit

        return filtered_data

    '''Split Audio by Duration and Overlap Parameter'''
    @staticmethod
    def segmentaudio(audio, chunk_duration, target_sr, overlap_ratio=0.):
        segmented_data = []
        start = 0
        chunk_number = 1
        while start + chunk_duration <= audio.duration:
            chunk = audio.data[start:start+chunk_duration]
            chunk_np = np.array(chunk.get_array_of_samples()).astype(np.float32)/32768 # 16 bit

            chunk_np_resampled = resample(y=chunk_np, orig_sr=audio.bitrate, target_sr=target_sr)
            segmented_data.append(chunk_np_resampled)

            chunk_number += 1
            start += int(chunk_duration * (1. - overlap_ratio))
        
        audio.chunk_duration = chunk_duration
        audio.overlap_ratio = overlap_ratio
        audio.segmented_data = segmented_data
        return audio
    
    '''Calculate MFCC'''
    @staticmethod
    def getmfcc(data, sr, n_mels):
        mfcc = librosa.feature.mfcc(y=data, sr=sr, n_mfcc=n_mels)
        return mfcc

    '''Calculate Mel Spectrogram'''
    @staticmethod
    def getmelspectrogram(data, sr, n_fft=11025, hop_length=2205, n_mels=10):
        mel_spectrogram = melspectrogram(y=data, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels)
        mel_spectrogram_db = power_to_db(mel_spectrogram)
        return mel_spectrogram_db

    '''Mel Spectrogram to Img'''
    @staticmethod
    def melspectrogram2img(S_db):
        S_db = Preprocessing.minmaxnormalization(S_db, min=0.0, max=1.0)
        #S_db = Preprocessing.minmaxnormalization(S_db, [S_db.min(), S_db.max()], min=0, max=255).astype(dtype=np.uint8)
        img = np.flip(S_db, axis=0) # put low frequencies at the bottom in image
        return img
    
    '''Save Mel Spectrogram'''
    @staticmethod
    def savemel(S_db, dst):
        plt.figure(figsize=(S_db.shape[0]/100, S_db.shape[1]/100))
        img = specshow(S_db, sr=sr, x_axis='off', y_axis='off')
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0, hspace=0, wspace=0)
        plt.savefig(dst)
    
    '''Normalization'''
    @staticmethod
    def minmaxnormalization(X, min=0.0, max=1.0):
        X_std = (X - X.min()) / (X.max() - X.min())
        X_scaled = X_std * (max - min) + min
        return X_scaled
    
    '''Create Hann window'''
    @staticmethod
    def gethannwindow(K):
        window = windows.hann(K)
        return window
    
    '''Calculate Min, Max, Mean, Standard Deviation of Mel Spectrogram db with output class'''
    @staticmethod
    def getMMMDCFeature(mel_spectrogram_db, continuous, output_class):
        MMMD_by_freq = [[min(data), max(data), mean(data), std(data)] for data in mel_spectrogram_db]
        MMMD_feature = [data for freq_data in MMMD_by_freq for data in freq_data] + [continuous, output_class]
        return MMMD_feature

def ms2time(milis):
    mseconds=int(milis%1000)
    seconds=int((milis/1000)%60)
    minutes=int((milis/(1000*60))%60)
    return ('' if minutes > 9 else '0') + str(minutes) + ':' + ('' if seconds > 9 else '0') + str(seconds) + '.' + ('' if mseconds > 99 else '0' if mseconds > 9 else '00') + str(mseconds)
import logging

from scipy.signal import butter, lfilter
import numpy as np
from scipy.ndimage import convolve
from scipy.signal.windows import gaussian
from librosa import power_to_db
from librosa.feature import melspectrogram
from skimage.io import imsave
from scipy.io.wavfile import write

logger = logging.getLogger(__name__)

class Audio:
    """
    Audio Object
    """
    @staticmethod
    def bandpassfilter(segment, sampling_rate, cutoff, order=5):
        """
        Butterworth bandpass filter
        """
        nyq = 0.5 * sampling_rate

        b, a = butter(order, [cutoff[0] / nyq, cutoff[1] / nyq], analog=False, btype='band')
        filtered_data = np.array(lfilter(b, a, segment)).astype(np.float32) # 16 bit

        return filtered_data
    
    @staticmethod
    def getmelspectrogram(segment, sampling_rate, n_fft, hop_length, n_mels):
        """
        Calculate and return mel spectrogram (dB) of the segment
        """
        mel_spectrogram = melspectrogram(y=segment, sr=sampling_rate, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels)
        mel_spectrogram_db = power_to_db(mel_spectrogram)
        return mel_spectrogram_db
    
    @staticmethod
    def normalize(S_db):
        """
        Return normalized and flipped (low frequencies at bottom {img}) spectrogram (db)
        """
        S_db = Audio.__minmaxnormalization(S_db, min=0.0, max=1.0)
        normalized = np.flip(S_db, axis=0) # put low frequencies at the bottom in image
        return normalized

    @staticmethod
    def RbIR(image, intensity_th):
        """
        Ratio-based Intensity Reduction
        """
        gaussian_kernel = Audio.creategaussiankernel(3, sigma=3)

        buffer_image = np.copy(image)
        buffer_image[buffer_image < intensity_th] **= 2

        filtered_image = convolve(buffer_image, gaussian_kernel)
        return filtered_image
    
    @staticmethod
    def creategaussiankernel(ksize, sigma=3):
        """
        Create 2D Gaussian Kernel
        """

        gkern1d = gaussian(ksize, std=sigma).reshape(ksize, 1)
        gkern2d = np.outer(gkern1d, gkern1d)
        return gkern2d

    @staticmethod
    def __minmaxnormalization(X, min=0.0, max=1.0):
        """
        Min-Max normalization function
        """
        X_std = (X - X.min()) / (X.max() - X.min())
        X_scaled = X_std * (max - min) + min
        return X_scaled

    @staticmethod
    def savemel(S_db, path):
        """
        Save spetrogram as image
        """
        path += ".png" if path[-4:] != ".png" else ""
        img = (S_db * 255).astype(dtype=np.uint8)
        imsave(path, img)
    
    @staticmethod
    def saveaudio(segment, sampling_rate, path):
        """
        Save audio as wav file
        """
        path += ".wav" if path[-4:] != ".wav" else ""
        write(path, sampling_rate, segment)
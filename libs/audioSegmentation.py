#!/usr/bin/python3
import pyaudio
import numpy as np
import wave
import logging
from python_speech_features import mfcc
from python_speech_features import delta
from python_speech_features import logfbank

mic = pyaudio.PyAudio()

OVERLAP_RATIO = 0.5	#0.1-1, with 0.1 step
SEGMENT_DUR = 0.1	#in second
NFFT = 2048

FORMAT=pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK_DUR = 0.01	#Each chunk duration in second
CHUNK = int(RATE * CHUNK_DUR)
RECORD_SECONDS = 5

stream = mic.open(format=FORMAT,
	channels=CHANNELS,
	rate=RATE,
	frames_per_buffer=CHUNK,
	output=True,
	input=True,
	input_device_index=1)

frames = []

def processSegment():
	segment = b''.join(frames)
	sig = np.frombuffer(segment, np.float32)

if __name__ == '__main__':
	try:
		#Prepare the first data
		min_chunk = int(SEGMENT_DUR / CHUNK_DUR)
		for i in range(0, min_chunk):
			data = stream.read(CHUNK)
			frames.append(data)
		
		#first segment
		processSegment()

		chunk_index = 0
		segment_chunk_limit = int(1 - (OVERLAP_RATIO * 10))
		for i in range(min_chunk, int(RATE / CHUNK * RECORD_SECONDS)):
		#while True:
			data = stream.read(CHUNK)
			chunk_index += 1
			frames.append(data)
			frames.pop(0)
			if chunk_index >= segment_chunk_limit:
				chunk_index = 0
				processSegment()
	except KeyboardInterrupt:
		pass
		
	stream.stop_stream()
	stream.close()
	mic.terminate()
		
	for i in range(0, len(frames)-1):
		"""
		wf = wave.open(str(i)+'.wav', 'wb')
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(mic.get_sample_size(FORMAT))
		wf.setframerate(RATE)
		wf.writeframes(b''.join([frames[i], frames[i + 1]]))
		wf.close()
		"""

import argparse
import logging
from datetime import datetime

import pyaudio
import wave

from libs.logger import initlogger

parser = argparse.ArgumentParser(prog="Audio Recorder")
logger = logging.getLogger(__name__)

def main():
    """
    Record audio for testing purpose
    """
    initargs()
    options = parser.parse_known_args()[0]
    initlogger(options.log)

    output_path = "Tests/8 real_data_test"
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H-%M-%S")
    output_file = "test_record_" + dt_string + ".wav"

    format = pyaudio.paInt16
    channels = 1
    chunk_dur = 0.01
    chunk = int(options.sampling_rate * chunk_dur)

    mic = pyaudio.PyAudio()
    stream = mic.open(
        format=format,
        channels=channels,
        rate = options.sampling_rate,
        frames_per_buffer=chunk,
        input=True,
        input_device_index=options.mic_index
    )
    frames = []

    while True:
        try:
            data = stream.read(chunk)
            frames.append(data)
        except KeyboardInterrupt:
            break
    
    stream.stop_stream()
    stream.close()
    mic.terminate()

    wf = wave.open( output_path + "/" + output_file, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(mic.get_sample_size(format=format))
    wf.setframerate(options.sampling_rate)
    wf.writeframes(b''.join(frames))
    wf.close()

def initargs():
    parser.add_argument(
        "-mic",
        "--mic-index",
        metavar="MIC_INDEX",
        type=int,
        default=1,
        help=(
            "Select used microphone index from available microphone devices. "
            "Use  main.py GET MIC  to get available microphone devices"
        ),
    ),
    parser.add_argument(
        "-sr",
        "--sampling-rate",
        metavar="SR",
        type=int,
        default=44100,
        help=(
            "Specify sampling rate value. "
            "Default 44100"
        )
    )

if __name__ == '__main__':
    main()
import sys
import requests
import json
from scipy import signal
import numpy as np
import pyaudio
import librosa
import time

def getFreqs(url):
    endpoint = url + '/api/filters'
    try:
        res = requests.get(endpoint)
    except BaseException as e:
        print('Error getting filters.')
        print(e)
        sys.exit(1)
    return res.json()

def filter(url):
    freqs = getFreqs(url)
    avg_gain = min(sum([freqs[x]['gain'] for x in range(len(freqs))]), 1)
    fs = 44100 # Sample rate
    fc = max(fs/2 - np.floor(fs/2 * avg_gain), 30) - 10  # Cutoff
    fstop = min((fc + 500), fs/2)  # End the transition band
    #fc = 10000
    #fstop = 10500
    ripple = 3  # 3dB ripple
    atten = 60 # 60dB attenuation
    #print('cutoff = ' + str(fc))
    #print('transition stop = ' + str(fstop))
    # Get the smallest order for the filter
    order, _ = signal.ellipord(fc, fstop, ripple, atten, fs=fs)

    return signal.ellip(order, ripple, atten, fc, fs=fs)

if __name__ == '__main__':


    if(sys.version_info.major < 3):
        logging.error('Please use Python 3.x or higher')
        sys.exit(1)

    if len(sys.argv) != 3:
        raise ValueError('Please provide a filename.')
        print('usage: python disco-player.py <url> <filepath>')
        sys.exit(1)

    URL = sys.argv[1]

    track_data, track_rate = librosa.load(sys.argv[2], sr=44.1e3, dtype=np.float32)

    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()
    count = 0

    # Now construct the filter
    b, a = filter(URL)

    # define callback (2)
    def callback(in_data, frame_count, time_info, status):
        global b, a, count

        track_frame = track_data[frame_count*count : frame_count*(count+1)]

        track_left = signal.filtfilt(b, a, track_frame)
        track_right = signal.filtfilt(b, a, track_frame)

        ret_data = np.empty((track_left.size + track_right.size), dtype=track_left.dtype)
        ret_data[1::2] = track_left
        ret_data[0::2] = track_right
        ret_data = ret_data.astype(np.float32).tostring()
        count += 1
        return (ret_data, pyaudio.paContinue)

    # open stream using callback (3)
    stream = p.open(format=pyaudio.paFloat32,
                    channels=2,
                    rate=int(track_rate),
                    output=True,
                    stream_callback=callback,
                    frames_per_buffer=2**16)

    # start the stream (4)
    stream.start_stream()

    # wait for stream to finish (5)
    while stream.is_active():
        b, a = filter(URL)
        time.sleep(1)
        # Will this loop audio? I hope!
        if not stream.is_active():
            stream.start_stream()

    # stop stream (6)
    stream.stop_stream()
    stream.close()

    # close PyAudio (7)
    p.terminate()

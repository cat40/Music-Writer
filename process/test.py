import pyaudio
import aubio
import numpy
import wave
import os
import time
import pysoundcard
from tempfile import SpooledTemporaryFile
from scipy import fftpack
import random

'''
get tone
use functions in order
'''
#eventually remove time and do one analysis per sample (about 44100 per second)
#Need to find a better way than writing a disk file 44100 times a second
def get_file(time):
    fname = str(int(random.random()*10**9))+'.wav'
    '''makes a temporary wave file in memory
    PyAudio will write to this file as Aubio reads from it
    Might need to change max_size
    '''
    chunk = 1024
    frames = []
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=chunk)
    
    for _ in range(int(44100.0/chunk * time)):
        frames.append(stream.read(chunk))
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    #with SpooledTemporaryFile() as temp:
    temp = wave.open(fname, 'wb')
    temp.setnchannels(1)
    temp.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    temp.setframerate(44100)
    temp.writeframes(b''.join(frames))
    temp.close()
    return fname

def get_pitches(fname):
    #s = aubio.source('AF.wav')
    s=
    samplerate = s.samplerate
    #not sure what these mean
    win_s = 4096
    hop_s = 512
    #aubio.pitch(method, buffer size, hop size, sample rate (see command line docs))
    pitch_o = aubio.pitch('fcomb', win_s, hop_s, samplerate)
    #this makes it put out midi numbers, NOT heartz!!!!!!!!
    #pitch_o.set_unit('midi')
    pitch_o.set_tolerance(0.8)
    read = 512
    while not read < hop_s:
        #seems to run 87 times per second? (check with other samples)
        samples, read = s()
        yield pitch_o(samples)[0]

#this will only analize multiple notes.
#use same process dynamically for live input
def get_lenth(pitches):
    count = 0
    first = True
    pitchold = None
    for pitch in pitches:
        pitch = aubio.freq2note(pitch)
        if pitch == pitchold:
            count += 1
        else:
            pitchold = pitch
            if not first:
                yield (pitchold, count)
            first = False
            count = 0
        
fname = get_file(5)
time.sleep(1)
for pitch in get_pitches(fname):
    print pitch
    print aubio.freq2note(pitch)
#os.remove(fname)

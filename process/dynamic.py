import aubio
import wave
import sys
import os
import pysoundcard as sound
searchPath = os.path.dirname(os.path.abspath('.'))
sys.path.append(searchPath)
import music
sys.path.remove(searchPath)

#s = aubio.source(sound.Stream())
#this gets called 44100/hop_size times per second
def get_file():
    fname = str(int(random.random()*10**9))+'.wav'
    '''
    makes a temporary wave file.
    PyAudio will write to this file as Aubio reads from it
    '''
    chunk = 1024
    frames = []
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=chunk)
    
    #for _ in range(int(44100.0/chunk*time)):
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
    count = 0
    s = aubio.source(fname)
    #s = aubio.source()
    samplerate = s.samplerate
    #not sure what these mean
    win_s = 4096
    hop_s = 512
    #aubio.pitch(method, buffer size, hop size, sample rate (see command line docs))
    pitch_o = aubio.pitch('yin', win_s, hop_s, samplerate)
    #this makes it put out midi numbers, NOT heartz!!!!!!!!
    #pitch_o.set_unit('midi')
    pitch_o.set_tolerance(0.8)
    read = 512
    while not read < hop_s:
        #seems to run 87 times per second? (check with other samples)
        samples, read = s()
        #pitch, time(seconds)
        yield pitch_o(samples)[0], count/87.
        count += 1

#this will "freeze" the program until a note change.
#Not sure if GUI will stop responding
#count might be 1 less than should be
#don't use this. Use a similar handling in the main file
# to do other stuff while reciving live input
#might not even work unless each frame of input is at least one note
def get_note():
    new = True
    count = 0
    for pitch in get_pitches(get_file())[0]:
        try: pitchName = aubio.freq2note(pitch)
        except ValueError: pass
        else:
            if new:
                pitchold = pitch
                pitcholdName = aubio.freq2note(pitch)
                new = False
            elif pitchName == pitcholdName:
                count += 1
            else:
                new = True
                yield music.Note(pitchold, count)
                count = 0
##    #need to add error handling(abuio does not like low inputs from noise)
##    try:
##        pitchStart = pitchold = pitch = get_pitches(get_file())
##    except ValueError:
##        noteName = 'error'
##    if pitch == 0:
##        noteName = 'rest'
##    else:
##        noteName = aubio.freq2note(pitch)
##    count = 0
##    while aubio.freq2note(pitch) == aubio.freq2note(pitchold):
##        count += 1
##        pitchold = pitch
##    return Note(pitchStart, count)

#takes a list of notes (pitch, count) and makes it into musical note
#(pitch, note)
#Expresses notes as fractions of the first note
def analyze_notes(notelist):
    first = True
    for note in notelist:
        if first:
            lenth = note.count
            frac = 1.0
        else:
            frac = lenth/float(note.count)
        yield frac

#eventually make this an infinate process
#that continues until a key press interrupts it
#temporary function to be added to GUI handling in the main file
def run(time):
    rate = 500 #sample rate per second
    for _ in range(int(time/rate)):
        print get_note().name

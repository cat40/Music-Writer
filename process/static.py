import aubio
import dynamic
import sys
import os
from variables import hopsize, winsize, samplerate
from numpy import median, diff
searchPath = os.path.dirname(os.path.abspath('.'))
sys.path.append(searchPath)
import music
sys.path.remove(searchPath)
#from . import music

#This does NOT catch note oscelations over a single hop, if the hop falls on a note change
#Instead, it breaks and returns the same note.
#Possibly fix this by yeilding on a one-note delay
#    - Check if note == previous note, in which case don't yeild until note != previous note (might need to sum times)
#However, those are probably inaccurate oscelations
def get_notes(fname):
    #next(p_iter(), default_value) does not raise exception on end, p_iter.next() does
    pitches = dynamic.get_pitches(fname)
    p_iter = iter(pitches)
    pitchname = oldpitchname = None
    pitch = True
    while pitch:
        pitch, time = next(p_iter, (None, None))
        oldtime = time
        pitchold = pitch
        pitchname = oldpitchname = aubio.freq2note(pitch)
        count = 0
        slightlyoldtime = 0
        while pitchname == oldpitchname:
            #gets next pitch and timestamp
            slightlyoldtime = time
            pitch, time = next(p_iter, (None, None))
            #break loop if iterator is out. 
            if not pitch: break
            pitchname = aubio.freq2note(pitch)
            print pitchname, oldpitchname
            count += 1
        yield music.Note(oldpitchname, count, slightlyoldtime-oldtime)
            
            
##    new = True
##    count = 0
##    oldtime = 0
##    maintime = 0
##    pitcholdName = None
##    #next try a pair of while loops while using iter object and iter.next()
##    for pitch, time in dynamic.get_pitches(fname):
##        time -= oldtime
##        try: pitchName = aubio.freq2note(pitch) if pitch != 0 else 'rest'
##        except ValueError: pitchName = 'rest'
##        else:
##            if not new:
##                if pitchName == pitcholdName:
##                    count += 1
##                    maintime += time
##                else:
##                    yield music.Note(pitchold, count, maintime)
##                    pitchold = pitch
##                    pitcholdName = aubio.freq2note(pitch) if pitch != 0 else 'rest'
##                    count = 0
##                    maintime = 0
##                #print pitchName, pitcholdName
##            else:
##                new = False
##                pitchold = pitch
##                pitcholdName = aubio.freq2note(pitch) if pitch != 0 else 'rest'
##        oldtime += time
                
#does not do tempo changes yet
def get_bpm(fname):
    s = aubio.source(fname)
    t = aubio.tempo('specdiff', winsize, hopsize, samplerate)
    beats = []
    read = hopsize
    jumpsize = 5 #evaluate if tempo changed at this interval
    tempos = []
    readed = 0
    tempochange = False
    while read >= hopsize:
##        if len(tempos) >= 5:
##            print 60./diff(tempos)
##            first = True
##            #this stays above for loops
##            if tempochange:
##                tempochange = False
##                if median(60./diff(tempos)) >= changedto-10 and median(60./diff(tempos)) <= changedto+10 and changedto != median(60./diff(beats)):
##                    yield median(60./diff(beats[:-10])), float(changeoccured)/hopsize#take last ten beats out because they would be a different tempo
##                    beats = beats[-5:]
##            #these for loops must stay seperate or stuff will be done to tempos before they are all rounded
##            else:
##                tempos = 60./diff(tempos)
##                for i, temp in enumerate(tempos):
##                    tempos[i] = round(temp, -1)
##                oldtempo = tempos[0]
##                for i, temp in enumerate(tempos):
##                    if i < len(tempos)-1:
##                        if not (temp <= tempos[i+1]+10 and temp >= tempos[i+1]-10):
##                            if first:
##                                changeoccured = readed
##                                first = False
##                            tempochange = True
##                            changedto = tempos[i+1]
##                tempos = []                
        readed += 1
        samples, read = s()
        if t(samples):
            bpm = t.get_last_s()
##            tempos.append(bpm)
            beats.append(bpm)
##    yield median(60./diff(beats)), float(readed)/hopsize
    return median(60./diff(beats))
    
###go through each note and change values until they make sense
##def reason_notes(notes):
##    

c = 0
for note in get_notes('a3.wav'):
    print note.name, note.time
    c += 1
    if c > 25:
        break

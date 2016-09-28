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
    def get_notes_helper(fname):
        #next(p_iter(), default_value) does not raise exception on end, p_iter.next() does
        pitches = dynamic.get_pitches(fname)
        p_iter = iter(pitches)
        pitchname = oldpitchname = None
        pitch = True
        while pitch:
            pitch, time = next(p_iter, (None, None))
            print pitch, time
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
                count += 1
            yield music.Note(oldpitchname, count, slightlyoldtime)            
    oldnote = None
    newtime = 0
    newcount = 0
    count = 0
    oldtime = 0
    notes = get_notes_helper(fname)
    for note in notes:
        if oldnote:
            if note.name == oldnote.name:
                newtime = note.time
                count += note.count
            else:
                yield music.Note(oldnote.name, count, newtime-oldtime)
                count = 0
                newtime = 0
                oldtime = newtime
        oldnote = note
    yield music.Note(oldnote.name, count, newtime-oldtime)
                
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

##def get_key(notes):
##    keys = {0:'C', 1:'G', 2:'D', 3:'A', 4:'E', 5:'B', 6:'F#',
##            -1:'F', -2:'Bb', -3:'Eb', -4:'Ab', -5:'Db'}
##    #sharps
##    for note in notes:     
        
c = 0
for note in get_notes('notebreak.wav'):
    print note.name, note.time

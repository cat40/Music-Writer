import mic
import process
import aubio

#this will "freeze" the program until a note change.
#Not sure if GUI will stop responding
class Note(object):
    def __init__(self, pitch, count):
        self.pitch = pitch
        self.count = count
        self.frac = 

def get_note():
    #need to add error handling(abuio does not like low inputs from noise)
    pitchold = pitch = process.get_pitches(mic.get_file())
    if pitch == 0:
        noteName = 'rest'
    else:
        noteName = aubio.freq2note(pitch)
    count = 0
    while aubio.freq2note(pitch) == aubio.freq2note(pitchold):
        count += 1
    return Note(noteName, count)

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
        yield note.
            
    

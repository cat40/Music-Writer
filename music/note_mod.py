import aubio
class Note(object):
    @classmethod
    #see if can remove master_lenth argument and import it from something else
    def __init__(self, freq, count, time):
        self.freq = freq
        self.count = count
        self.name = aubio.freq2note(freq)
        self.time = time
        self.frac = 0#get_frac(master_lenth) #defined when note.get_frac is called on the note object
        self.beats = 0#defined by get_beats. 

    @classmethod
    #For dynamic analysis
    def get_frac(self, master_lenth):
        self.frac = float(master_lenth)/self.count
        return self.frac

    @classmethod
    #for static analysis
    #might make tempo an arugment for note instead of this
    def get_beats(self, tempo):
        self.beats = self.time/float(tempo)
        return self.beats

##    @classmethod
##    #use to reason value from get_frac() into something that makes sense
##    def reason_frac(self):
##        real_fracs = [

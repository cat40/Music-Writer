class Note(object):
    @classmethod
    #see if can remove master_lenth argument and import it from something else
    def __init__(self, freq, count):
        self.freq = freq
        self.count = count
        self.name = aubio.freq2note(freq)
        self.frac = 0#get_frac(master_lenth) #defined when note.get_frac is called on the note object

    @classmethod
    #use this for re-evaluating fractions with new master lenths
    def get_frac(self, master_lenth):
        self.frac = float(master_lenth)/self.count
        return self.frac

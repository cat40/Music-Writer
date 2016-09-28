class Note(object):
    #see if can remove master_lenth argument and import it from something else
    def __init__(self, name, count, time):
        self.count = count
        self.name = name
        self.time = time
        self.frac = 0#get_frac(master_lenth) #defined when note.get_frac is called on the note object
        self.beats = 0#defined by get_beats. 

    #For dynamic analysis
    def get_frac(self, master_lenth):
        self.frac = float(master_lenth)/self.count
        return self.frac

    #for static analysis
    #might make tempo an arugment for note instead of this
    def get_beats(self, tempo):
        self.beats = self.time/float(tempo)
        return self.beats

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

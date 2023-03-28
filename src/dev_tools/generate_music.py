"""
I am the developer of this library :).
Its named PyMusic-Instrument.
PyAudio doesn't supports 3.11 now :(.

See installation page at https://pymusic-instrument.readthedocs.io/en/latest/installation.html#installation
"""


from Instrument import Instrument

if __name__ == '__main__':
    piano = Instrument.Instrument()
    # 28 30 32 33 47
    # C  D  E  F  G

    # Gregorian chant dies irae.
    piano.record_key(33, 0.5)
    piano.record_key(32, 0.5)
    piano.record_key(33, 0.5)
    piano.record_key(30, 0.5)
    piano.record_key(32, 0.5)
    piano.record_key(30, 0.5)
    piano.record_key(28, 0.5)

    piano.to_wav("recording.wav")

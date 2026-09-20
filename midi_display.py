import mido

midi = mido.MidiFile("contrapunctusI.mid")

for track in midi.tracks:
    for event in track:
        print(event)

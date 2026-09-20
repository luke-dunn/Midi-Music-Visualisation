import mido


def load_midi_notes(filename):
    midi = mido.MidiFile(filename)

    notes = []
    current_time = 0.0
    active = {}

    for msg in mido.merge_tracks(midi.tracks):
        current_time += mido.tick2second(
            msg.time,
            midi.ticks_per_beat,
            500000
        )

        if msg.type == "note_on" and msg.velocity > 0:
            active[msg.note] = (current_time, msg.velocity)

        elif msg.type in ("note_off", "note_on"):
            if msg.note in active:
                start, velocity = active.pop(msg.note)

                notes.append({
                    "pitch": msg.note,
                    "start": start,
                    "duration": current_time - start,
                    "velocity": velocity
                })

    return notes

import math
import numpy as np


def note_to_helix(note):
    pitch = note["pitch"]

    angle = 2 * math.pi * (pitch % 12) / 12
    octave = (pitch - 60) / 12

    radius = 1.0

    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    z = octave

    return np.array([x, y, z])

def generate_midi_geometry(notes):
    lines = []

    if len(notes) < 2:
        return lines

    points = [note_to_helix(note) for note in notes]

    for i in range(len(points) - 1):
        lines.append((points[i], points[i + 1]))

    return lines




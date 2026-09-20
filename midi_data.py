import mido


def read_notes(filename):

    midi = mido.MidiFile(filename)

    active = {}
    notes = []
    current_time = 0.0

    for msg in midi:

        current_time += msg.time

        if msg.type == "note_on" and msg.velocity > 0:

            key = (msg.channel, msg.note)

            active.setdefault(key, []).append({
                "start": current_time,
                "velocity": msg.velocity,
                "program": 0
            })

        elif msg.type == "note_off" or (
            msg.type == "note_on" and msg.velocity == 0
        ):

            key = (msg.channel, msg.note)

            if key in active and active[key]:

                start_info = active[key].pop(0)

                notes.append({
                    "start": start_info["start"],
                    "end": current_time,
                    "duration": current_time - start_info["start"],
                    "pitch": msg.note,
                    "channel": msg.channel
                })

    return notes, current_time

import math


palette = [
    (240, 90, 90),
    (90, 200, 240),
    (240, 190, 80),
    (130, 220, 130),
    (190, 120, 240),
    (240, 130, 190),
    (100, 220, 200),
    (220, 220, 100),
]

PITCH_RADIUS = 1.0
PITCH_SPACING = 0.18
CENTRE_PITCH = 60


def build_radial_geometry(notes):

    channels = sorted(
        set(note["channel"] for note in notes)
    )

    channel_depth = {}

    for i, channel in enumerate(channels):

        if len(channels) == 1:
            z = 0.0
        else:
            z = -1.5 + (
                3.0 * i / (len(channels) - 1)
            )

        channel_depth[channel] = z

    for note in notes:

        note["z"] = channel_depth[note["channel"]]

        pitch_offset = note["pitch"] - CENTRE_PITCH
        angle = math.tau * pitch_offset / 12.0

        note["x"] = PITCH_RADIUS * math.cos(angle)
        note["y"] = PITCH_RADIUS * math.sin(angle)

        note["z"] += pitch_offset * PITCH_SPACING

        note["dx"] = math.cos(angle)
        note["dy"] = math.sin(angle)

        note["length"] = (
            0.10 + note["duration"] * 0.45
        )

        note["width"] = max(
            1,
            int(2 + (note["pitch"] - 36) / 8)
        )

        note["colour"] = palette[
            note["channel"] % len(palette)
        ]

    return channels, channel_depth


def build_whirly_geometry(notes):

    channels = sorted(
        set(note["channel"] for note in notes)
    )

    channel_depth = {}

    for i, channel in enumerate(channels):

        if len(channels) == 1:
            z = 0.0
        else:
            z = -1.5 + (
                3.0 * i / (len(channels) - 1)
            )

        channel_depth[channel] = z

    # Find pitch range
    pitches = [note["pitch"] for note in notes]
    centre_pitch = sum(pitches) / len(pitches)

    for note in notes:

        # Time runs horizontally
        note["x"] = (
            note["start"] / max(n["end"] for n in notes)
        ) * 3.0 - 1.5

        # Pitch runs vertically
        note["y"] = (
            note["pitch"] - centre_pitch
        ) * 0.035

        # Voice/channel occupies depth
        pitch_offset = note["pitch"] - centre_pitch

        note["z"] = (
            channel_depth[note["channel"]]
            + pitch_offset * 0.05
        )

        # Notes initially travel along time axis
        note["dx"] = 1.0
        note["dy"] = 0.0

        note["length"] = max(
            0.015,
            note["duration"] * 0.12
        )

        note["width"] = 7

        note["colour"] = palette[
            note["channel"] % len(palette)
        ]

    return channels, channel_depth



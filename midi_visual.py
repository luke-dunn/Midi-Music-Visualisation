import random
from settings import *
from midi_data import read_notes
from transform3d import rotate_point, project_point
from geometry import build_whirly_geometry
from video_export import synthesize_midi, encode_video, add_soundtrack
from renderer import render_frames

# ------------------------------------------------------------
# READ MIDI
# ------------------------------------------------------------

notes, duration = read_notes(MIDI_FILE)

print("Notes:", len(notes))
print("Duration:", round(duration, 2), "seconds")

channels, channel_depth = build_whirly_geometry(notes)

print("Channels:", channels)
print("Depth layers:", channel_depth)

render_frames(notes, duration)

synthesize_midi(
    MIDI_FILE,
    SOUNDFONT,
    WAV_FILE
)

encode_video(
    FRAMES_DIR,
    FPS,
    SILENT_VIDEO
)

add_soundtrack(
    SILENT_VIDEO,
    WAV_FILE,
    OUTPUT_VIDEO
)

print()
print("DONE:", OUTPUT_VIDEO)

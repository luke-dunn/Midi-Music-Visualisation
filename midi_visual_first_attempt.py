import mido
import random
import math
import subprocess
import os

from PIL import Image, ImageDraw


# ------------------------------------------------------------
# SETTINGS
# ------------------------------------------------------------

MIDI_FILE = "bach.mid"
SOUNDFONT = "/usr/share/sounds/sf2/FluidR3_GM.sf2"

WIDTH = 1080
HEIGHT = 1920
FPS = 25

BACKGROUND = (10, 12, 18)

FRAMES_DIR = "frames"+str(random.randint(100000,200000))
WAV_FILE = "bach.wav"
SILENT_VIDEO = "silent.mp4"
OUTPUT_VIDEO = "bach_visual.mp4"

random.seed(42)


# ------------------------------------------------------------
# READ MIDI
# ------------------------------------------------------------

def read_notes(filename):

    midi = mido.MidiFile(filename)

    active = {}
    notes = []

    # mido.play-style iteration gives messages with
    # time already converted into seconds.
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


notes, duration = read_notes(MIDI_FILE)

print("Notes:", len(notes))
print("Duration:", round(duration, 2), "seconds")


# ------------------------------------------------------------
# GIVE EACH NOTE ITS VISUAL IDENTITY
# ------------------------------------------------------------

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


for note in notes:

    note["x"] = random.randint(100, WIDTH - 100)
    note["y"] = random.randint(100, HEIGHT - 100)

    angle = random.uniform(0, math.tau)

    note["dx"] = math.cos(angle)
    note["dy"] = math.sin(angle)

    # Duration determines final line length.
    note["length"] = 80 + note["duration"] * 350

    # Pitch determines width.
    note["width"] = max(1, int(2 + (note["pitch"] - 36) / 8))

    # For this first experiment MIDI channel acts as
    # our instrument/voice colour.
    note["colour"] = palette[note["channel"] % len(palette)]


# ------------------------------------------------------------
# RENDER FRAMES
# ------------------------------------------------------------

os.makedirs(FRAMES_DIR, exist_ok=True)

total_frames = math.ceil(duration * FPS)

print("Frames:", total_frames)


for frame_number in range(total_frames):

    t = frame_number / FPS

    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)

    for note in notes:

        if t < note["start"]:
            continue

        # Completed notes remain fully visible.
        if t >= note["end"]:
            progress = 1.0
        else:
            progress = (
                (t - note["start"]) /
                max(note["duration"], 0.0001)
            )

        length = note["length"] * progress

        x1 = note["x"]
        y1 = note["y"]

        x2 = x1 + note["dx"] * length
        y2 = y1 + note["dy"] * length

        draw.line(
            (x1, y1, x2, y2),
            fill=note["colour"],
            width=note["width"]
        )

    filename = os.path.join(
        FRAMES_DIR,
        f"frame_{frame_number:06d}.png"
    )

    image.save(filename)

    if frame_number % 100 == 0:
        print(
            f"Rendering {frame_number}/{total_frames}"
        )


# ------------------------------------------------------------
# SYNTHESIZE MIDI
# ------------------------------------------------------------

print("Synthesizing MIDI...")

subprocess.run([
    "fluidsynth",
    "-ni",
    SOUNDFONT,
    MIDI_FILE,
    "-F",
    WAV_FILE,
    "-r",
    "44100"
], check=True)


# ------------------------------------------------------------
# CREATE VIDEO
# ------------------------------------------------------------

print("Encoding video...")

subprocess.run([
    "ffmpeg",
    "-y",
    "-framerate", str(FPS),
    "-i", f"{FRAMES_DIR}/frame_%06d.png",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-r", str(FPS),
    SILENT_VIDEO
], check=True)


# ------------------------------------------------------------
# ADD AUDIO + AAC ENCODING
# ------------------------------------------------------------

print("Adding soundtrack...")

subprocess.run([
    "ffmpeg",
    "-y",
    "-i", SILENT_VIDEO,
    "-i", WAV_FILE,
    "-c:v", "copy",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    OUTPUT_VIDEO
], check=True)


print()
print("DONE:", OUTPUT_VIDEO)

# settings.py

import math
import random

MIDI_FILE = "MozartWA-KV525-mov-01.mid"
SOUNDFONT = "/usr/share/sounds/sf2/FluidR3_GM.sf2"

WIDTH = 1080
HEIGHT = 1920
FPS = 25

# 3D
WORLD_SCALE = 650
CAMERA_DISTANCE = 4.5

ROTATIONS = 1.0
TILT = math.radians(18)

# Appearance
BACKGROUND = (10, 12, 18)

# Files
FRAMES_DIR = "frames" + str(random.randint(100000, 200000))
WAV_FILE = "mozart_01.wav"
SILENT_VIDEO = "silent.mp4"
OUTPUT_VIDEO = "Mozart_01.mp4"

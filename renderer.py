import math
import os

from PIL import Image, ImageDraw

from settings import (
    WIDTH,
    HEIGHT,
    FPS,
    ROTATIONS,
    BACKGROUND,
    FRAMES_DIR,
)

from transform3d import rotate_point, project_point
def draw_voice_connections(draw, notes, t, rotation):

    # Group notes by MIDI channel
    channels = {}

    for note in notes:
        channels.setdefault(
            note["channel"], []
        ).append(note)

    for channel_notes in channels.values():

        # Ensure chronological order
        channel_notes.sort(
            key=lambda note: note["start"]
        )

        for previous, current in zip(
            channel_notes,
            channel_notes[1:]
        ):

            # Don't draw connections into the future
            if current["start"] > t:
                break

            # 3D positions
            x1 = previous["x"]
            y1 = previous["y"]
            z1 = previous["z"]

            x2 = current["x"]
            y2 = current["y"]
            z2 = current["z"]

            # Rotate
            x1, y1, z1 = rotate_point(
                x1, y1, z1, rotation
            )

            x2, y2, z2 = rotate_point(
                x2, y2, z2, rotation
            )

            # Project
            sx1, sy1 = project_point(x1, y1, z1)
            sx2, sy2 = project_point(x2, y2, z2)

            draw.line(
                (sx1, sy1, sx2, sy2),
                fill=current["colour"],
                width=2
            )

def render_frames(notes, duration):

    os.makedirs(FRAMES_DIR, exist_ok=True)

    total_frames = math.ceil(duration * FPS)

    print("Frames:", total_frames)

    for frame_number in range(total_frames):

        t = frame_number / FPS

        rotation = (
            frame_number / total_frames
        ) * math.tau * ROTATIONS

        image = Image.new(
            "RGB",
            (WIDTH, HEIGHT),
            BACKGROUND
        )

        draw = ImageDraw.Draw(image)

        draw_voice_connections(
            draw,
            notes,
            t,
            rotation
        )

        for note in notes:
            if t < note["start"]:
                continue

            # Completed notes remain visible
            if t >= note["end"]:
                progress = 1.0
            else:
                progress = (
                    (t - note["start"]) /
                    max(note["duration"], 0.0001)
                )

            length = note["length"] * progress

            # Line endpoints in 3D
            x1 = note["x"]
            y1 = note["y"]
            z1 = note["z"]

            x2 = x1 + note["dx"] * length
            y2 = y1 + note["dy"] * length
            z2 = z1

            # Rotate
            x1, y1, z1 = rotate_point(
                x1, y1, z1, rotation
            )

            x2, y2, z2 = rotate_point(
                x2, y2, z2, rotation
            )

            # Project
            sx1, sy1 = project_point(x1, y1, z1)
            sx2, sy2 = project_point(x2, y2, z2)

            draw.line(
                (sx1, sy1, sx2, sy2),
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

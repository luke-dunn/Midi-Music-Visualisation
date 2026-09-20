# video_export.py

import subprocess


def synthesize_midi(midi_file, soundfont, wav_file):

    print("Synthesizing MIDI...")

    subprocess.run([
        "fluidsynth",
        "-ni",
        soundfont,
        midi_file,
        "-F",
        wav_file,
        "-r",
        "44100"
    ], check=True)

def encode_video(frames_dir, fps, silent_video):

    print("Encoding video...")

    subprocess.run([
        "ffmpeg",
        "-y",
        "-framerate", str(fps),
        "-i", f"{frames_dir}/frame_%06d.png",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-r", str(fps),
        silent_video
    ], check=True)


def add_soundtrack(silent_video, wav_file, output_video):

    print("Adding soundtrack...")

    subprocess.run([
        "ffmpeg",
        "-y",
        "-i", silent_video,
        "-i", wav_file,
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_video
    ], check=True)

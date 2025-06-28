import os

SAMPLE_RATE    = 16_000
FRAME_MS       = 20
FRAME_SIZE     = int(SAMPLE_RATE * FRAME_MS / 1000)
SILENCE_THRESH = 0.01
SILENCE_MS     = 500
SILENCE_FRAMES = int(SILENCE_MS / FRAME_MS)
AUDIO_DIR      = "audio"
INPUT_WAV      = os.path.join(AUDIO_DIR, "input.wav")
OUTPUT_AUDIO   = os.path.join(AUDIO_DIR, "output.mp3")

OPENAI_API_KEY = ""
OPENAI_API_BASE = "https://api.openai.com/v1"

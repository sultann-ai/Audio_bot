import os
import queue
import numpy as np
import sounddevice as sd
from config.settings import *

def rms(frame: np.ndarray) -> float:
    return np.sqrt(np.mean(frame**2))

def ensure_audio_dir():
    os.makedirs(AUDIO_DIR, exist_ok=True)

class AudioAgent:
    def __init__(self):
        self.q = queue.Queue()
        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE, channels=1,
            blocksize=FRAME_SIZE, callback=self._callback
        )
        self.buffer = []
        self.silent_count = 0

    def _callback(self, indata, frames, time, status):
        self.q.put(indata[:, 0].copy())

    def start(self):
        self.stream.start()

    def stop(self):
        self.stream.stop()

    def read_utterance(self) -> np.ndarray:
        frame = self.q.get()
        self.buffer.append(frame)
        if rms(frame) < SILENCE_THRESH:
            self.silent_count += 1
        else:
            self.silent_count = 0

        if self.silent_count > SILENCE_FRAMES and self.buffer:
            utt = np.concatenate(self.buffer)
            self.buffer.clear()
            self.silent_count = 0
            return utt
        return None

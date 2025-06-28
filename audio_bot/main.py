from config.settings import *
from utils.recorder import AudioAgent, ensure_audio_dir
from utils.api import transcribe, chat_reply, synthesize
from utils.playback import play_file
from scipy.io.wavfile import write

def main():
    ensure_audio_dir()
    agent = AudioAgent()
    history = []

    print("▶️ Starting... speak into your mic.")
    agent.start()
    try:
        while True:
            utt = agent.read_utterance()
            if utt is None:
                continue

            pcm = (utt * 32767).astype("int16")
            write(INPUT_WAV, SAMPLE_RATE, pcm)

            text = transcribe(INPUT_WAV)
            print("👤 You:", text)

            reply = chat_reply(text, history)
            print("🤖 Bot:", reply)
            history.extend([
                {"role": "user", "content": text},
                {"role": "assistant", "content": reply}
            ])

            synthesize(reply, OUTPUT_AUDIO)
            play_file(OUTPUT_AUDIO)
            print("—" * 40)
    except KeyboardInterrupt:
        print("\n🛑 Exiting.")
        agent.stop()

if __name__ == "__main__":
    main()

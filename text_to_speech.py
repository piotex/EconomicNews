import os
import subprocess
import time

text_ts = "Minister Izraela straszy? Użycie bomby jądrowej w Gazie jest opcją."
out_file_mp3 = "hello.mp3"
out_file_vvt = "hello.mp3"
voice_model = "pl-PL-ZofiaNeural"  # pl-PL-MarekNeural
command = f"edge-tts --text \"{text_ts}\" --write-media {out_file_mp3} --write-subtitles {out_file_vvt} --voice {voice_model}"
subprocess.run(command, shell=True, timeout=None)
while not (os.path.isfile(out_file_mp3)):
    time.sleep(0.1)

print("Polecenie zostało zakończone")

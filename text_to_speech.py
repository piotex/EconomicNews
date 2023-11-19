import os
import subprocess
import time
import dataclasses
import json
from models.model_news import model_news
from pydub import AudioSegment
import asyncio
import edge_tts
##########################################

async def edge_tts_generate_to_file(text, voice, file) -> None:
    communicate = edge_tts.Communicate(text, voice, rate="+30%")
    await communicate.save(file)


path_in_data = "important_files/4_sort_by_comments_count.json"
path_out_data = "important_files/5_text_to_speech.json"

with open(path_in_data, "r") as json_file:
    data_from_json = json.load(json_file)
my_class_objects = [model_news(**item) for item in data_from_json]

voice_model = "pl-PL-ZofiaNeural"  # pl-PL-MarekNeural
i = 1
for elem in my_class_objects:
    text_data = elem.header
    out_file_mp3 = f"audio/{i}.header.mp3"
    out_file_vvt = f"audio/{i}.header.vvt"
    # command = f"edge-tts --text \"{text_data}\" --write-media {out_file_mp3} --write-subtitles {out_file_vvt} --voice {voice_model}"
    # subprocess.run(command, shell=True, timeout=None)
    # while not (os.path.isfile(out_file_mp3)):
    #     time.sleep(0.1)
    # elem.audio_header_path = out_file_mp3

    text_data = elem.quick_info
    out_file_mp3 = f"audio/{i}.quick_info.mp3"
    out_file_vvt = f"audio/{i}.quick_info.vvt"
    # command = f"edge-tts --text \"{text_data}\" --write-media {out_file_mp3} --write-subtitles {out_file_vvt} --voice {voice_model}"
    # subprocess.run(command, shell=True, timeout=None)
    # while not (os.path.isfile(out_file_mp3)):
    #     time.sleep(0.1)
    # elem.audio_quick_info_path = out_file_mp3

    loop = asyncio.get_event_loop_policy().get_event_loop()
    try:
        loop.run_until_complete(edge_tts_generate_to_file(text_data, voice_model, out_file_mp3))
    finally:
        loop.close()

    i += 1

    print("ala ma kotea")
    break

# for elem in my_class_objects:
#     audio = AudioSegment.from_file(elem.audio_header_path, format="mp3")
#     sped_up = audio.speedup(playback_speed=1.5)
#     sped_up.export(elem.audio_header_path, format="mp3")

news_dict_list = [dataclasses.asdict(news) for news in my_class_objects]
with open(path_out_data, "w") as json_file:
    json.dump(news_dict_list, json_file, indent=4)

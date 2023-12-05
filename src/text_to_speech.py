import sys
import json
import asyncio
import edge_tts
import dataclasses
from models.model_news import NewsModel
from general_utils import get_idx_to_process


async def edge_tts_generate_to_file(text, voice, path_mp3, path_vvt) -> None:
    communicate = edge_tts.Communicate(text, voice, rate="+30%")
    await communicate.save(path_mp3)

    sub_maker = edge_tts.SubMaker()
    with open(path_mp3, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                sub_maker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])

    with open(path_vvt, "w", encoding="utf-8") as file:
        file.write(sub_maker.generate_subs())


async def wrapper_edge_tts_generate_to_file(elem, voice_model):
    await edge_tts_generate_to_file(elem.quick_info, voice_model, elem.audio_quick_info_mp3_path,
                                    elem.audio_quick_info_vvt_path)


def text_to_speech(idx_to_process: int):
    func_name = "text_to_speech"
    print(f"{func_name}: {idx_to_process}")
    path_news_list = "../data_files/important_files/news_list.json"

    with open(path_news_list, "r") as json_file:
        data_from_json = json.load(json_file)
    my_class_objects = [NewsModel(**item) for item in data_from_json]

    idx = 0
    for elem in my_class_objects:
        if idx == idx_to_process:
            voice_model = "pl-PL-ZofiaNeural"  # pl-PL-MarekNeural
            elem.audio_quick_info_mp3_path = f"../data_files/audio/{elem.id}.quick_info.mp3"
            elem.audio_quick_info_vvt_path = f"../data_files/audio/{elem.id}.quick_info.vvt"
            try:
                asyncio.run(wrapper_edge_tts_generate_to_file(elem, voice_model))
                break
            except Exception as exxx:
                print(exxx)
                pass
        idx += 1

    news_dict_list = [dataclasses.asdict(news) for news in my_class_objects]
    with open(path_news_list, "w") as json_file:
        json.dump(news_dict_list, json_file, indent=4)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        idx_to_process_arg = get_idx_to_process()
        text_to_speech(idx_to_process_arg)
    else:
        for i in range(5):
            text_to_speech(i)

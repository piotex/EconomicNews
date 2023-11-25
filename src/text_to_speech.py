import dataclasses
import json
from models.model_news import NewsModel
import asyncio
import edge_tts


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


def text_to_speech():
    path_in_data = "../data_files/important_files/4_sort_by_comments_count.json"
    path_out_data = "../data_files/important_files/5_text_to_speech.json"

    with open(path_in_data, "r") as json_file:
        data_from_json = json.load(json_file)
    my_class_objects = [NewsModel(**item) for item in data_from_json]

    voice_model = "pl-PL-ZofiaNeural"  # pl-PL-MarekNeural
    loop = asyncio.get_event_loop_policy().get_event_loop()
    for elem in my_class_objects:
        elem.audio_quick_info_mp3_path = f"../data_files/audio/{elem.id}.quick_info.mp3"
        elem.audio_quick_info_vvt_path = f"../data_files/audio/{elem.id}.quick_info.vvt"
        try:
            loop.run_until_complete(edge_tts_generate_to_file(elem.quick_info, voice_model, elem.audio_quick_info_mp3_path, elem.audio_quick_info_vvt_path))
        except Exception as exxx:
            print(exxx)
            pass

    loop.close()

    news_dict_list = [dataclasses.asdict(news) for news in my_class_objects]
    with open(path_out_data, "w") as json_file:
        json.dump(news_dict_list, json_file, indent=4)


if __name__ == "__main__":
    text_to_speech()

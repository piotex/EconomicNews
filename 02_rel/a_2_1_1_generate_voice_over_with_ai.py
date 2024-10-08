import asyncio
import edge_tts
from unidecode import unidecode
import time
from news_model import *


async def edge_tts_generate_to_file(text: str, path:str, voice_model:str) -> None:
    speed = "+25%"
    if voice_model == "pl-PL-MarekNeural":
        speed = "+35%"

    communicate = edge_tts.Communicate(text, voice_model, rate=speed)
    await communicate.save(path+".mp3")

    communicate = edge_tts.Communicate(text, voice_model, rate=speed)
    sub_maker = edge_tts.SubMaker()
    with open(path+".mp3", "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                sub_maker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])

    with open(path+".vvt", "w", encoding="utf-8") as file:
        file.write(sub_maker.generate_subs())


async def wrapper_edge_tts_generate_to_file(elem: NewsModel, file_path: str):
    voice_models = ["pl-PL-MarekNeural","pl-PL-ZofiaNeural"]
    text_list = elem.parsed_text.split(".")
    text_list = [a.replace("\n",'') for a in text_list if a != ""]

    for i, text in enumerate(text_list):
        file_name = "audio_file_name" # unidecode(text.replace(' ','_').replace('"','').replace("'",'').replace('"',''))[:15]
        path = f"{file_path}/{i}_{file_name}"
        await edge_tts_generate_to_file(text, path, voice_models[i % len(voice_models)])


def text_to_speech(elem: NewsModel, file_path: str):
    try:
        asyncio.run(wrapper_edge_tts_generate_to_file(elem, file_path))
    except Exception as exxx:
        print(f"ERROR: {exxx}")
        pass


def main():
    model_list = load_obj_list()
    for i, model in enumerate(model_list):
        text_to_speech(model, f"data/audios/{i}")


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    total_s = end_time - start_time
    total_m = int(total_s / 60)
    total_s = int(total_s - total_m * 60)
    print(f"")
    print(f"#####################################")
    print(f"Total time: {total_m}m {total_s}s")
    print(f"#####################################")

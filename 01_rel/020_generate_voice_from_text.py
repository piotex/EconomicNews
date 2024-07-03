import asyncio
import edge_tts
from news_model import *


async def edge_tts_generate_to_file(model: NewsModel) -> None:
    voice_model = "pl-PL-ZofiaNeural"  # pl-PL-MarekNeural
    speed = "+25%"

    communicate = edge_tts.Communicate(model.article_text, voice_model, rate=speed)
    await communicate.save(model.mp3_path)

    communicate = edge_tts.Communicate(model.article_text, voice_model, rate=speed)
    sub_maker = edge_tts.SubMaker()
    with open(model.mp3_path, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                sub_maker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])

    with open(model.vvt_path, "w", encoding="utf-8") as file:
        file.write(sub_maker.generate_subs())


async def wrapper_edge_tts_generate_to_file(elem: NewsModel):
    await edge_tts_generate_to_file(elem)


def text_to_speech(elem: NewsModel):
    elem.mp3_path = f"data/audio/{elem.idx}.mp3"
    elem.vvt_path = f"data/audio/{elem.idx}.vvt"
    try:
        asyncio.run(wrapper_edge_tts_generate_to_file(elem))
    except Exception as exxx:
        print(f"ERROR: {exxx}")
        pass


def main():
    obj_list = load_obj_list()
    m_obj = obj_list[0]
    text_to_speech(m_obj)
    save_obj_list(obj_list)


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

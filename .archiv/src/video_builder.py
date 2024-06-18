import sys
import json
import dataclasses
from models.model_news import NewsModel
from general_utils import get_idx_to_process
from moviepy.editor import VideoFileClip, AudioFileClip


def video_builder(idx_to_process):
    func_name = "video_builder"
    print(f"{func_name}: {idx_to_process}")
    path_news_list = "../data_files/important_files/news_list.json"

    with open(path_news_list, "r") as json_file:
        data_from_json = json.load(json_file)
    my_class_objects = [NewsModel(**item) for item in data_from_json]

    idx = 0
    for elem in my_class_objects:
        if idx == idx_to_process:
            elem.video_quick_info_mp4_path = f"../data_files/movies/{elem.id}.video_builder.mp4"
            clip_gif = VideoFileClip(elem.video_quick_info_gif_path)
            audio = AudioFileClip(elem.audio_quick_info_mp3_path)

            speed_val = clip_gif.duration / audio.duration
            video_clip = clip_gif.speedx(factor=speed_val)
            video_clip = video_clip.set_audio(audio)
            video_clip.write_videofile(elem.video_quick_info_mp4_path, codec='libx264', audio_codec='aac')
        idx += 1

    news_dict_list = [dataclasses.asdict(news) for news in my_class_objects]
    with open(path_news_list, "w") as json_file:
        json.dump(news_dict_list, json_file, indent=4)


if __name__ == "__main__":
    if __name__ == "__main__":
        if len(sys.argv) > 1:
            idx_to_process_arg = get_idx_to_process()
            video_builder(idx_to_process_arg)
        else:
            for i in range(5):
                video_builder(i)

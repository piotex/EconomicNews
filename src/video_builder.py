import dataclasses
import json
from moviepy.editor import VideoFileClip, AudioFileClip
from models.model_news import NewsModel


def video_builder():
    path_in_data = "../data_files/important_files/6_gif_builder.json"
    path_out_data = "../data_files/important_files/7_video_builder.json"

    with open(path_in_data, "r") as json_file:
        data_from_json = json.load(json_file)
    my_class_objects = [NewsModel(**item) for item in data_from_json]

    i = 0
    for elem in my_class_objects:
        print(f"video_builder: {i}")
        i += 1
        elem.video_quick_info_mp4_path = f"../data_files/movies/{elem.id}.video_builder.mp4"
        clip_gif = VideoFileClip(elem.video_quick_info_gif_path)
        audio = AudioFileClip(elem.audio_quick_info_mp3_path)

        speed_val = clip_gif.duration / audio.duration
        video_clip = clip_gif.speedx(factor=speed_val)
        video_clip = video_clip.set_audio(audio)
        video_clip.write_videofile(elem.video_quick_info_mp4_path, codec='libx264', audio_codec='aac')

    news_dict_list = [dataclasses.asdict(news) for news in my_class_objects]
    with open(path_out_data, "w") as json_file:
        json.dump(news_dict_list, json_file, indent=4)


if __name__ == "__main__":
    video_builder()
